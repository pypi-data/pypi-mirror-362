# go2rpm

go2rpm is a Python application designed to assist in the creation of RPM
specfiles for Go (Golang) projects.
It automates the process of
fetching project details, determining dependencies, and generating a specfile.

## Features

- **Automatic Specfile Generation**: go2rpm automatically generates RPM
  specfiles based on the Go project's details and structure.
- **Support for Various Forges**: go2rpm works with different code hosting
  platforms such as GitHub, GitLab, Bitbucket, Pagure, and Gitea.
- **Up to commit level spec generation**: go2rpm can create a spec file based
  on a project's latest release or tag (default) or a custom version, tag, or commit.

## Usage

To use go2rpm, execute the application with the necessary parameters:

``` shell
go2rpm [OPTIONS] GO_IMPORT_PATH
```

### Options

- **-r, --rpmautospec**: Use autorelease and autochangelog features (default)
- **-n, --no-rpmautospec**: Use static release and changelog instead of rpmautospec
- **-L, --use-new-versioning**: Enable new naming scheme for
   versioned compat packages (default)
- **--no-use-new-versioning**: Use older naming scheme for versioned compat packages
- **--no-auto-changelog-entry**: Do not generate a changelog entry
- **--dynamic-buildrequires**: Use dynamic BuildRequires feature (default)
- **-R, --no-dynamic-buildrequires**: Do not use dynamic BuildRequires feature
- **-C, --clean**: Clean cache for chosen Go import path (default)
- **--no-clean**: Do not clean the cache
- **--clean-all**: Clean all cached Go imports
- **-d, --create-directory**: Save the final specfile output to NAME/NAME.spec
- **--name**: Use a specific name for the spec file
- **--print-name**: Print the generated package name and exit
- **-q, --no-spec-warnings**: Exclude warning comments from generated specfile
- **-t, --tag**: Use especified package tag
- **-a, --altipaths**: Include alternate import paths
- **-c, --commit**: Use especified package commit
- **-f, --forge**: Forge URLs
- **-p, --profile**: Use specified profile. Options are:
  1. **1**: Use legacy macros
  1. **2**: Default. Use current macros
  1. **vendor**: Use bundled vendored dependencies
- **-v, --version**: Use especified package versions
- **--stdout**: Print spec into stdout

### Examples

``` shell
# Generate specfile a project hosted on GitHub
go2rpm github.com/rhysd/actionlint

# Generate specfile for a project where import path doesn't match the repository
go2rpm --forge https://github.com/kubernetes/api k8s.io/api

# Generate specfile for a project using a specific commit
go2rpm --commit c2c7a15d6c994356c68dc7a14868c3519836286b --forge 'https://git.sr.ht/~emersion/go-scfg' 'git.sr.ht/~emersion/go-scfg'

# Generate specfile for a project using a specific version
go2rpm -v 2.1.0 github.com/hashicorp/hcl/v2

# Generate specfile with a custom name. This is useful for application packages.
go2rpm --name gh -f https://github.com/cli/cli github.com/cli/cli/v2

# Generate specfile with support for bundled vendoring.
go2rpm --profile vendor -d github.com/cri-o/cri-o --name cri-o
```

### Bundled vendored dependencies

> **NOTE:**
>
> go-vendor-tools, with which go2rpm interfaces to implement this
> functionality, is under active development and may be subject to breaking
> changes.
> Please see go-vendor-tools' [Stability][g-v-t-stability] note for more
> information and join the Fedora Go SIG Matrix room and mailing list
> to be notified of any major changes.

Current [Fedora Golang packaging guidelines][bundled-or-unbundled]
recommend unbundling packages by default.
Bundled dependencies are allowed with justification.
For instance, a complex application with multiple unpackaged dependencies may
justify vendoring.

`go2rpm` can generate a specfile with support for bundled dependencies using
the `--profile vendor` option.
Packagers must also install `go-vendor-tools` alongside `go2rpm` to support the
additional requirements for building and maintaining Golang packages with
bundled vendored dependencies.
`dnf install go2rpm+vendor` will ensure that the necessary dependencies are installed.

For more information, see the [Go Vendor Tools documentation][g-v-t].
Specific package workflow examples for bundled dependencies are in the
[Scenarios][g-v-t-scenarios] section.

[g-v-t-stability]: https://fedora.gitlab.io/sigs/go/go-vendor-tools/#stability
[bundled-or-unbundled]: https://docs.fedoraproject.org/en-US/packaging-guidelines/Golang/#_bundled_or_unbundled
[g-v-t-scenarios]: https://fedora.gitlab.io/sigs/go/go-vendor-tools/scenarios/
[g-v-t]: https://fedora.gitlab.io/sigs/go/go-vendor-tools/

## Requirements

- Python 3
- Git
- Askalono (a license detection tool)
- Aiohttp (for asynchronous HTTP requests)
- Go Vendor Tools (when `--profile vendor` is used)

## License

This application is licensed under the [MIT License](LICENSE).
Feel free to modify and distribute it in accordance with the license terms.
