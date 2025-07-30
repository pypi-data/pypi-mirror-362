from __future__ import annotations

import difflib
from pathlib import Path

import pytest

from go2rpm.__main__ import main


@pytest.mark.network
@pytest.mark.parametrize(
    "args, test_spec",
    [
        pytest.param(
            ["github.com/rhysd/actionlint", "--version", "1.6.26"],
            None,
            id="actionlint",
        ),
        pytest.param(
            ["codeberg.org/UnifiedPush/common-proxies", "--tag", "v2.2.0"],
            None,
            id="common-proxies",
        ),
        pytest.param(
            [
                "--forge",
                "https://github.com/kubernetes/api",
                "--version",
                "0.29.2",
                "--no-spec-warnings",
                "k8s.io/api",
            ],
            None,
            id="golang-k8s-api",
        ),
        pytest.param(
            [
                "--commit",
                "c2c7a15d6c994356c68dc7a14868c3519836286b",
                # TODO(anyone): Test --no-rpmautospec and handle changelog date changes
                # "--no-rpmautospec",
                "--download",
                "git.sr.ht/~emersion/go-scfg",
            ],
            None,
            id="golang-sr-emersion-scfg",
        ),
        pytest.param(
            [
                "https://github.com/rhysd/actionlint",
                "--version=1.6.26",
                "--profile=vendor",
                "--no-download",
                "--name=actionlint",
                "--compression=xz",
            ],
            "actionlint.spec",
            id="actionlint-vendored",
        ),
    ],
)
def test_expected_content(
    args: list[str],
    test_spec: str | None,
    test_data: Path,
    tmp_path: Path,
    capsys: pytest.CaptureFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("go2rpm.__main__.__version__", "<TEST VERSION>")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("RPM_PACKAGER", "Example <example@example.com>")
    main(["--no-clean", *args])
    stdout, _ = capsys.readouterr()
    test_spec = test_spec or Path(stdout.strip()).name
    expected = tmp_path / test_spec
    dest = test_data / stdout.strip().splitlines()[0]
    dest_lines = dest.read_text().splitlines(True)
    expected_lines = expected.read_text().splitlines(True)
    print(expected)
    try:
        assert dest_lines == expected_lines
    except AssertionError:
        print("".join(difflib.unified_diff(expected_lines, dest_lines)))
        raise


@pytest.mark.parametrize(
    "goipath, name, extra_args",
    [
        pytest.param("golang.org/x/sys", "golang-x-sys", []),
        pytest.param(
            "github.com/AdamSLevy/jsonrpc2/v14",
            "golang-github-adamslevy-jsonrpc2_14",
            [],
        ),
        pytest.param(
            "github.com/AdamSLevy/jsonrpc2/v14",
            "golang-github-adamslevy-jsonrpc2-14",
            ["--no-use-new-versioning"],
        ),
        pytest.param(
            "github.com/apparentlymart/go-textseg/v15",
            "golang-github-apparentlymart-textseg15",
            [],
        ),
        pytest.param(
            "github.com/apparentlymart/go-textseg/v15",
            "golang-github-apparentlymart-textseg-15",
            ["--no-use-new-versioning"],
        ),
        pytest.param(
            "filippo.io/edwards25519",
            "golang-filippo-edwards25519",
            [],
        ),
        (
            "github.com/x448/float16",
            "golang-github-x448-float16",
            [],
        ),
    ],
)
def test_expected_name(
    goipath: str, name: str, extra_args: list[str], capsys: pytest.CaptureFixture
) -> None:
    main([goipath, "--print-name", *extra_args])
    stdout, _ = capsys.readouterr()
    assert stdout.strip() == name
