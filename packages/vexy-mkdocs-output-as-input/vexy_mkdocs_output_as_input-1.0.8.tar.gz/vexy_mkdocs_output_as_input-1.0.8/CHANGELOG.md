# Changelog

All notable changes to vexy-mkdocs-output-as-input will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete documentation pages for getting started, configuration, examples, and API reference
- Additional test cases for edge cases, improving coverage to 91%+
- Proper error handling for missing directories (docs_dir, site_dir)
- Configuration option `include_frontmatter` to control whether YAML frontmatter is included in output files (default: true)
- Configuration option `preserve_links` to convert absolute links to relative paths (default: false)
- Configuration options `minify` and `prettify` for HTML output formatting (mutually exclusive)
- Support for multiple HTML selectors - extract multiple elements in one pass
- Support for CSS selectors in addition to tag names (e.g., `.content`, `#main`)
- CLI tool `mkdocs-output-as-input` for standalone HTML processing
- CLI options for preserving relative links, minifying, and prettifying HTML output
- CLI support for multiple selectors using `--html-element` flag multiple times
- Comprehensive test suite for CLI functionality

### Changed
- Replaced Black formatter with Ruff format in CI workflow
- Enhanced type hints with proper type ignore comments for MkDocs compatibility
- Improved error handling and logging throughout the plugin
- Refactored `build_docs.py` to use proper two-stage MkDocs pipeline:
  1. Source → Intermediate (with plugin capturing HTML)
  2. Intermediate → Final (standard MkDocs build with full Material theme)

### Fixed
- Fixed broken plugin implementation - all methods now properly implemented
- Fixed broken test suite - all tests now passing with proper fixtures
- Fixed mypy type checking errors with appropriate type annotations
- Pre-commit configuration updated to remove conflicting Black formatter
- Documentation build now generates proper MkDocs Material site (not manual HTML)
- Removed duplicate README.md from docs directory

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