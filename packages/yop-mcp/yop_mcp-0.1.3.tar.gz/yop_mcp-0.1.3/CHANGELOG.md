# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.3] - 2025-01-XX

### Changed
- **BREAKING**: Updated Python requirement from 3.13+ to 3.10+ for better compatibility
- Updated Python version badge in README from 3.13+ to 3.10+
- Updated CI/CD workflows to test against Python 3.10, 3.11, and 3.12
- Updated development tools configuration to target Python 3.10
- Fixed pre-commit configuration argument formatting

### Fixed
- Resolved installation issues for users with Python 3.10-3.12
- Improved package compatibility with broader Python ecosystem

## [Unreleased]

### Added
- Comprehensive README documentation with badges and detailed usage instructions
- Complete GitHub Actions CI/CD pipeline with modern workflows
- Code quality tools configuration (Black, isort, flake8, mypy, pylint)
- Security scanning with Bandit and Trivy
- Pre-commit hooks for code quality enforcement
- Comprehensive test suite with pytest
- Code coverage reporting
- Dependency review and security scanning
- Enhanced pyproject.toml configuration with development dependencies

### Changed
- Updated all GitHub Actions to latest versions (v4)
- Migrated from pip to uv package manager for better performance
- Improved error handling and logging
- Enhanced documentation structure and content

### Fixed
- Fixed GitHub Actions compatibility issues
- Improved error messages and user feedback
- Enhanced security configurations

### Security
- Added security scanning with multiple tools
- Implemented dependency vulnerability checking
- Added pre-commit security hooks

## [0.1.2] - 2024-01-XX

### Added
- Initial release of YOP MCP Server
- 10 core tool functions for YOP platform integration:
  - `yeepay_yop_overview()` - Platform overview and specifications
  - `yeepay_yop_product_overview()` - Product capabilities overview
  - `yeepay_yop_product_detail_and_associated_apis()` - Product details and APIs
  - `yeepay_yop_api_detail()` - Detailed API documentation
  - `yeepay_yop_java_sdk_user_guide()` - Java SDK usage guide
  - `yeepay_yop_sdk_and_tools_guide()` - SDK and tools guide
  - `yeepay_yop_link_detail()` - Link content retrieval
  - `yeepay_yop_gen_key_pair()` - Cryptographic key pair generation
  - `yeepay_yop_download_cert()` - CFCA certificate download
  - `yeepay_yop_parse_certificates()` - Certificate parsing utilities
- Support for RSA and SM2 cryptographic algorithms
- HTTP utilities with HTTP/2 support
- Certificate management tools
- MCP (Model Context Protocol) server implementation
- Basic error handling and fallback mechanisms

### Dependencies
- httpx[http2] >= 0.28.1 for HTTP client functionality
- mcp[cli] >= 1.6.0 for MCP server implementation
- gmssl >= 3.2.2 for SM2 cryptographic support
- cryptography >= 42.0.0 for RSA cryptographic operations

### Documentation
- Basic README with installation and usage instructions
- Function documentation with examples
- Configuration examples for Cursor and Claude Desktop

---

## Release Notes

### Version 0.1.2
This is the initial release of the YOP MCP Server, providing a comprehensive set of tools for integrating with the YeePay Open Platform (YOP). The server implements the Model Context Protocol (MCP) to enable seamless integration with AI development tools like Claude Desktop and Cursor.

**Key Features:**
- **Platform Integration**: Direct access to YOP documentation, product information, and API specifications
- **Cryptographic Support**: Full support for both RSA and SM2 algorithms for key generation and certificate management
- **Developer-Friendly**: Easy setup with uv package manager and comprehensive documentation
- **AI Tool Integration**: Native MCP support for popular AI development environments

**Getting Started:**
1. Install dependencies with `uv sync`
2. Run the server with `uv run main.py`
3. Configure your AI tool to connect to the MCP server

For detailed installation and usage instructions, see the [README](README.md).

**Support:**
- Documentation: [YeePay Open Platform](https://open.yeepay.com/)
- Issues: [GitLab Issues](http://gitlab.yeepay.com/yop/yop-mcp/-/issues)
- MCP Protocol: [Model Context Protocol](https://modelcontextprotocol.io/)
