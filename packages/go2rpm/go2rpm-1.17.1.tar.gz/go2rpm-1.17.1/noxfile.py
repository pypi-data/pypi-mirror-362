# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: MIT

from __future__ import annotations

import os
from glob import iglob
from pathlib import Path

import nox

IN_CI = "JOB_ID" in os.environ or "CI" in os.environ
# TODO(anyone): Disable editable mode in CI once the coverage issue is figured out.
# ALLOW_EDITABLE = os.environ.get("ALLOW_EDITABLE", str(not IN_CI)).lower() in (
ALLOW_EDITABLE = os.environ.get("ALLOW_EDITABLE", str(True)).lower() in (
    "1",
    "true",
)

PROJECT = "go2rpm"
SPECFILE = "go2rpm.spec"
LINT_SESSIONS = (
    "formatters",
    "codeqa",
    # "typing",
)
LINT_FILES = (PROJECT, "tests/", "noxfile.py")

nox.options.sessions = ("lint", "covtest")


# Helpers


def install(session: nox.Session, *args, editable=False, **kwargs):
    # nox --no-venv
    if isinstance(session.virtualenv, nox.virtualenv.PassthroughEnv):
        session.warn(f"No venv. Skipping installation of {args}")
        return
    if editable and ALLOW_EDITABLE:
        args = ("-e", *args)
    session.install(*args, **kwargs)


def git(session: nox.Session, *args, **kwargs):
    return session.run("git", *args, **kwargs, external=True)


# General


@nox.session(python=["3.9", "3.10", "3.11", "3.12"])
def test(session: nox.Session):
    packages: list[str] = [".[test]"]
    env: dict[str, str] = {}
    tmp = Path(session.create_tmp())

    if any(i.startswith("--cov") for i in session.posargs):
        packages.extend(("coverage[toml]", "pytest-cov"))
        env["COVERAGE_FILE"] = str(tmp / ".coverage")

    install(session, *packages, editable=True)
    session.run("pytest", *session.posargs, env=env)


@nox.session
def coverage(session: nox.Session):
    install(session, "coverage[toml]")
    session.run("coverage", "combine", "--keep", *iglob(".nox/test*/tmp/.coverage"))
    session.run("coverage", "xml")
    session.run("coverage", "html")
    session.run("coverage", "report")


@nox.session()
def covtest(session: nox.Session):
    session.run("rm", "-f", *iglob(".nox/*/tmp/.coverage*"), external=True)
    test_sessions = (f"test-{v}" for v in test.python)  # type: ignore[attr-defined]
    for target in test_sessions:
        session.notify(target, ["--cov"])
    session.notify("coverage")


@nox.session(venv_backend="none")
def lint(session: nox.Session):
    """
    Run formatters, codeqa, and typing sessions
    """
    for notify in LINT_SESSIONS:
        session.notify(notify)


@nox.session
def codeqa(session: nox.Session):
    install(session, ".[codeqa]")
    session.run("ruff", "check", *session.posargs, *LINT_FILES)
    session.run("pymarkdownlnt", "scan", *session.posargs, *iglob("*.md"))


@nox.session
def formatters(session: nox.Session):
    install(session, ".[formatters]")
    posargs = session.posargs
    if IN_CI:
        posargs.append("--check")
    session.run("black", *posargs, *LINT_FILES)
    session.run("isort", *posargs, *LINT_FILES)


# Disable for now
# @nox.session
# def typing(session: nox.Session):
#     install(session, ".[typing]", editable=True)
#     session.run("mypy", *LINT_FILES)


@nox.session
def bump(session: nox.Session):
    version = session.posargs[0]

    install(session, "build", "releaserr >= 0.1.dev123", "fclogr", "flit")
    session.run("releaserr", "--version")

    session.run("releaserr", "check-tag", version)
    session.run("releaserr", "ensure-clean")
    session.run("releaserr", "set-version", "-s", "file", version)

    install(session, ".")

    # Bump specfile
    # fmt: off
    session.run(
        "fclogr", "bump",
        "--new", version,
        "--comment", f"Release {version}.",
        SPECFILE,
    )
    # fmt: on

    # Bump changelog, commit, and tag
    git(session, "add", SPECFILE, f"{PROJECT}/__init__.py")
    session.run("releaserr", "clog", version, "--tag")
    session.run("releaserr", "build", "--backend", "flit_core")


@nox.session
def publish(session: nox.Session):
    # Setup
    install(session, "releaserr")
    session.run("releaserr", "--version")

    session.run("releaserr", "ensure-clean")

    # Upload to PyPI
    session.run("releaserr", "upload")

    # Push to git
    if not session.interactive or input("Push to forge (Y/n) ").lower() in ("", "y"):
        git(session, "push", "--follow-tags")

    # Post-release bump
    session.run("releaserr", "post-version", "-s", "file")
    git(session, "add", f"{PROJECT}/__init__.py")
    git(session, "commit", "-S", "-m", "Post release version bump")


def releaserr(session: nox.Session):
    session.install("releaserr")
    session.run("releaserr", *session.posargs)
