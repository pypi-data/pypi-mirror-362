# Changelog

All notable changes to MusicGen Unified will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2024-01-13

### Added
- Complete rewrite focused on simplicity and functionality
- GPU optimization with mixed precision and flash attention
- Extended generation for >30s audio using intelligent segmentation
- Batch processing from CSV files
- Prompt engineering for better results
- Simple web UI for easy access
- REST API with FastAPI
- Docker support for easy deployment
- AWS deployment scripts and CloudFormation template
- Comprehensive test suite

### Changed
- Consolidated from 343 files to focused implementation
- Removed all non-working features
- Simplified architecture - no microservices
- Focus on instrumental music only

### Removed
- VocalGen (doesn't work with MusicGen)
- Complex microservices architecture
- Unnecessary abstraction layers
- Non-essential features

### Fixed
- MP3 export reliability
- Memory management for long generations
- Progress reporting accuracy

## [1.2.0] - 2024-01-12

### Added
- VocalGen experimental feature (later removed)
- Advanced audio processing

### Fixed
- CI/CD pipeline issues
- SQLAlchemy dependency

## [1.1.2] - 2024-01-11

### Fixed
- Confusing UX when MP3 conversion fails
- Better error messages

## [1.1.1] - 2024-01-11

### Fixed
- MP3 filename handling crash
- Soundfile format errors

## [1.1.0] - 2024-01-10

### Added
- Extended generation (>30s)
- Batch processing from CSV
- MP3 output support
- Progress bars for long operations

## [1.0.0] - 2024-01-09

### Added
- Initial release
- Basic text-to-music generation
- Command-line interface
- PyPI package

## [0.1.0] - 2024-01-08

### Added
- Proof of concept
- Minimal working implementation