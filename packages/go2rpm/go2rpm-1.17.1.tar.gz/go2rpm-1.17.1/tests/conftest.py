from __future__ import annotations

from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent


@pytest.fixture()
def test_data() -> Path:
    return HERE / "test_data"
