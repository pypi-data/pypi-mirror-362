# NEWS

## 1.17.1 - 2025-07-17 <a id='1.17.1'></a>

Correct error in release process

## 1.17.0 - 2025-07-17 <a id='1.17.0'></a>

- vendor: use `--autofill` feature for go_vendor_license.
- vendor: Bump minimum supported go-vendor-tools to v0.8.0.
- packaging: enforce minimum version of go-vendor-tools when installing RPM
  package.
- templates vendor: get rid of unnecessary `%common_description` macro.
  We can just set `%description` directly.
- templates vendor: turn on go modules mode.
  We don't need `GO111MODULE=off` now that we use vendored dependencies.
  Along with this change, the template switches from `%gocheck` to `%gotest`.
  Additional documentation will be provided.

## 1.16.0 - 2025-03-23 <a id='1.16.0'></a>

- Add forgejo and codeberg to known forges
    (contributed by Mikel Olasagasti).
- Warn if package name length is longer than 64 chars
    (contributed by Mikel Olasagasti).
- vendor: support scancode when unavailable at buildtime.
    Together with the introduction of `%go_vendor_license_check_disable` in
    go-vendor-tools 0.7.0, this allows using scancode as a license detector
    while not pulling it in at buildtime when it's unavailable.
- Require go-vendor-tools >= 0.7.0

## 1.15.0 - 2024-12-12 <a id='1.15.0'></a>

### Added

- cli: group vendor profile flags together in `--help` message
- doc: fully document `--profile` option and add
  "Bundled vendored dependencies" section
  (contributed by Brad Smith)

### Fixed

- cli and templates: properly handle cases when `--tag` and `--version` are
  passed simultaneously
- doc README: fix broken link

## 1.14.0 - 2024-06-30 <a id='1.14.0'></a>

### Added

- Warning indicating not to use globs in generated specs
- A global bootstrap bcond in order to provide a bootstrap workflow

## 1.13.1 - 2024-06-14 <a id='1.13.1'></a>

### Added

- Publish go2rpm to PyPI

### Fixed

- templates vendor: adjust go-vendor-tools–generated comment

## 1.13.0 - 2024-04-10 <a id='1.13.0'></a>

### Added

- `templates`: add consistent sorting to ensure that specfile generation is
  deterministic
- `vendor`: add `--compression` and `--compresslevel` flags
- `vendor`: add informational comment above generated license
- `vendor`: use `bz2` as default compression to match `go-vendor-tools`
- `vendor`; `packaging`: bump minimum go-vendor-tools version

## 1.12.0 - 2024-03-28 <a id='1.12.0'></a>

### Added

- `doc`: extend README file (@mikelolasagasti)
- **`main`: add `vendor` profile and integrate go-vendor-tools**
- `main`: add `--no-clean flag` and use it in tests
- `main`: add `-V/--go2rpm-version` flag
- **`main`: add `--download` flag to download sources**
- `tests`: add basic pytest unit tests

### Changed

- `init`: correct `__version__` constant
- `packaging`: switch to `flit_core` and adopt PEP 621 metadata

### Fixed

- `cli`: print error message to stderr
- **`rpmname`: fix `use_new_versioning` regex for multi-number suffixes**

## 1.11.1 - 2024-04-08 <a id='1.11.1'></a>

This is an **out-of-band release** that includes changes from 1.12.0.

### Fixed

- **`rpmname`: fix use_new_versioning regex**
- `.gitignore`: add missing setuptools build directories
- `init`: correct `__version__` constant
- `setup.py`: fix metadata for upload to PyPI
