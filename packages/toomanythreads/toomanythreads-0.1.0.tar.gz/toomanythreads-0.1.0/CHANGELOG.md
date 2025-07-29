# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial development

## [0.1.0] - 2025-7-14

### Added
- Singleton-based thread management system
- Auto-registration and unregistration of threads
- Verbose logging support with loguru integration
- Dynamic mixin system for thread enhancement
- Thread deduplication to prevent duplicate instances
- Daemon thread support by default
- Comprehensive type hints and documentation
- Thread lifecycle management
- Error handling for mixin application

### Features
- `ManagedThread` decorator/factory for creating managed threads
- `_ThreadManager` singleton for centralized thread management
- Toggleable verbose logging
- Thread lookup by name
- Automatic cleanup on thread completion

### Dependencies
- loguru >= 0.6.0
- singleton-decorator >= 1.0.0
- Python >= 3.8