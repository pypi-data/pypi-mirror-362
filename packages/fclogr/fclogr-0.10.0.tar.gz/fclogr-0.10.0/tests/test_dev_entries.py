# Copyright (C) 2024 Maxwell G <maxwell@gtmx.me>
# SPDX-License-Identifier: GPL-2.0-or-later OR MIT

from __future__ import annotations

import datetime
import subprocess
from functools import partial
from pathlib import Path
from shutil import copy2

import git
import pytest
from pytest_mock import MockerFixture

from fclogr.cli import main

GIT_NAME = "Perry The Packager"
GIT_EMAIL = "example@example.com"
dt = partial(datetime.datetime, tzinfo=datetime.timezone.utc)
default_test_filename = Path("package.spec")


def commithash(commit: git.Commit) -> str:
    return commit.binsha.hex()[:7]


@pytest.fixture
def repo_with_specfile(
    request: pytest.FixtureRequest,
    tmp_path: Path,
    test_data: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> git.Repo:
    test_filename = getattr(request, "param", default_test_filename)
    (repo_path := tmp_path / test_filename.with_suffix("")).mkdir()
    copy2(test_data / test_filename, repo_path / test_filename)

    # Make sure git doesn't read existing config
    (tmp_home := tmp_path / "home").mkdir()
    monkeypatch.setenv("HOME", str(tmp_home))
    monkeypatch.delenv("XDG_CONFIG_HOME", False)
    repo = git.Repo.init(repo_path)
    with repo.config_writer() as writer:
        writer.add_value("user", "name", GIT_NAME)
        writer.add_value("user", "email", GIT_EMAIL)
    repo.index.add([test_filename])
    date1 = dt(2023, 10, 10, 0, 0)
    repo.index.commit("init", author_date=date1, commit_date=date1)
    monkeypatch.chdir(repo_path)
    return repo


@pytest.fixture
def repo_tag(repo_with_specfile: git.Repo) -> None:
    repo_with_specfile.create_tag("v1", message="Initial release")


@pytest.fixture
def repo_extra_commits(repo_with_specfile: git.Repo) -> tuple[git.Commit, ...]:
    mkcommit = repo_with_specfile.index.commit
    date1 = dt(2023, 10, 15, 0, 0)
    commit1 = mkcommit("a change", author_date=date1, commit_date=date1)
    date2 = dt(2023, 10, 16, 0, 0)
    commit2 = mkcommit("another change", author_date=date2, commit_date=date2)
    return commit1, commit2


def test_dev_entries_basic(
    test_data: Path,
    repo_with_specfile: git.Repo,
    repo_tag,
    repo_extra_commits: tuple[git.Commit, ...],
) -> None:
    commit1, commit2 = repo_extra_commits
    assert main(["dev-entries", str(default_test_filename)]) == 0
    expected_contents = (
        (test_data / "package-dev_entries_basic.spec")
        .read_text(encoding="utf-8")
        .replace("COMMIT1", commithash(commit1))
        .replace("COMMIT2", commithash(commit2))
    )
    Path("expected.spec").write_text(expected_contents, encoding="utf-8")
    gotten_contents = default_test_filename.read_text(encoding="utf-8")
    assert expected_contents == gotten_contents


def test_dev_entries_no_tag(
    test_data: Path,
    repo_with_specfile: git.Repo,
    repo_extra_commits: tuple[git.Commit, ...],
) -> None:
    commit1, commit2 = repo_extra_commits
    assert main(["dev-entries", str(default_test_filename)]) == 0
    expected_contents = (
        (test_data / "package-dev_entries_no_tag.spec")
        .read_text(encoding="utf-8")
        .replace("COMMIT1", commithash(commit1))
        .replace("COMMIT2", commithash(commit2))
    )
    Path("expected.spec").write_text(expected_contents, encoding="utf-8")
    gotten_contents = default_test_filename.read_text(encoding="utf-8")
    assert expected_contents == gotten_contents


@pytest.mark.parametrize(
    "repo_with_specfile", [Path("package-with-source.spec")], indirect=True
)
def test_dev_srpm(
    test_data: Path,
    repo_with_specfile: git.Repo,
    repo_extra_commits,
    mocker: MockerFixture,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    assert main(["dev-srpm", "package-with-source.spec"]) == 0
    dist = subprocess.check_output(["rpm", "-E", "%{?dist}"], text=True).strip()
    assert Path(f"package-1~2.20231016.aae73bc-1{dist}.src.rpm").is_file()
