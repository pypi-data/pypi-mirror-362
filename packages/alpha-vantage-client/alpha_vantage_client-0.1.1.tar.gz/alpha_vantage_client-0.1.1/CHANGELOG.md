# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to
[Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.1] - 2024-07-14

### Fixed

- **Intelligent Defaults**: Fixed critical bug where global defaults were
  applied to all endpoints regardless of validation rules
  - Commodities endpoints (sugar, wheat, etc.) now work without specifying
    interval
  - Economic indicators (GDP, CPI, etc.) now work without specifying interval
  - Time series and technical indicators still use appropriate defaults
  - Invalid parameters are properly rejected with clear error messages

### Added

- **CLI Interface**: Added command-line interface with `alpha-vantage` command
  - `alpha-vantage list` - List available endpoints with filtering options
  - `alpha-vantage query` - Query specific endpoints with parameters
  - Support for pretty-printed JSON output
- **Enhanced Documentation**: Comprehensive README with examples and usage
  patterns
- **Better Error Handling**: Clear validation error messages with valid options

### Improved

- **Parameter Validation**: Smarter default application based on
  endpoint-specific validation rules
- **Developer Experience**: Better endpoint discovery and filtering capabilities
- **Code Quality**: Improved type hints and error handling throughout

### Technical Details

- Defaults are now applied intelligently only if they pass endpoint validation
- CLI supports both environment variables and command-line arguments for API
  keys
- All 111+ endpoints are now properly supported with appropriate defaults

## [0.1.0] - 2024-07-14

### Added

- Initial release of Alpha Vantage Client
- Comprehensive support for all Alpha Vantage API endpoints
- Configuration-driven design with default parameters
- Support for stocks, forex, crypto, commodities, economic indicators, and Alpha
  Intelligence
- Built-in endpoint discovery and filtering
- Type safety with full type hints
- Developer-friendly output formatting
