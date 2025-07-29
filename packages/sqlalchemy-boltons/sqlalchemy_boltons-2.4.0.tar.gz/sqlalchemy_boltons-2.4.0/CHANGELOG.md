# Changelog

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [Unreleased]

## [2.4.0] - 2025-07-15

### Added

- `core`: Add utility function `count1()` for producing SQL `COUNT(1)`.
- `reset`: Add `install_reset_auto()` for installing best-effort-by-default connection reset hooks.
- `temporary`: Add `with temporary_table(): ...` for creating a temporary table that is automatically dropped at the
  end of a `with` block.

## [2.3.0] - 2025-07-11

### Changed

- `orm`: Provide `IdKey.get_one()` even on SQLAlchemy 1.4 even though `Session.get_one()` is absent.

## [2.2.0] - 2025-07-10

### Changed

- `orm`: Restore SQLAlchemy 1.4 compatibility by fixing an import.

### Added

- `orm`: Add class `IdKey` which is a simple and convenient wrapper around `Session.identity_key` and `Session.get`.

## [2.1.0] - 2025-06-30

### Added

- `orm`: Specifying the join conditions on both sides of an ORM relationship is tiresome. Add `Relationships` class
  to automate that process.

## [2.0.1] - 2025-06-28

### Added

- `orm`: Add self-referential tables to test cases.

## [2.0.0] - 2025-06-28

### Added

- `orm`: Add module for elegantly extracting the filter condition out of an ORM relationship.

## [1.1.0] - 2025-03-11

### Changed

- `sqlite`: Use an unlimited-size QueuePool by default.

## [1.0.1] - 2025-02-22

### Changed

- Improve the documentation.

## [1.0.0] - 2025-02-22

### Added

- New module `sqlalchemy_boltons.sqlite` to customize transaction, foreign key enforcement, and journal mode settings.

## [0.0.0] - 1970-01-01

### Added

- This is an example entry.
- See below for the other types of changes.

### Changed

- Change in functionality.

### Deprecated

- Feature that will be removed soon.

### Removed

- Feature that is now removed.

### Fixed

- Bug that was fixed.

### Security

- Security vulnerability notice.
