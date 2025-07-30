# Copyright (c) 2023 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

from pathlib import Path

import pytest

TEST_DATA = Path(__file__).resolve().parent.joinpath("test_data")


@pytest.fixture
def test_data():
    return TEST_DATA
