# SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
#
# SPDX-License-Identifier: GPL-2.0-or-later


from __future__ import annotations

import argparse
import logging
import re
import subprocess
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

import specfile
import specfile.changelog
import specfile.macro_definitions

from fclogr._util import escape_percentage
from fclogr.cli.base import Command, InvalidArgumentError

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath

# https://pagure.io/fedora-infra/rpmautospec/blob/edf18a1967f05253f937aa93ea90209459d18695/f/rpmautospec/misc.py#_11
AUTORELEASE_RE = re.compile(
    r"%(?:autorelease(?:\s|$)|\{\??autorelease(?:\s+[^\}]*)?\})"
)

PRE_REL_MATCHER = re.compile(r"^(0\.)(\d+)(.*)")
REL_MATCHER = re.compile(r"^(\d+)(.*)")
POST_REL_MATCHER = re.compile(r"^([^\d]+\.)(\d+)($)")

RELEASE_PATTERNS: tuple[re.Pattern[str], ...] = (
    PRE_REL_MATCHER,
    REL_MATCHER,
    POST_REL_MATCHER,
)

LOG = logging.getLogger(__name__)


class Bumper(Command):
    """
    Bump the release and changelog of a specfile.
    """

    def __init__(
        self,
        *,
        specpath: Path | None,
        comment: list[str] | None,
        version: str | None,
        entry_only: bool,
        commit: bool,
        gpg_sign: bool,
    ) -> None:
        self.specpath: Path = self._v_specpath(specpath)
        self.version: str | None = version
        self.entry_only: bool = entry_only
        self.commit: bool = gpg_sign or commit
        self.gpg_sign: bool = gpg_sign
        try:
            self.spec = specfile.Specfile(self.specpath, force_parse=True)
        except specfile.exceptions.SpecfileException as err:
            LOG.debug("Failed to load specfile", exc_info=True)
            raise InvalidArgumentError(f"Failed to load specfile: {err}") from None
        comment = comment or [f"Update to {self.version}." if self.version else "bump"]
        self.comment: list[str] = [
            escape_percentage(c if c.startswith("- ") else "- " + c) for c in comment
        ]
        if entry_only and version:
            raise InvalidArgumentError("--entry-only and --new are mutually exclusive.")

    def _write_spec(self) -> int | str:
        try:
            self.specpath.write_text(str(self.spec), encoding="utf-8")
        except OSError as err:
            return f"Failed to output specfile to {self.specpath}: {err}"
        return 0

    def _evr(self) -> str:
        return self.spec.expand("%{?epoch:%{epoch}:}%{version}-%{release}")

    def _bump_version(self, version: str) -> None:
        macros: specfile.macro_definitions.MacroDefinitions
        with self.spec.macro_definitions() as macros:
            if "version0" in macros:
                self._update_macro("version0", version, macros)
                return
        self.spec.update_tag("Version", version)

    def run(self) -> int | str:
        uses_autorelease: bool = False
        old_evr = self._evr()

        if self.version:
            self._bump_version(self.version)

        if self.entry_only:
            pass
        elif any(AUTORELEASE_RE.search(line) for line in str(self.spec).splitlines()):
            uses_autorelease = True
            LOG.info("%s uses %%autorelease. Preserving Release.", self.specpath)
        elif self.version:
            self.spec.release = "1"
        else:
            self._handle_release()

        if not uses_autorelease:
            LOG.info("%s: bumped %s -> %s", self.specpath, old_evr, self._evr())
        elif self.version:
            LOG.info(
                "%s: bumped Version to %s", self.specpath, self.spec.expanded_version
            )

        if not self.spec.has_autochangelog:
            if uses_autorelease:
                LOG.warning(
                    "%s uses %%autorelease, but it does not use %%autochangelog."
                    " We're adding a changelog entry,"
                    " but its EVR part may be incorrect.",
                    self.specpath,
                )
            self.spec.add_changelog_entry(self.comment)
        else:
            LOG.info("%s uses %%autochangelog. Preserving %%changelog.", self.specpath)
        if r := self._write_spec():
            return r
        if self.commit:
            self.git_commit(
                allow_empty=uses_autorelease and self.spec.has_autochangelog
            )
        return 0

    def _update_macro(
        self,
        name: str,
        value: str,
        macros: specfile.macro_definitions.MacroDefinitions,
    ) -> None:
        macro = macros.get(name)
        macro.body = value

    def _handle_release(self) -> None:
        baserelease = self.spec.expand("%{baserelease}")
        if baserelease != "%{baserelease}":
            with self.spec.macro_definitions() as macros:
                self._update_macro(
                    "baserelease", self._handle_release2(baserelease), macros
                )
        else:
            self.spec.release = self._handle_release2(self.spec.release)

    @staticmethod
    def _handle_release2(value: str) -> str:
        for pattern in RELEASE_PATTERNS:
            if match := pattern.match(value):
                groups = list(match.groups())
                groups[-2] = str(int(groups[-2]) + 1)
                return "".join(groups)
        return value + ".1"

    def _get_git_messages(self) -> list[str]:
        args: list[str] = []
        for entry in self.comment:
            entry = re.sub("^- ", "", entry)
            args.extend(("-m", entry))
        return args

    def _git(
        self, cmd: Sequence[StrOrBytesPath], *args, **kwargs
    ) -> subprocess.CompletedProcess:
        cmd = ["git", *cmd]
        LOG.info("Running %s", cmd)
        return subprocess.run(cmd, *args, **kwargs)  # noqa: PLW1510

    def git_commit(self, allow_empty: bool = False) -> None:
        args: list[str | Path] = ["add", self.specpath]
        self._git(args, check=True, stdout=subprocess.DEVNULL)
        args = ["commit", *self._get_git_messages()]
        if allow_empty:
            args.append("--allow-empty")
        if self.gpg_sign:
            args.append("--gpg-sign")
        self._git(args, check=True)

    @classmethod
    def make_parser(
        cls, parser_func: Callable = argparse.ArgumentParser, standalone=False, **kwargs
    ) -> argparse.ArgumentParser:
        kwargs["description"] = cls.__doc__
        if not standalone:
            kwargs["help"] = cls.__doc__
        parser = parser_func(**kwargs)
        parser.add_argument("-c", "--comment", action="append")
        parser.add_argument(
            "--new", dest="version", help="Bump Release to 1 and change Version"
        )
        parser.add_argument(
            "-M",
            "--entry-only",
            action="store_true",
            # help="Don't bump Release",
            help=argparse.SUPPRESS,
        )
        parser.add_argument(
            "--commit", action="store_true", help="Commit the specfile bump"
        )
        parser.add_argument(
            "-S",
            "--gpg-sign",
            action="store_true",
            help="Sign the specfile bump commit." " Implies --commit.",
        )
        parser.add_argument("specpath", nargs="?", type=Path)
        return parser
