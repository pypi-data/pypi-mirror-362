# Release process

1. Ensure `nox` is installed
2. Ensure the `origin` remote points to the upstream repo
3. Ensure `twine` is configured to upload to PyPI.
4. Run full test suite

    ``` shell
    nox
    ```

5. Determine last version

    ``` shell
    last_version=0.1.0
    version=0.2.0
    ```

6. Create changelog fragment

    ``` shell
    git log --pretty='- %s' --reverse v${last_version}..HEAD | \
        grep -vEi '^- (nox|Post.release|ci|lint)' > NEWS_FRAGMENT.md
    ```

    and organize changes in `NEWS_FRAGMENT.md` under `### Added`, `### Changed`,
    `### Deprecated`, and `### Removed` headings as appropriate.
7. Create a version bump and build Python distributions

    ``` shell
    nox -e bump -- ${version}
    ```

8. Upload distributions to PyPI

    ``` shell
    nox -e publish
    ```
