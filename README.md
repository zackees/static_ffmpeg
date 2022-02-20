
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_macos.yml)
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/Win_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_win.yml)
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_ubuntu.yml)

# static_ffmpeg


## Version
FFMPEG Version: 5.0

## Install

`python -m pip install static-ffmpeg`

## About

This tool installs binaries for ffmpeg and ffprobe binary into the system on the first usage of this library. This libary itself is very
lightweight. Binaries will be installed for `win32` (Windows) / `darwin` (MacOS) / `ubuntu` (Linux)

There is both a python api and a command line api. After installing this package the command line aliases will be available:

  * `static_ffmpeg` operates just like `ffmpeg`
  * `static_ffprobe` operates just like `ffprobe`.
  * `static_ffmpeg_paths` prints out the paths of the ffmpeg binaries.

```
> static_ffmpeg_paths
FFMPEG=c:\users\niteris\dev\static_ffmpeg\static_ffmpeg\bin\win32\ffmpeg.exe
FFPROBE=c:\users\niteris\dev\static_ffmpeg\static_ffmpeg\bin\win32\ffprobe.exe
```

## Api

Here's how to get the binaries and execute them.

```
import os
from static_ffmpeg import run
ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
# ffmpeg, ffprobe will be paths to ffmpeg and ffprobe.
os.system(f"{ffmpeg} -version")
os.system(f"{ffprobe} -version")
```

## Testing

Just simply run `tox`

## Virtual Environment (optional)

To test it in a virtual environment, use this easy helper:

To easily setup a virtual environment, please see this installation script:
https://raw.githubusercontent.com/zackees/static_ffmpeg/main/setupvirtualenv.py

Then activate `. venv/bin/activate`

## Binary source
  * https://github.com/zackees/ffmpeg_bins


## Testing

  * Clone this project `git clone https://github.com/zackees/static_ffmpeg`
  * Then setup the virtual env using the script `python virtualenvsetup.py`
  * Then run tox `tox`

## Release History
  * 2.0:
    * ffmpeg upgraded to 5.0
    * added ffprobe (static_ffprobe or get run.get_platform_executables_or_raise() to get the binary location)
    * Now downloads platform specific binary to reduce install size (reduced 2/3rds of the install size vs 1.0)
  * 1.0:
    * ffmpeg 4.4 released + tests
