NEWS
======

## 0.10.0 - 2025-07-16 <a id='0.10.0'></a>

- dev_entries: remove `%autochangelog` when generating our own changelog entries

## 0.9.0 - 2024-09-19 <a id='0.9.0'></a>

### Added

- dev_entries: support non-annotated tags.
  Previously, the `dev-entries` and `dev-srpm` commands would traceback when
  the repository used non-annotated/lightweight tags.

### Changed

- dev_entries: default to specfile Version: when no tags exist.
  If no tags exist in the repo, fclogr now defaults to the value of the
  Version: tag instead of `0.1.0` as the base version to use before appending
  '~' and the snapshot information.

## 0.8.0 - 2024-03-03 <a id='0.8.0'></a>

### Added

- dev-entries: remove `%{forgesetupargs}` from `%setup` command in `%prep`

## 0.7.0 - 2024-03-02 <a id='0.7.0'></a>

### Fixed

- bump: fix regression for forge macros packages that do not use the
  `%forgeversion` feature

## 0.6.0 - 2024-02-29 <a id='0.6.0'></a>

### Added

- all: declare support for Python 3.12
- bump: support new `%{forgeversion}` `%version0` macro
- dev-entries: add `--evr-only` flag

## 0.5.0 - 2023-06-21 <a id='0.5.0'></a>

- dev-srpm and dev-spec - escape percentage signs in commit messages

## 0.4.0 - 2023-06-20 <a id='0.4.0'></a>

- bump - preserve macros when updating Version and Release
- bump - support specfiles with `%include` statements
- bump - properly escape percentage signs
- bump - use relative paths in logging statements
- RPM package - remove dependency on rpmdevtools

## 0.3.1 - 2023-04-15 <a id='0.3.1'></a>

Fixed:

- fix README markdown syntax error

## 0.3.0 - 2023-04-15 <a id='0.3.0'></a>

### Added

- add bump subcommand
- add provisional and untested `--entry-only` option to `dev-srpm` subcommand
- add RPM specfile
- add NEWS.md

### Fixed

- improve CLI exception handling
- sync subcommand: fix changelog preservation and truncate file

## 0.2.0 - 2022-03-18 <a id='0.2.0'></a>

### Added

- add --clean flag to `dev-srpm` subcommand
- add `sync` subcommand

### Fixed

- improve error handling and make `--last-ref` optional
