# SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import argparse
import datetime as dt
import functools
import logging
import shutil
import subprocess
import sys
import tarfile
import tempfile
from collections.abc import Callable
from contextlib import suppress
from pathlib import Path
from typing import TYPE_CHECKING

import pygit2
import specfile as sfile
from specfile import options

from .._util import escape_percentage
from .base import Command, InvalidArgumentError

if TYPE_CHECKING:
    from _typeshed import StrOrBytesPath

LOG = logging.getLogger(__name__)


class GitLogEntry:
    def __init__(
        self,
        *,
        commit: pygit2.Commit,
        baseversion: str,
        pre: bool,
        index: str | int = 1,
    ):
        self.commit = commit
        self.baseversion = baseversion
        self.pre = pre
        self.index = index

    @property
    def message(self) -> list[str]:
        message = self.commit.message.splitlines()
        # --allow-empty-message
        if not message:
            message = ["bump"]
        return ["- " + escape_percentage(message[0])]

    @property
    def author(self) -> str:
        return f"{self.commit.author.name} <{self.commit.author.email}>"

    @property
    def date(self) -> dt.date:
        # Use UTC date
        timestamp = dt.datetime.fromtimestamp(
            self.commit.commit_time, tz=dt.timezone.utc
        )
        return timestamp.date()

    @property
    def version(self) -> str:
        return "{ref}{sep}{num}.{date:%Y%m%d}.{hash}".format(
            ref=self.baseversion,
            sep="~" if self.pre else "^",
            num=self.index,
            date=self.date,
            hash=self.commit.short_id,
        )

    @property
    def evr(self) -> str:
        return self.version + "-1"

    @property
    def entry(self) -> sfile.changelog.ChangelogEntry:
        return sfile.changelog.ChangelogEntry.assemble(
            self.date, self.author, self.message, self.evr
        )

    def add_to_clog(self, clog: sfile.changelog.Changelog) -> None:
        if self.entry not in clog:
            clog.append(self.entry)


class DevEntries(Command):
    baseversion: str
    pre: bool

    def __init__(
        self,
        *,
        specpath: Path | None,
        outdir: Path,
        stdout: bool = False,
        archive: bool,
        baseversion: str | None,
        pre: str | None,
        evr_only: bool = False,
    ) -> None:
        self.specpath = self._v_specpath(specpath)

        self.outdir: Path = outdir
        if not self.outdir.is_dir():
            raise InvalidArgumentError(f"--outdir '{self.outdir}' is not a directory")

        self.stdout: bool = stdout

        self.archive: bool = archive

        self.git_path: Path = Path.cwd()

        try:
            self.spec = sfile.Specfile(self.specpath)
        except sfile.exceptions.SpecfileException as err:
            raise InvalidArgumentError(f"Failed to load specfile: {err}") from None

        try:
            self.repository = pygit2.Repository(str(self.git_path))
        except pygit2.GitError:
            raise InvalidArgumentError(
                f"{self.git_path} is not in a git repository"
            ) from None
        self._guess_last_ref(baseversion, pre)

        self.evr_only: bool = evr_only

        self.last_entry: GitLogEntry | None = None

    @classmethod
    def make_parser(
        cls, parser_func: Callable = argparse.ArgumentParser, standalone=False, **kwargs
    ) -> argparse.ArgumentParser:
        del standalone
        parser = parser_func(**kwargs)
        parser.add_argument("specpath", nargs="?", type=Path)
        parser.add_argument("-r", "--last-ref", dest="baseversion", metavar="LAST_REF")
        parser.add_argument("--pre")
        parser.add_argument("-o", "--outdir", default=Path.cwd(), type=Path)
        parser.add_argument("--stdout", action="store_true")
        parser.add_argument("-A", "--archive", action="store_true")
        parser.add_argument(
            "--evr-only",
            action="store_true",
            help="Print out the generated evr and exit",
        )
        return parser

    def _guess_last_ref(self, baseversion: str | None, pre: str | None) -> None:
        self.pre = bool(pre)
        if not baseversion:
            try:
                baseversion = self.repository.describe(  # type: ignore[attr-defined]
                    self.repository.head,
                    abbreviated_size=0,
                    describe_strategy=pygit2.GIT_DESCRIBE_TAGS,  # type: ignore[attr-defined]
                )
            except pygit2.GitError:
                self.pre = True
                self.baseversion = pre or self.spec.version
                self.last_ref_hash = next(
                    self.repository.walk(
                        self.repository.head.target, pygit2.GIT_SORT_REVERSE  # type: ignore[attr-defined]
                    )
                ).id
                return

        if TYPE_CHECKING:
            assert isinstance(baseversion, str)  # satisfy mypy
        try:
            ref = self.repository.revparse_single(baseversion)
        except KeyError:
            raise InvalidArgumentError(f"Invalid baseversion {baseversion!r}") from None

        self.last_ref_hash = (
            ref.target  # pyright: ignore[reportAttributeAccessIssue]
            if hasattr(ref, "target")
            else ref.id
        )
        if pre:
            self.baseversion = pre
        elif isinstance(ref, pygit2.Tag):
            self.baseversion = baseversion.lstrip("v")
        else:
            self.baseversion = baseversion

    def write_spec(self) -> None:
        content = str(self.spec)
        if self.stdout:
            sys.stdout.write(content)
            return None
        out = self.outdir.joinpath(self.specpath.name)
        try:
            out.write_text(content)
        except OSError as err:
            sys.exit(f"Failed to output specfile to {out}: {err}")

    def add_entries(self) -> None:
        walker = self.repository.walk(
            self.repository.head.target, pygit2.GIT_SORT_REVERSE  # type: ignore[attr-defined]
        )
        walker.hide(self.last_ref_hash)
        has_autochangelog = self.spec.has_autochangelog
        with self.spec.changelog() as changelog:
            assert changelog is not None
            if has_autochangelog:
                changelog.clear()
                with suppress(AttributeError):
                    changelog._predecessor.clear()
                self.spec.release = "1"
            for index, commit in enumerate(walker):
                self.last_entry = GitLogEntry(
                    commit=commit,
                    index=index + 1,
                    baseversion=self.baseversion,
                    pre=self.pre,
                )
                self.last_entry.add_to_clog(changelog)

    def create_archive(self, nv: str):
        with tarfile.open(self.outdir / f"{nv}.tar.gz", "w:gz") as tf:
            self.repository.write_archive(  # type: ignore[attr-defined]
                self.repository.head.target, tf, prefix=f"{nv}/"
            )

    def _reference_archive(self, nv: str) -> None:
        archive_name = nv + ".tar.gz"
        with self.spec.sources() as sources:
            sources[0].location = archive_name
        with self.spec.prep() as prep:
            assert prep is not None
            for name in ("autosetup", "setup"):
                if "%" + name not in prep:
                    continue
                macro = getattr(prep, name)
                del macro.options.n
                # Clear forgesetupargs
                tokens = getattr(macro.options, "_tokens", None)
                if tokens is None:
                    break
                for idx, token in enumerate(tokens):
                    if (
                        "forgesetupargs" in token.value
                        and token.type == options.TokenType.DEFAULT
                    ):
                        del tokens[idx]
                        break
                break

    def run(self) -> int:
        self.add_entries()
        version = self.last_entry.version if self.last_entry else self.spec.version
        if self.evr_only:
            print(version)
            return 0
        if self.last_entry:
            self.spec.set_version_and_release(version, "1")
        nv = f"{self.spec.expanded_name}-{self.spec.expanded_version}"
        if self.archive:
            self.create_archive(nv)
            self._reference_archive(nv)
        self.write_spec()
        return 0


class DevSRPM(DevEntries):
    def __init__(
        self,
        *,
        specpath: Path | None,
        baseversion: str | None,
        pre: str | None,
        # Unique
        srpm_outdir: Path,
        keep: bool,
        clean_srpms: bool,
        # Unused
        evr_only: bool = False,  # noqa: ARG002
    ) -> None:
        self.keep: bool = keep
        self.srpm_outdir = srpm_outdir
        self.clean_srpms = clean_srpms
        if self.keep:
            outdir = self.srpm_outdir
        else:
            outdir = Path(tempfile.mkdtemp())
            self.cleanup.append(
                # mypy doesn't like the partial
                functools.partial(shutil.rmtree, outdir, ignore_errors=True)  # type: ignore[misc]
            )

        super().__init__(
            specpath=specpath,
            baseversion=baseversion,
            outdir=outdir,
            pre=pre,
            archive=True,
            stdout=False,
        )

    def run(self) -> int:
        if r := super().run():
            return r
        try:
            self.build_srpm()
        except subprocess.CalledProcessError as err:
            LOG.error("Failed to run: %s", err.cmd)
            return err.returncode
        if self.clean_srpms:
            for file in self.srpm_outdir.glob(f"{self.spec.expanded_name}-*.src.rpm"):
                if self.spec.expanded_version not in file.name:
                    LOG.debug("Removing old SRPM %r", str(file))
                    file.unlink()
        return 0

    def build_srpm(self) -> subprocess.CompletedProcess:
        defines = {
            # "_topdir": self.outdir,
            "_sourcedir": self.outdir,
            "_specdir": self.outdir,
            "_srcrpmdir ": self.srpm_outdir,
        }
        cmd: list[StrOrBytesPath] = [
            "rpmbuild",
            "-bs",
            self.outdir / self.specpath.name,
        ]
        for name, value in defines.items():
            cmd.extend(("-D", f"{name} {value}"))
        LOG.info("Building SRPM: %s", cmd)
        proc = subprocess.run(cmd, check=True)
        return proc

    @classmethod
    def make_parser(
        cls, parser_func: Callable = argparse.ArgumentParser, standalone=False, **kwargs
    ) -> argparse.ArgumentParser:
        del standalone
        parser = parser_func(**kwargs)
        parser.add_argument("specpath", nargs="?", type=Path)
        parser.add_argument("-r", "--last-ref", dest="baseversion", metavar="LAST_REF")
        parser.add_argument("--pre")
        parser.add_argument(
            "-o",
            "--outdir",
            default=Path.cwd(),
            type=Path,
            dest="srpm_outdir",
            metavar="OUTDIR",
        )
        parser.add_argument(
            "--clean",
            action="store_true",
            help="Cleanup old SRPMs in --outdir",
            dest="clean_srpms",
        )
        parser.add_argument("-k", "--keep", action="store_true")
        return parser
