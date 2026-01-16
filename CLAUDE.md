# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

static-ffmpeg is a Python package that provides cross-platform ffmpeg v5.0 binaries. It downloads and installs platform-specific ffmpeg/ffprobe executables on first use, without requiring elevated permissions.

## Build and Development Commands

```bash
# Install dependencies
pip install -e .

# Run tests
tox                    # Full test suite with linting
pytest                 # Just unit tests
pytest tests/test_static_ffmpeg.py::static_ffmpegTester::test_add_paths  # Single test

# Linting (run via tox or individually)
flake8 static_ffmpeg
pylint static_ffmpeg
mypy static_ffmpeg

# Build package
uv build --wheel

# Upload to PyPI
./upload_package.sh
```

## Architecture

### Core Module Structure (`static_ffmpeg/`)

- **`run.py`**: Main entry point logic
  - `get_or_fetch_platform_executables_else_raise()`: Downloads platform binaries on first call (thread-safe via FileLock)
  - Downloads from `https://github.com/zackees/ffmpeg_bins` based on `sys.platform`
  - Binaries stored in `static_ffmpeg/bin/{platform}/`
  - Creates `installed.crumb` marker file after successful install

- **`_add_paths.py`**: Path management
  - `add_paths(weak=False)`: Adds ffmpeg to PATH (weak=True only adds if ffmpeg/ffprobe missing)
  - `remove_paths()`: Removes ffmpeg from PATH

### Entry Points (defined in pyproject.toml)

- `static_ffmpeg` -> `run:main_static_ffmpeg`
- `static_ffprobe` -> `run:main_static_ffprobe`
- `static_ffmpeg_paths` -> `run:main_print_paths`

### Platform Support

Supported platforms (must match keys in `PLATFORM_ZIP_FILES` dict):
- `win32` (Windows)
- `darwin` (macOS)
- `linux` (Ubuntu 20+)

### Binary Source

Binaries are fetched from https://github.com/zackees/ffmpeg_bins at version 5.0.
