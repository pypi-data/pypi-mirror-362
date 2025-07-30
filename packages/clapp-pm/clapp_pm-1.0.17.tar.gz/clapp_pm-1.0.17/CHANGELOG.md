# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-01-15

### Added
- Initial release of clapp package manager
- Cross-language support for Python and Lua applications
- Modern GUI interface using Flet framework
- Command-line interface with comprehensive commands
- Package manifest system with JSON-based configuration
- Dependency resolution and validation
- Remote package repository support via GitHub
- App Store GUI with package browsing and installation
- Developer tools for scaffolding, publishing, and validation
- System tools for diagnostics and maintenance
- Settings management with theme support
- Comprehensive error handling and user feedback
- PyPI packaging support

### Features
- **Core Functionality:**
  - Install, uninstall, and run applications
  - List and manage installed packages
  - Validate package manifests and dependencies
  - Clean system and temporary files

- **GUI Interface:**
  - Dashboard with installed apps management
  - App Store with remote package browsing
  - Developer tools for app creation and publishing
  - System tools for diagnostics and maintenance
  - Settings panel with theme and configuration management

- **CLI Interface:**
  - Full command-line support for all operations
  - Comprehensive help system
  - Environment checking and diagnostics
  - Package validation and publishing tools

- **Package System:**
  - JSON-based manifest files
  - Dependency resolution
  - Version management
  - Category and tagging support
  - Multi-language support (Python, Lua)

- **Developer Tools:**
  - App scaffolding with templates
  - Package validation and publishing
  - Manifest generation and validation
  - System diagnostics and health checks

### Technical Details
- Python 3.8+ compatibility
- Flet-based modern GUI
- Cross-platform support (Windows, macOS, Linux)
- GitHub-based package repository
- Semantic versioning
- Comprehensive error handling
- Threaded operations for GUI responsiveness

### Dependencies
- flet>=0.21.0 (GUI framework)
- typing-extensions>=4.0.0 (Python <3.10 compatibility)

### Installation
```bash
pip install clapp
```

### Usage
```bash
# Command line
clapp list
clapp run my-app
clapp install package-url

# GUI
clapp gui
```

## [Unreleased]

### Planned Features
- Lua application support enhancement
- Plugin system for custom commands
- Advanced dependency resolution
- Package signing and verification
- Automated testing framework
- Documentation website
- Package statistics and analytics
- Multi-language GUI support 