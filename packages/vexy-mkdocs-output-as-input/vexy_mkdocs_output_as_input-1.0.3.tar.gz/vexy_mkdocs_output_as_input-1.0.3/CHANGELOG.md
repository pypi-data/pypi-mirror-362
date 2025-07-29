# Changelog

All notable changes to vexy-mkdocs-output-as-input will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.0] - 2025-01-14

### Changed
- **BREAKING**: Migrated to src-layout package structure
- **BREAKING**: Minimum Python version is now 3.9
- Switched from Loguru to standard library logging for better integration
- Modernized packaging with PEP 621 compliant pyproject.toml
- Improved type hints throughout the codebase

### Added
- Comprehensive test suite with >90% coverage
- Pre-commit hooks for code quality
- GitHub Actions CI/CD workflows
- Support for Python 3.9, 3.10, 3.11, and 3.12
- Automated release process with trusted PyPI publishing
- Development documentation in README

### Fixed
- Better error handling for missing files
- Graceful handling of invalid YAML frontmatter
- Improved logging messages for debugging

## [0.1.0] - 2025-01-10

### Added
- Initial release of vexy-mkdocs-output-as-input plugin
- Core functionality to capture HTML output and create cousin Markdown files
- Configurable stage directory for output files
- Configurable HTML element extraction (default: `<main>`)
- Configurable target tag transformation (default: `<article>`)
- Preservation of original YAML frontmatter
- Verbose logging mode for debugging
- Basic documentation and examples

[Unreleased]: https://github.com/vexyart/vexy-mkdocs-output-as-input/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/vexyart/vexy-mkdocs-output-as-input/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/vexyart/vexy-mkdocs-output-as-input/releases/tag/v0.1.0