# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## v5.12.1 (2025-07-17)

### Fixed

- remove errors in ci

## v5.12.0 (2025-07-17)

### Added

- add changelog to code

## v5.11.1 (2025-07-17)

### Fixed

- improve release workflow changelog creation

## v5.11.0 (2025-07-17)

### Added

- improve release.yml

## v5.10.2 (2025-07-17)

### Fixed

- release.sh

## v5.10.1 (2025-07-16)

### Fixed

- regenerate complete lockfile

## v5.10.0 (2025-07-16)

### Added

- improve release process

### Fixed

- make release.sh executable

## v5.9.0 (2025-07-16)

### Added

- install extra dev group in ci

## v5.8.0 (2025-07-16)

### Added

- install extra groups in ci

### Fixed

- fix ci yml

## v5.7.0 (2025-07-16)

### Added

- **build**: improve the ci workflow

## v5.6.0 (2025-07-16)

### Added

- **build**: use .venv with ci

## v5.5.0 (2025-07-16)

### Added

- fix the ci workflow

## v5.4.0 (2025-07-16)

### Added

- update the git workflow

## v5.3.0 (2025-07-14)

### Added

- update ci workflow

## v5.2.0 (2025-07-14)

### Added

- improve build system

## v5.1.0 (2025-07-14)

### Added

- improve linting and formatting

## v5.0.0 (2025-07-14)

### Added

- implement new project workflow
- store discography metadata in db
- implement artist, album, track creation logic
- add a parsing custom error
- create models to represent fetched data
- avoid no handler warnings
- implement request handler
- add request specific error
- create artist url from name

### Changed

- denote all library methods as private
- improve database and utils structure
- move database initialization into sub file

## v2.2.0 (2025-07-11)

### Added

- implement database structure
- add custom library errors

## v2.1.0 (2025-07-11)

### Added

- add aiohttp as a dependency

## v2.0.0 (2025-07-11)

### BREAKING CHANGE

- Redesigned with improved logging, error handling, storage management, and project structure

### Added

- complete rewrite of lyrically library
