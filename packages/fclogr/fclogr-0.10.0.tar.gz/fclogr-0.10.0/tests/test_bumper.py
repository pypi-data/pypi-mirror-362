# Copyright (c) 2023 Maxwell G <gotmax@e.email>
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import annotations

import datetime
import subprocess
from collections.abc import Sequence
from pathlib import Path
from shutil import copy2
from unittest import mock

import pytest
import pytest_mock
import specfile
import specfile.changelog
import specfile.macros

from fclogr.cli import Bumper, main

DEFAULT_PACKAGER = "Perry the Packager <perry@example.com>"
DATE_STR = datetime.datetime.now(tz=datetime.timezone.utc).strftime("%a %b %d %Y")


@pytest.mark.parametrize(
    "value,expected",
    [
        # REL_MATCHER
        pytest.param("1", "2", id="simple"),
        pytest.param("33", "34", id="simple double"),
        # PRE_REL_MATCHER
        pytest.param("0.1", "0.2", id="prerel"),
        # POST_REL_MATCHER
        pytest.param("abcdefgh.1", "abcdefgh.2", id="postrel"),
        # fallback
        pytest.param("abcdefgh", "abcdefgh.1", id="fallback"),
    ],
)
def test_bumper_handle_release(value: str, expected: str) -> None:
    assert Bumper._handle_release2(value) == expected


def get_entry_obj(
    evr: str,
    lines: list[str],
    following_lines: list[str],
    date_str: str = DATE_STR,
    packager: str = DEFAULT_PACKAGER,
):
    header = f"* {date_str} {packager} - {evr}"
    return specfile.changelog.ChangelogEntry(header, lines, following_lines)


@pytest.fixture()
def rpm_packager(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("RPM_PACKAGER", DEFAULT_PACKAGER)


INITIAL_ENTRIES = (
    get_entry_obj(
        "1-1",
        ["- Initial package"],
        [],
        "Fri Mar 03 2023",
        "Packager <example@example.com>",
    ),
    get_entry_obj(
        "1-2",
        ["- rebuilt"],
        [""],
        "Fri Mar 03 2023",
        "Packager <example@example.com>",
    ),
)


@pytest.mark.parametrize(
    "args, changelog, version, raw_release, subprocess_calls",
    [
        pytest.param(
            [],
            [*INITIAL_ENTRIES, get_entry_obj("1-3", ["- bump"], [""])],
            "1",
            "3%{?dist}",
            [],
            id="no-arguments",
        ),
        pytest.param(
            ["--new", "3"],
            [*INITIAL_ENTRIES, get_entry_obj("3-1", ["- Update to 3."], [""])],
            "3",
            "1%{?dist}",
            [],
            id="new-version-no-arguments",
        ),
        pytest.param(
            ["--new", "3", "--commit"],
            [*INITIAL_ENTRIES, get_entry_obj("3-1", ["- Update to 3."], [""])],
            "3",
            "1%{?dist}",
            [
                lambda p: mock.call(
                    ["add", p],
                    check=True,
                    stdout=subprocess.DEVNULL,
                ),
                lambda _: mock.call(["commit", "-m", "Update to 3."], check=True),
            ],
            id="new-version-commit",
        ),
        pytest.param(
            ["--comment", "abc"],
            [*INITIAL_ENTRIES, get_entry_obj("1-3", ["- abc"], [""])],
            "1",
            "3%{?dist}",
            [],
            id="comment",
        ),
        pytest.param(
            ["--comment", "%changelog is escaped"],
            [
                *INITIAL_ENTRIES,
                get_entry_obj("1-3", ["- %%changelog is escaped"], [""]),
            ],
            "1",
            "3%{?dist}",
            [],
            id="comment-escape",
        ),
        pytest.param(
            ["--comment", "- abc", "-c", "xyz", "--new", "5", "-S"],
            [*INITIAL_ENTRIES, get_entry_obj("5-1", ["- abc", "- xyz"], [""])],
            "5",
            "1%{?dist}",
            [
                lambda p: mock.call(
                    ["add", p],
                    check=True,
                    stdout=subprocess.DEVNULL,
                ),
                lambda _: mock.call(
                    ["commit", "-m", "abc", "-m", "xyz", "--gpg-sign"], check=True
                ),
            ],
            id="new-version-with-multiple-comments",
        ),
    ],
)
def test_bumper_full(
    # Fixtures
    test_data: Path,
    tmp_path: Path,
    rpm_packager: None,
    mocker: pytest_mock.MockerFixture,
    # Params
    args: Sequence[str],
    changelog: list[specfile.changelog.ChangelogEntry],
    version: str,
    raw_release: str,
    subprocess_calls: Sequence[mock._Call],
):
    subprocess_mock: mock.MagicMock = mocker.patch.object(Bumper, "_git")
    name = "package.2.spec"
    path = tmp_path / name
    copy2(test_data / name, path)
    args = ["bump", *args, str(path)]
    assert main(args) == 0
    specfile.macros.Macros.reinit()

    with specfile.Specfile(path) as spec:
        assert spec.raw_release == raw_release
        assert spec.version == version
        with spec.changelog() as spec_changelog:
            assert spec_changelog is not None
            assert list(spec_changelog) == changelog
    assert subprocess_mock.call_args_list == [call(path) for call in subprocess_calls]


@pytest.mark.parametrize(
    "args,subprocess_calls,version",
    [
        pytest.param([], [], None, id="simple-noop"),
        pytest.param(["--new", "10"], [], "10", id="new"),
        pytest.param(
            ["--new", "10", "--commit"],
            [
                lambda p: mock.call(
                    ["add", p],
                    check=True,
                    stdout=subprocess.DEVNULL,
                ),
                lambda _: mock.call(
                    ["commit", "-m", "Update to 10.", "--allow-empty"], check=True
                ),
            ],
            "10",
            id="new-commit",
        ),
    ],
)
def test_bumper_autospec(
    test_data: Path,
    tmp_path: Path,
    mocker: pytest_mock.MockerFixture,
    # Params
    args: Sequence[str],
    version: str | None,
    subprocess_calls,
) -> None:
    subprocess_mock: mock.MagicMock = mocker.patch.object(Bumper, "_git")
    name = "package-autospec.spec"
    src = test_data / name
    dest = tmp_path / name
    copy2(src, dest)

    args = ["bump", *args, str(dest)]
    assert main(args) == 0
    if version is None:
        assert src.read_text() == dest.read_text()
    else:
        specfile.macros.Macros.reinit()
        with specfile.Specfile(dest) as spec:
            assert spec.expanded_version == version
            spec.update_tag("Version", "1")
            assert spec.expanded_version == "1"
            assert src.read_text() == str(spec)
    assert subprocess_mock.call_args_list == [call(dest) for call in subprocess_calls]


def replace_instance(lines: Sequence[str], match: str, repl: str) -> list[str]:
    lines = list(lines)
    for idx, line in enumerate(lines):
        if match in line:
            line = line.replace(match, repl)
            lines[idx] = line
            break
    return lines


@pytest.mark.parametrize(
    "initial, final, command, replace_date",
    [
        pytest.param(
            "package-forge.spec",
            "package-forge.2.spec",
            ["--new", "0.60.0"],
            "Thu Feb 01 2024",
            id="package-forge",
        ),
        pytest.param(
            "package-forgeversion.spec",
            "package-forgeversion.2.spec",
            ["--new", "0.60.0"],
            "Thu Feb 01 2024",
            id="package-forge",
        ),
    ],
)
def test_bumper_forge_compare(
    test_data: Path,
    tmp_path: Path,
    rpm_packager: None,
    initial: str,
    final: str,
    command: Sequence[str],
    replace_date: str,
) -> None:
    if (
        "forgeversion" in initial
        and subprocess.run(
            ["rpm", "-E", "%{defined forgeversion}"],
            check=False,
            capture_output=True,
            text=True,
        ).stdout.strip()
        == "0"
    ):
        pytest.skip("forgeversion is not supported in RHEL!")
    src = test_data / initial
    dest = tmp_path / initial
    copy2(src, dest)
    final_path = test_data / final
    final_lines = replace_instance(
        final_path.read_text().splitlines(), DATE_STR, replace_date
    )

    args: list[str] = ["bump", str(dest), *command]
    assert main(args) == 0

    dest_lines = replace_instance(dest.read_text().splitlines(), DATE_STR, replace_date)
    assert final_lines == dest_lines
