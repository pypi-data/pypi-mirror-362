from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import time
from collections.abc import Callable
from datetime import datetime, timezone
from functools import partial
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import IO
from urllib.parse import urlparse

import aiohttp
import git
import jinja2

from . import __version__

DEFAULT_EDITOR = "vi"
XDG_CACHE_HOME = os.getenv("XDG_CACHE_HOME", os.path.expanduser("~/.cache"))
CACHEDIR = os.path.join(XDG_CACHE_HOME, "go2rpm")
GIT_CACHEDIR = os.path.join(XDG_CACHE_HOME, "go2rpm", "src")
JINJA_ENV = jinja2.Environment(
    loader=jinja2.ChoiceLoader(
        [
            jinja2.FileSystemLoader(["/"]),
            jinja2.PackageLoader("go2rpm", "templates"),
        ]
    ),
    extensions=["jinja2.ext.do"],
    trim_blocks=True,
    lstrip_blocks=True,
)
SPECTOOL_PATH = shutil.which("spectool")
GO_VENDOR_LICENSE_AUTODETECT_DOC = "https://fedora.gitlab.io/sigs/go/go-vendor-tools/scenarios/#manually-detecting-licenses"
COLOR = None
RED = "\033[31m"  # ]
BLUE = "\033[34m"  # ]
CLEAR = "\033[0m"  # ]

eprint = partial(print, file=sys.stderr)


def colorlog(__msg: str, /, *, fg=RED, file: IO[str] = sys.stdout) -> None:
    color = COLOR
    if color is None:
        color = file.isatty()
    print(f"{fg if color else ''}{__msg}{CLEAR if color else ''}", file=file)


def detect_packager():
    rpmdev_packager = shutil.which("rpmdev-packager")
    if rpmdev_packager is not None:
        return subprocess.check_output(rpmdev_packager, universal_newlines=True).strip()

    gitbinary = shutil.which("git")
    if gitbinary is not None:
        name = subprocess.check_output(
            [gitbinary, "config", "user.name"], universal_newlines=True
        ).strip()
        email = subprocess.check_output(
            [gitbinary, "config", "user.email"], universal_newlines=True
        ).strip()
        return f"{name} <{email}>"
    return None


def file_mtime(path):
    return datetime.fromtimestamp(os.stat(path).st_mtime, timezone.utc).isoformat()


@jinja2.pass_environment
def do_customwordwrap(
    environment,
    s,
    width=79,
    break_long_words=True,
    wrapstring=None,
    break_on_hyphens=False,
):
    """
    Return a copy of the string passed to the filter wrapped after
    ``79`` characters.  You can override this default using the first
    parameter.  If you set the second parameter to `false` Jinja will not
    split words apart if they are longer than `width`. By default, the newlines
    will be the default newlines for the environment, but this can be changed
    using the wrapstring keyword argument.
    """
    if not wrapstring:
        wrapstring = environment.newline_sequence
    import textwrap

    return wrapstring.join(
        textwrap.wrap(
            s,
            width=width,
            expand_tabs=False,
            replace_whitespace=False,
            break_long_words=break_long_words,
            break_on_hyphens=break_on_hyphens,
        )
    )


# Sanitize a Go import path that can then serve as rpm package name
# Mandatory parameter: a Go import path
def rpmname(goipath, use_new_versioning=True):
    # lowercase and end with '/'
    goname = goipath.lower() + "/"
    # remove eventual protocol prefix
    goname = re.sub(r"^http(s?):\/\/", r"", goname)
    # remove eventual .git suffix
    goname = re.sub(r"\.git\/", r"", goname)
    # remove eventual git. prefix
    goname = re.sub(r"^git\.", r"", goname)
    # remove FQDN root (.com, .org, etc)
    # will also remove vanity FQDNs such as "tools"
    goname = re.sub(r"^([^/]+)\.([^\./]+)/", r"\g<1>/", goname)
    # add golang prefix
    goname = "golang-" + goname
    # special-case x.y.z number-strings as that’s an exception in our naming
    # guidelines
    while re.search(r"(\d)\.(\d)", goname):
        goname = re.sub(r"(\d)\.(\d)", r"\g<1>:\g<2>", goname)
    # replace various separators rpm does not like with -
    goname = re.sub(r"[\._/\-\~]+", r"-", goname)
    # because of the Azure sdk
    goname = re.sub(r"\-for\-go\-", r"-", goname)
    # Tokenize along - separators and remove duplicates to avoid
    # golang-foo-foo-bar-foo names
    result = ""
    tokens = {}
    tokens["go"] = True
    for token in goname.split("-"):
        if token not in tokens:
            result = result + "-" + token
            tokens[token] = True
    # reassemble the string, restore x.y.z runs, convert the vx.y.z
    # Go convention to x.y.z as prefered in rpm naming
    result = re.sub(r"^-", r"", result)
    result = re.sub(r"-$", r"", result)
    result = re.sub(r":", r".", result)
    # some projects have a name that end up in a number, and *also* add release
    # numbers on top of it, keep a - prefix before version strings
    result = re.sub(r"\-v(\d[\.\d]*)$", r"-\g<1>", result)
    result = re.sub(r"\-v(\d[\.\d]*\-)", r"-\g<1>", result)
    # according to the guidelines, if the base package name does not end with
    # a digit, the version MUST be directly appended to the package name with
    # no intervening separator.
    # If the base package name ends with a digit, a single underscore (_) MUST
    # be appended to the name, and the version MUST be appended to that, in
    # order to avoid confusion over where the name ends and the version begins.
    if use_new_versioning:
        result = re.sub(
            r"([^-]*)(-)([\.0-9]+)$",
            lambda m: (
                f"{m.group(1)}_{m.group(3)}"
                if re.search(r"\d$", m.group(1))
                else f"{m.group(1)}{m.group(3)}"
            ),
            result,
        )
    return result


def has_cmd(git_local_path):
    cmd = os.path.isdir(os.path.join(git_local_path, "cmd"))
    return cmd


def has_other_cmd(git_local_path):
    other_cmd = set()
    exclude = set(
        [
            "cmd",
            "vendor",
            "example",
            "examples",
            "_example",
            "_examples",
            "internal",
            "Godeps",
            "testdata",
            "_testdata",
            "tests",
            "test",
        ]
    )
    for root, dirs, files in os.walk(git_local_path, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        for file in files:
            if file.endswith(".go"):
                with open(os.path.join(root, file), "r") as f:
                    for line in f:
                        if line.startswith("package main"):
                            other_cmd.add(os.path.relpath(root, git_local_path))
                            break
    return list(other_cmd)


def detect_license(git_local_path):
    licenses = set()
    raw_licenses = subprocess.check_output(
        ["askalono", "--format", "json", "crawl", git_local_path],
        universal_newlines=True,
    )
    raw_licenses = to_list(raw_licenses)
    for j in raw_licenses:
        try:
            if "vendor" not in json.loads(j)["path"]:
                licenses.add(json.loads(j)["result"]["license"]["name"])
        except KeyError:
            pass
    return " AND ".join(list(licenses))


def get_license_files(git_local_path):
    license_files = []
    exclude = set(
        [
            "vendor",
            "example",
            "examples",
            "_example",
            "_examples",
            "internal",
            "Godeps",
            "testdata",
            "_testdata",
            ".github",
            "tests",
            "test",
        ]
    )
    matcher = re.compile(
        r"(COPYING|COPYING[\.\-].*|COPYRIGHT|COPYRIGHT[\.\-].*|"
        r"EULA|EULA[\.\-].*|licen[cs]e|licen[cs]e.*|LICEN[CS]E|"
        r"LICEN[CS]E[\.\-].*|.*[\.\-]LICEN[CS]E.*|NOTICE|NOTICE[\.\-].*|"
        r"PATENTS|PATENTS[\.\-].*|UNLICEN[CS]E|UNLICEN[CS]E[\.\-].*|"
        r"agpl[\.\-].*|gpl[\.\-].*|lgpl[\.\-].*|AGPL-.*[0-9].*|"
        r"APACHE-.*[0-9].*|BSD-.*[0-9].*|CC-BY-.*|GFDL-.*[0-9].*|"
        r"GNU-.*[0-9].*|GPL-.*[0-9].*|LGPL-.*[0-9].*|MIT-.*[0-9].*|"
        r"MPL-.*[0-9].*|OFL-.*[0-9].*)"
    )
    for root, dirs, files in os.walk(git_local_path, topdown=True):
        dirs[:] = [d for d in dirs if d not in exclude]
        dirs.sort()
        for f in sorted(files):
            if matcher.match(f):
                license_files.append(
                    os.path.relpath(os.path.join(root, f), git_local_path)
                )
    return license_files


def get_doc_files(git_local_path):
    doc_files = []
    include = set(["doc", "docs", "example", "examples", "_example", "_examples"])
    exclude = set(
        [
            "vendor",
            "doc",
            "docs",
            "example",
            "examples",
            "_example",
            "_examples",
            "internal",
            "Godeps",
            "testdata",
            "_testdata",
            ".github",
            "tests",
            "test",
            ".circleci",
        ]
    )
    matcher = re.compile(
        r"(.*\.md|.*\.markdown|.*\.mdown|.*\.mkdn|.*\.rst|.*\.txt|AUTHORS|"
        r"AUTHORS[\.\-].*|CONTRIBUTORS|CONTRIBUTORS[\.\-].*|README|"
        r"README[\.\-].*|CHANGELOG|CHANGELOG[\.\-].*|TODO|TODO[\.\-].*)",
        re.IGNORECASE,
    )
    licensesex = re.compile(
        r"(COPYING|COPYING[\.\-].*|COPYRIGHT|COPYRIGHT[\.\-].*|EULA|"
        r"EULA[\.\-].*|licen[cs]e|licen[cs]e.*|LICEN[CS]E|LICEN[CS]E[\.\-].*|"
        r".*[\.\-]LICEN[CS]E.*|NOTICE|NOTICE[\.\-].*|PATENTS|PATENTS[\.\-].*|"
        r"UNLICEN[CS]E|UNLICEN[CS]E[\.\-].*|agpl[\.\-].*|gpl[\.\-].*|"
        r"lgpl[\.\-].*|AGPL-.*[0-9].*|APACHE-.*[0-9].*|BSD-.*[0-9].*|CC-BY-.*|"
        r"GFDL-.*[0-9].*|GNU-.*[0-9].*|GPL-.*[0-9].*|LGPL-.*[0-9].*|"
        r"MIT-.*[0-9].*|MPL-.*[0-9].*|OFL-.*[0-9].*|CMakeLists\.txt)"
    )
    for root, dirs, files in os.walk(git_local_path, topdown=True):
        doc_files = doc_files + [d for d in dirs if d in include]
        dirs[:] = [d for d in dirs if d not in exclude]
        dirs.sort()
        for f in sorted(files):
            if matcher.match(f) and not licensesex.match(f):
                doc_files.append(os.path.relpath(os.path.join(root, f), git_local_path))
    return doc_files


async def get_description(forge):
    owner = forge.split("/")[-2]
    repo = forge.split("/")[-1]
    if "github.com" in forge:
        api_url = f"https://api.github.com/repos/{owner}/{repo}"
    elif "gitlab.com" in forge:
        api_url = f"https://gitlab.com/api/v4/projects/{owner}%2F{repo}"
    elif "bitbucket.org" in forge:
        api_url = f"https://api.bitbucket.org/2.0/repositories/{owner}/{repo}"
    elif "pagure.io" in forge:
        repo = "/".join(forge.split("/")[3:])
        api_url = f"https://pagure.io/api/0/{repo}"
    elif any(domain in forge for domain in ["gitea.com", "codeberg.org"]):
        parsed_url = urlparse(forge)
        base_url = parsed_url.netloc
        api_url = f"https://{base_url}/api/v1/repos/{owner}/{repo}"
    else:
        return None

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url) as resp:
            jsonresp = await resp.json()
            if "message" in jsonresp or "error" in jsonresp:
                return None
            return normalize_description(jsonresp["description"])


def normalize_description(description):
    if description is not None:
        description = description.strip()
    else:
        return description
    if description != "":
        description = description[:1].upper() + description[1:]
    else:
        return None
    if not re.search(r"(\.|!)$", description):
        description = description + "."
    return description


def get_repo_name(forge):
    url = forge.split("/")
    return url[2:]


def get_subdirectory(subdir):
    if subdir and not subdir.startswith("/"):
        subdir = "/" + subdir
    if subdir:
        url = subdir.split("/")
    else:
        url = ""
    return url


def get_repo_host(forge):
    url = forge.split("/")
    return url[0:3]


def download(forge):
    # shutil.rmtree(os.path.join(GIT_CACHEDIR, *get_repo_name(forge)), ignore_errors=True)
    git_local_path = os.path.join(GIT_CACHEDIR, *get_repo_name(forge))
    try:
        repo = git.Repo.clone_from(forge, git_local_path)
        repo.head.reference = repo.heads[0]
        repo.head.reset(index=True, working_tree=True)
    except git.GitCommandError as err:
        if "is not an empty directory" in err.stderr:
            try:
                repo = git.Repo(git_local_path)
                repo.remotes[0].fetch()
                repo.git.checkout(repo.heads[0])
                repo.git.clean("-xdf")
                repo.git.reset(repo.remotes[0].refs[0], "--hard")
            except git.GitCommandError as err:
                print(f"ERROR: Unable to 'git pull {forge}':")
                print(err.stderr)
                print("Try deleting the cache with the -C flag.")
                sys.exit(1)
        else:
            print(f"ERROR: Unable to 'git clone {forge}':")
            print(err.stderr)
            sys.exit(1)


def get_version(git_local_path):
    repo = git.Repo(git_local_path)
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    if not len(tags):
        commit = str(repo.heads[0].commit)
        version = None
        tag = None
    else:
        latest = str(tags[-1])
        if latest.startswith("v"):
            version = latest[1:]
            tag = None
        else:
            version = None
            tag = latest
        tag_date = datetime.now(timezone.utc) - tags[-1].commit.committed_datetime
        if (
            tag_date.days > 365
            and repo.heads[0].commit.count() - tags[-1].commit.count() > 14
        ):
            commit = str(repo.heads[0].commit)
        else:
            commit = None
    return version, tag, commit


def check_if_version_exists(git_local_path, version, tag, commit):
    repo = git.Repo(git_local_path)
    repo.remotes[0].fetch()
    repo.git.checkout(repo.heads[0])
    repo.git.clean("-xdf")
    repo.git.reset(repo.remotes[0].refs[0], "--hard")
    if commit:
        try:
            repo.git.checkout(commit)
        except git.GitCommandError:
            return False
    elif tag:
        try:
            repo.git.checkout(tag)
        except git.GitCommandError:
            return False
    elif version:
        try:
            repo.git.checkout("v" + version)
        except git.GitCommandError:
            return False
    return True


def set_repo_version(git_local_path, version, tag, commit):
    repo = git.Repo(git_local_path)
    repo.remotes[0].fetch()
    repo.git.checkout(repo.heads[0])
    repo.git.clean("-xdf")
    repo.git.reset(repo.remotes[0].refs[0], "--hard")
    if commit:
        repo.git.checkout(commit)
    elif tag:
        repo.git.checkout(tag)
    elif version:
        repo.git.checkout("v" + version)


def get_buildrequires(forge, subdir):
    os.environ["GOPATH"] = CACHEDIR
    os.environ["GO111MODULE"] = "off"
    buildrequires = subprocess.check_output(
        [
            "golist",
            "--imported",
            "--skip-self",
            "--package-path",
            "/".join(get_repo_name(forge)) + subdir,
        ],
        universal_newlines=True,
    )
    return buildrequires


def get_test_buildrequires(forge, subdir):
    os.environ["GOPATH"] = CACHEDIR
    os.environ["GO111MODULE"] = "off"
    test_buildrequires = subprocess.check_output(
        [
            "golist",
            "--imported",
            "--tests",
            "--skip-self",
            "--package-path",
            "/".join(get_repo_name(forge)) + subdir,
        ],
        universal_newlines=True,
    )
    return test_buildrequires


def to_list(s):
    if not s:
        return []
    return [line.strip() for line in s.splitlines()]


def main(argv: list[str] | None = None) -> int:
    rc = 0
    parser = argparse.ArgumentParser(
        "go2rpm", formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument(
        "--color",
        action=argparse.BooleanOptionalAction,
        default=False if os.environ.get("NO_COLOR") else None,
    )
    parser.add_argument("-V", "--go2rpm-version", action="version", version=__version__)
    changelog_group = parser.add_mutually_exclusive_group()
    changelog_group.add_argument(
        "-r",
        "--rpmautospec",
        action="store_true",
        default=True,
        help="Use autorelease and autochangelog features",
    )
    changelog_group.add_argument(
        "-n",
        "--no-rpmautospec",
        action="store_false",
        dest="rpmautospec",
        help="Use static release and changelog instead of rpmautospec.",
    )
    parser.add_argument(
        "--no-auto-changelog-entry",
        action="store_true",
        help="Do not generate a changelog entry",
    )
    versioning_group = parser.add_mutually_exclusive_group()
    versioning_group.add_argument(
        "-L",
        "--use-new-versioning",
        action="store_true",
        default=True,
        help="Enable new naming scheme for versioned compat packages that\n"
        "respect Fedora Packaging Guidelines.\n"
        "All new go packages should use this option.",
    )
    versioning_group.add_argument(
        "--no-use-new-versioning",
        action="store_false",
        dest="use_new_versioning",
        help="Use older naming scheme for versioned compat packages.\n"
        "This does not respect Fedora Packaging Guidelines and\n"
        "should not be used for new packages.",
    )
    parser.add_argument(
        "-", "--stdout", action="store_true", help="Print spec into stdout"
    )
    parser.add_argument(
        "-p",
        "--profile",
        action="store",
        nargs="?",
        choices=["1", "2", "vendor"],
        default="2",
        help="Profile of macros to use. \
                        1: legacy macros. 2: current macros. \
                        vendor: support bundled vendoring. \
                        default: 2",
    )
    parser.add_argument(
        "-q",
        "--no-spec-warnings",
        dest="spec_warnings",
        action="store_false",
        help="Exclude warning comments from generated specfile.\n"
        "Currently, this only removes the %%gometa -f explanatory comment.",
    )
    parser.add_argument("-f", "--forge", action="store", nargs="?", help="Forge URL")
    parser.add_argument(
        "-s",
        "--subdir",
        action="store",
        nargs="?",
        default=None,
        help="Git subdirectory to specifically package",
    )
    parser.add_argument(
        "-a",
        "--altipaths",
        action="store",
        nargs="+",
        help="List of alternate import paths",
    )
    parser.add_argument(
        "-v", "--version", action="store", nargs="?", help="Package version"
    )
    parser.add_argument("-t", "--tag", action="store", nargs="?", help="Package tag")
    parser.add_argument(
        "-c", "--commit", action="store", nargs="?", help="Package commit"
    )
    dynamic_br_group = parser.add_mutually_exclusive_group()
    dynamic_br_group.add_argument(
        "--dynamic-buildrequires",
        action="store_true",
        help="Use dynamic BuildRequires feature",
    )
    dynamic_br_group.add_argument(
        "-R",
        "--no-dynamic-buildrequires",
        action="store_true",
        help="Do not use dynamic BuildRequires feature",
    )
    parser.add_argument(
        "-C",
        "--clean",
        action="store_true",
        default=True,
        help="Clean cache for chosen Go import path",
    )
    parser.add_argument("--no-clean", action="store_false", dest="clean")
    parser.add_argument(
        "--clean-all", action="store_true", help="Clean all cached Go imports"
    )
    parser.add_argument(
        "-d",
        "--create-directory",
        action="store_true",
        help="Save the final specfile output to NAME/NAME.spec",
    )
    parser.add_argument(
        "--name",
        help="Specify the name for the spec file (max 64 characters).\n"
        "This is useful for binary applications.",
    )
    parser.add_argument(
        "--print-name",
        action="store_true",
        help="Print the generated package name and exit",
    )
    parser.add_argument(
        "--download",
        help="Download source tarball with spectool",
        action=argparse.BooleanOptionalAction,
        dest="download",
        default=None,
    )
    vendor_profile_group = parser.add_argument_group(
        "vendor profile", description="Arguments that only apply to the vendor profile"
    )
    vendor_profile_group.add_argument(
        "--compresslevel",
        help="See '--compresslevel' in 'man go_vendor_archive_create'.",
        default=None,
        type=int,
    )
    vendor_profile_group.add_argument(
        "--compression",
        help="See '--compression' in 'man go_vendor_archive_create'"
        " Default: %(default)s",
        default="bz2",
    )
    vendor_profile_group.add_argument(
        "--detector", help="Which license detector to use with go_vendor_license"
    )
    parser.add_argument("goipath", help="Import path")
    args = parser.parse_args(argv)

    global COLOR
    COLOR = args.color

    if args.download:
        if args.stdout:
            eprint("--stdout and --download are incompatible!")
            rc = 1
            return rc
        if not SPECTOOL_PATH:
            eprint(
                "spectool is not installed."
                " Install rpmdevtools and try again or pass --no-download."
            )
            rc = 1
            return rc

    subdir = "/".join(get_subdirectory(args.subdir))
    goipath = re.sub(r"^http(s?)://", r"", args.goipath)
    goipath = goipath.strip("/")
    if args.name:
        name = args.name
    else:
        name = rpmname(goipath + subdir, args.use_new_versioning)
    if len(name) > 64:
        eprint("Warning - package name shouldn't be larger than 64 characters")
        # This is a non-fatal error, but we want the program to eventually exit
        # with a non-zero exit code
        rc = 1
    if args.print_name:
        print(name)
        rc = 0
        return rc

    known_forge = (
        "github.com",
        "gitlab.com",
        "bitbucket.org",
        "pagure.io",
        "gitea.com",
        "codeberg.org",
    )
    known_forge_re = r"^(" + r"|".join(re.escape(url) for url in known_forge) + r")"
    if not re.search(known_forge_re, goipath) and args.forge is None:
        print(
            "The forge provided is not known by go-rpm-macros. You will have to provide the source and archive parameters manually.",
            file=sys.stderr,
        )

    if args.forge is None:
        forge = "https://" + goipath
    else:
        if not args.forge.startswith("http"):
            args.forge = "https://" + args.forge
        forge = args.forge.strip("/")

    git_local_path = os.path.join(GIT_CACHEDIR, *get_repo_name(forge))

    # Clean any existing repos, if requested.
    if args.clean_all:
        shutil.rmtree(GIT_CACHEDIR, ignore_errors=True)
    elif args.clean:
        shutil.rmtree(git_local_path, ignore_errors=True)

    # Download the repo
    download(forge)

    # Sort out the versions
    if args.version is not None or args.tag is not None or args.commit is not None:
        if not check_if_version_exists(
            git_local_path, args.version, args.tag, args.commit
        ):
            version, tag, commit = get_version(git_local_path)
        else:
            version, tag, commit = args.version, args.tag, args.commit
    else:
        version, tag, commit = get_version(git_local_path)

    # Prepare the repo
    set_repo_version(git_local_path, version, tag, commit)

    if args.no_dynamic_buildrequires:
        # Get BuildRequires and filter them out of test BuildRequires
        buildrequires = to_list(get_buildrequires(forge, subdir))
        buildrequires = [ipath for ipath in buildrequires if goipath not in ipath]
        test_buildrequires = list(
            set(to_list(get_test_buildrequires(forge, subdir))).difference(
                set(buildrequires)
            )
        )
        test_buildrequires = [
            ipath for ipath in test_buildrequires if goipath not in ipath
        ]
    else:
        args.dynamic_buildrequires = True
        buildrequires = []
        test_buildrequires = []

    description = asyncio.run(get_description(forge))
    if description is not None:
        summary = description[:-1]
    else:
        summary = None

    license_files = (
        get_license_files(git_local_path) if args.profile != "vendor" else []
    )
    doc_files = get_doc_files(git_local_path)

    cmd = has_cmd(git_local_path)
    other_cmd = has_other_cmd(git_local_path)
    if "." in other_cmd:
        main_cmd = get_repo_name(forge)[-1]
        other_cmd.remove(".")
    else:
        main_cmd = None

    JINJA_ENV.filters["customwordwrap"] = do_customwordwrap
    if args.profile == "1":
        template = JINJA_ENV.get_template("profile1.spec")
    elif args.profile == "2":
        template = JINJA_ENV.get_template("profile2.spec")
    elif args.profile == "vendor":
        template = JINJA_ENV.get_template("vendor.spec")
        # Set --download to the default with vendor profile
        args.download = True if args.download is None else args.download

    kwargs = {}
    kwargs["generator_version"] = __version__
    kwargs["detector"] = args.detector
    kwargs["goipath"] = goipath
    kwargs["goname"] = args.name
    kwargs["name"] = name
    kwargs["forge"] = forge
    kwargs["subdir"] = subdir
    kwargs["altipaths"] = args.altipaths

    kwargs["version"] = version
    kwargs["tag"] = tag
    kwargs["commit"] = commit

    kwargs["description"] = description
    kwargs["summary"] = summary

    kwargs["license_files"] = license_files
    kwargs["doc_files"] = doc_files

    kwargs["buildrequires"] = buildrequires
    kwargs["test_buildrequires"] = test_buildrequires
    kwargs["generate_buildrequires"] = args.dynamic_buildrequires

    kwargs["has_cmd"] = cmd
    kwargs["main_cmd"] = main_cmd
    kwargs["other_cmd"] = other_cmd

    kwargs["rpmautospec"] = args.rpmautospec
    kwargs["spec_warnings"] = args.spec_warnings
    kwargs["use_new_versioning"] = args.use_new_versioning
    if args.no_auto_changelog_entry:
        kwargs["auto_changelog_entry"] = False
    else:
        kwargs["auto_changelog_entry"] = True

    if version is None and tag is None:
        kwargs["pkg_autorelease"] = "%autorelease -p"
        kwargs["pkg_release"] = "0.1"
    else:
        kwargs["pkg_autorelease"] = "%autorelease"
        kwargs["pkg_release"] = "1"

    kwargs["date"] = time.strftime("%a %b %d %Y")
    kwargs["shortdate"] = time.strftime("%Y%m%d")
    if commit is not None:
        kwargs["shortcommit"] = commit[:7]
    kwargs["packager"] = detect_packager()
    kwargs["vendor_archive_name"] = "%{archivename}-vendor.tar"
    if args.compression != "tar":
        kwargs["vendor_archive_name"] += f".{args.compression}"

    licenses = detect_license(git_local_path)
    if licenses != "":
        kwargs["licenses"] = licenses

    output_dir = Path(name) if args.create_directory else Path(".")
    output_dir.mkdir(exist_ok=True)
    spec_file = output_dir / f"{name}.spec"
    spec_contents = template.render(**kwargs)
    if args.stdout:
        print(f"# {spec_file}")
        print(spec_contents)
    else:
        with open(spec_file, "w") as fobj:
            fobj.write(spec_contents)
        print(spec_file)
    if args.download:
        subprocess.run(["spectool", "-g", spec_file.name], cwd=output_dir, check=True)
    if args.profile == "vendor":
        rc = rc or handle_vendor_archive(
            spec_file,
            output_dir,
            args.download,
            args.compresslevel,
            args.detector,
            partial(template.render, **kwargs),
        )
    return rc


def handle_vendor_archive(
    spec_file: Path,
    output_dir: Path,
    should_run: bool,
    compresslevel: int | None,
    detector: str | None,
    renderer: Callable[..., str],
) -> int:
    """
    Create vendor archive

    Args:
        spec_file: Path to spec
        output_dir: Directory in which to output vendor archive
        should_run:
            Set to False for dry-run mode where the commands are printed but
            not ran.
        compresslevel:
            See go_vendor_archive's compresslevel option
        detector:
            Name of detector backend to use.
            Otherwise, g-v-t uses its default.
        renderer:
            Function used to render specfile template.
            The specfile is rendered a second time to fill in the license
            information provided by g-v-t.
    """
    runner = partial(subprocess.run, check=True, cwd=output_dir)
    # fmt: off
    go_vendor_archive_args: list[str | Path] = [
        "go_vendor_archive",
        "create",
        "--config", "go-vendor-tools.toml",
        "--write-config",
        spec_file.name,
    ]
    # fmt: on
    if compresslevel is not None:
        go_vendor_archive_args.extend(("--compresslevel", str(compresslevel)))
    go_vendor_archive_cmd = shlex.join(map(str, go_vendor_archive_args))
    # fmt: off
    go_vendor_license_args: list[str|Path] = [
        "go_vendor_license",
        *(("--detector", detector) if detector else ()),
        "--config", "go-vendor-tools.toml",
        "--path", spec_file.name,
        "report",
        "--prompt",
        "--autofill", "auto",
        "--write-config",
        "--update-spec",
    ]
    # fmt: on
    go_vendor_license_cmd = shlex.join(map(str, go_vendor_license_args))
    if should_run:
        colorlog(f"$ cd {output_dir}", fg=BLUE)
        colorlog(f"$ {go_vendor_archive_cmd}", fg=BLUE)
        try:
            runner(go_vendor_archive_args)
        except subprocess.CalledProcessError as exc:
            colorlog(f"\n! Command exited {exc.returncode}")
            return exc.returncode
        colorlog(f"$ {go_vendor_license_cmd}", fg=BLUE)
        with NamedTemporaryFile("rt") as fp:
            try:
                runner(go_vendor_license_args + ["--write-json", fp.name])
            except subprocess.CalledProcessError as exc:
                colorlog(
                    "\n! Failed to determine license expression."
                    f" See {GO_VENDOR_LICENSE_AUTODETECT_DOC} for help."
                )
                return exc.returncode
            data = json.load(fp)
            spec_file.write_text(
                renderer(
                    license=data["license_expression"],
                    detector=data["detector_name"],
                )
            )
    else:
        print(
            "When --no-download is specified,"
            " you must create the vendor archive manually:"
        )
        if output_dir != Path():
            print(f"* cd {output_dir}")
        print("* Generate the archive with:", go_vendor_archive_cmd)
        print("* Determine the license expression:", go_vendor_license_cmd)
    return 0


if __name__ == "__main__":
    sys.exit(main())
