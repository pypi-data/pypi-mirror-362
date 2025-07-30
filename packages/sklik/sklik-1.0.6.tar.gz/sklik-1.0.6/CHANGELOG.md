# Change Log
All notable changes to this project will be documented in this file.
 
The format is based on [Keep a Changelog](http://keepachangelog.com/).

## [1.0.6] - 2025-07-16

### Added
- Support for longer period reports
- Improved data handling efficiency
- Added example_dataframe.py to demonstrate saving report results to pandas DataFrame

### Changed
- Updated dependencies, including numpy version
- Restricted max interval check to daily granularity

### Fixed
- Fixed pagination issue for zero total_count
- Fixed filters pagination

## [0.1.4] - 2024-01-21 
 
### Added

### Changed
- Refactor 'load_page' method and add '_load_raw_page' method.
### Fixed

## [0.1.3] - 2024-01-20

### Added

### Changed
- Make 'fields' parameter mandatory in 'create_report' function.
- Update sklik_request method call in SklikApi.
### Fixed

## [0.1.0] - 2023-12-09
Initial version.