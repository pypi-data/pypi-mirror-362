# SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import abc
import argparse
import logging
from collections.abc import Callable
from pathlib import Path
from typing import Any

fmt = "{levelname}:{name}: {message}"
logging.basicConfig(format=fmt, style="{")
LOG = logging.getLogger("fclogr")


class InvalidArgumentError(Exception):
    """
    A problem parsing or validating a command line argument
    """


class Command(abc.ABC):
    _cleanup: list[Callable[[], Any]]

    @classmethod
    @abc.abstractmethod
    def make_parser(
        cls, parser_func: Callable = argparse.ArgumentParser, standalone=False, **kwargs
    ) -> argparse.ArgumentParser: ...

    @abc.abstractmethod
    def run(self) -> str | int: ...

    @property
    def cleanup(self) -> list[Callable[[], Any]]:
        if getattr(self, "_cleanup", None) is None:
            self._cleanup = []
        return self._cleanup

    def _v_specpath(self, path: Path | None = None) -> Path:
        if not path:
            pwd = Path.cwd()
            path = Path(pwd.name + ".spec")
        if not path.is_file() or path.suffix != ".spec":
            raise InvalidArgumentError(f"{path} must exist an end with '.spec'")
        return path
