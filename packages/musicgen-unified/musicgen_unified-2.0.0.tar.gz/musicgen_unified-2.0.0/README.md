# MusicGen Unified - v2.0

[![PyPI version](https://badge.fury.io/py/musicgen-unified.svg)](https://badge.fury.io/py/musicgen-unified)
[![Python](https://img.shields.io/pypi/pyversions/musicgen-unified.svg)](https://pypi.org/project/musicgen-unified/)
[![License](https://img.shields.io/pypi/l/musicgen-unified.svg)](https://github.com/Bright-L01/musicgen-unified/blob/main/LICENSE)
[![CI](https://github.com/Bright-L01/musicgen-unified/actions/workflows/ci.yml/badge.svg)](https://github.com/Bright-L01/musicgen-unified/actions/workflows/ci.yml)
[![Downloads](https://pepy.tech/badge/musicgen-unified)](https://pepy.tech/project/musicgen-unified)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A clean, focused implementation of Facebook's MusicGen for instrumental music generation.

## What This Is

- **Simple**: Just music generation, no unnecessary complexity
- **Fast**: GPU-optimized for 10x realtime generation
- **Practical**: CLI, API, and web interface included
- **Deployable**: One-click AWS deployment

## What This Isn't

- Not for vocal/singing generation (MusicGen doesn't support it)
- Not a microservices architecture (it's a simple tool)
- Not a research framework (it's for practical use)

## Quick Start

```bash
# Install
pip install musicgen-unified

# Generate music
musicgen generate "upbeat jazz piano" --duration 30

# Start web interface
musicgen serve

# Start API
musicgen api
```

## Features

- ✅ Text-to-music generation
- ✅ Extended generation (>30 seconds)
- ✅ Batch processing from CSV
- ✅ GPU acceleration
- ✅ Web interface
- ✅ REST API
- ✅ AWS deployment ready

## Installation

```bash
# Basic installation
pip install musicgen-unified

# With GPU support
pip install musicgen-unified[gpu]

# Development
git clone https://github.com/yourusername/musicgen-unified
cd musicgen-unified
pip install -e ".[dev]"
```

## Usage

### Command Line

```bash
# Basic generation
musicgen generate "smooth jazz saxophone" -o jazz.mp3

# Extended generation
musicgen generate "epic orchestral" --duration 120 -o epic.mp3

# Batch processing
musicgen batch playlist.csv --output-dir music/
```

### Python API

```python
from musicgen import MusicGenerator

# Initialize
generator = MusicGenerator(device="cuda")

# Generate music
audio, sample_rate = generator.generate(
    "ambient electronic",
    duration=30.0
)

# Save
generator.save_audio(audio, sample_rate, "output.mp3")
```

### Web Interface

```bash
musicgen serve --port 8080
# Open http://localhost:8080
```

### REST API

```bash
musicgen api --port 8000

# Generate music
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "classical piano", "duration": 30}'
```

## Deployment

### Docker

```bash
docker build -t musicgen .
docker run -p 8080:8080 --gpus all musicgen
```

### AWS

```bash
# Configure AWS credentials
aws configure

# Deploy
./deployment/deploy_aws.sh
```

## Architecture

```
musicgen-unified/
├── musicgen/
│   ├── generator.py    # Core generation with GPU optimization
│   ├── batch.py        # Batch processing
│   ├── prompt.py       # Prompt engineering
│   ├── api.py          # FastAPI server
│   ├── cli.py          # CLI interface
│   └── utils.py        # Utilities
├── static/             # Web UI files
├── tests/              # Test suite
└── deployment/         # Deployment scripts
```

## Performance

- **GPU**: 10x faster than realtime
- **CPU**: 1x realtime (approximate)
- **Memory**: <1GB base, ~4GB with large model
- **Startup**: <10 seconds

## Models

- `small`: Fast, lower quality (300M parameters)
- `medium`: Balanced (1.5B parameters)
- `large`: Best quality (3.3B parameters)

## Contributing

We welcome contributions! Please see CONTRIBUTING.md for guidelines.

## License

MIT License - see LICENSE file for details.

## Acknowledgments

- Facebook Research for MusicGen
- The open source community

## Support

- Issues: GitHub Issues
- Discussions: GitHub Discussions
- Email: support@example.com