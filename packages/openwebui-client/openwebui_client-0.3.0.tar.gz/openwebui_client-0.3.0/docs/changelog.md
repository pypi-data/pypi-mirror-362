# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-07-17

### Added
- Added models functionality
- Added comprehensive documentation for the models functionality

## [0.2.1] - 2025-07-05

### Fixed
- Fixed type error in `files.py` related to multipart form data
- Updated type annotations to use `Union[]` instead of pipe operator (`|`) for better compatibility
- Increased HTTP request timeout from 45 to 60 seconds

## [0.2.0] - 2025-06-15

### Added
- Support for function calling and tools
- Tool registry for automatic function registration
- Extended completions class with file support

## [0.1.0] - 2025-05-27

### Added
- Initial release
- Basic client functionality
- Support for file uploads
- Support for file attachments in chat completions
