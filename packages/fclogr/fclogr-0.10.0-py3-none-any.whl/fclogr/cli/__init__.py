# SPDX-FileCopyrightText: 2023 Maxwell G <gotmax@e.email>
#
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Sequence
from subprocess import CalledProcessError

from fclogr.cli.sync import Syncer

from .base import LOG, Command, InvalidArgumentError
from .bump import Bumper
from .dev_entries import DevEntries, DevSRPM


def get_command(argv: Sequence[str] | None = None, **kwargs) -> Command:
    parser = argparse.ArgumentParser(
        description="fclogr is a tool for managing RPM changelogs and updates", **kwargs
    )
    log_group = parser.add_mutually_exclusive_group()
    log_group.add_argument(
        "--debug", action="store_const", dest="log_level", const="DEBUG"
    )
    log_group.add_argument(
        "--ll",
        "--log-level",
        dest="log_level",
        type=lambda t: t.upper(),
        choices=["DEBUG", "INFO"],
    )
    subparsers = parser.add_subparsers(
        title="Subcommands", dest="action", required=True
    )
    for name, cls in COMMANDS.items():
        cls.make_parser(subparsers.add_parser, standalone=False, name=name)

    args = vars(parser.parse_args(argv))
    action = args.pop("action")
    if log_level := args.pop("log_level"):
        level = getattr(logging, log_level)
        LOG.setLevel(level)

    return COMMANDS[action](**args)


def main(argv: Sequence[str] | None = None) -> int | str:
    try:
        command = get_command(argv)
    except InvalidArgumentError as err:
        # sys.exit() in the console_script handles this
        return str(err)
    try:
        r = command.run()
    except CalledProcessError as err:
        print(err, file=sys.stderr)
        r = err.returncode
    except Exception:
        LOG.exception("Unexpected Exception")
        r = 1
    for func in command.cleanup:
        func()
    return r


COMMANDS: dict[str, type[Command]] = {
    "bump": Bumper,
    "dev-entries": DevEntries,
    "dev-srpm": DevSRPM,
    "sync": Syncer,
}
