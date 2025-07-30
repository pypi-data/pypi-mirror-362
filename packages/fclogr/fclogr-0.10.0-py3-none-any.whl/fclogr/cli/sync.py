# Copyright (c) 2023 Maxwell G <gotmax@e.email>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import argparse
import logging
import typing
from collections.abc import Callable
from functools import partial
from pathlib import Path

from fclogr.cli.base import Command, InvalidArgumentError

LOG = logging.getLogger(__name__)


class Syncer(Command):
    """
    Copy a specfile sans the changelog entries.
    """

    def __init__(self, inp: list[Path], out: list[Path]) -> None:
        if inp == out:
            raise InvalidArgumentError("Input and output are the same file")
        self.inp: typing.TextIO = inp[0].open()
        self.out: typing.TextIO = out[0].open("r+")
        self._cleanup = [partial(self.inp.close), partial(self.out.close)]

    @classmethod
    def make_parser(
        cls,
        parser_func: Callable = argparse.ArgumentParser,
        standalone: bool = False,
        **kwargs,
    ) -> argparse.ArgumentParser:
        kwargs.setdefault("description", cls.__doc__)
        if not standalone:
            kwargs.setdefault("help", cls.__doc__)
        parser = parser_func(**kwargs)
        parser.add_argument("inp", nargs=1, type=Path)
        parser.add_argument("out", nargs=1, type=Path)
        return parser

    def _get_out_changelog(self) -> tuple[str | None, list[str]]:
        in_changelog: bool = False
        release: str | None = None
        lines: list[str] = []
        for line in self.out:
            if not release and line.startswith("Release:"):
                release = line
                continue
            if line.strip() == "%changelog":
                in_changelog = True
            if in_changelog:
                lines.append(line)
        self.out.seek(0)
        return release, lines

    def run(self) -> int:
        release, clog = self._get_out_changelog()
        for line in self.inp:
            if release and line.startswith("Release:"):
                self.out.write(release)
            elif clog and line.strip() == "%changelog":
                self.out.writelines(clog)
                break
            else:
                self.out.write(line)
        self.out.truncate()
        return 0
