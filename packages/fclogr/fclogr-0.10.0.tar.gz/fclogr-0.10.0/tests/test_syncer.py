# Copyright (c) 2023 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import shutil

import pytest

from fclogr.cli import main
from fclogr.cli.base import InvalidArgumentError
from fclogr.cli.sync import Syncer


def test_syncer_same(test_data, tmp_path):
    data = tmp_path / "data"
    shutil.copytree(test_data, data)
    path = data.joinpath("package.spec")
    with pytest.raises(
        InvalidArgumentError, match="Input and output are the same file"
    ):
        Syncer([path], [path])


def test_syncer(test_data, tmp_path):
    data = tmp_path / "data"
    shutil.copytree(test_data, data)
    assert main(["sync", str(data / "package.spec"), str(data / "package.2.spec")]) == 0
    # ruff: noqa: SIM117
    with open(data / "package.2.spec") as output:
        with open(data / "package.3.spec") as expected:
            for o, e in zip(output, expected):
                assert o == e
