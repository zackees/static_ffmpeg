
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_macos.yml)
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/Win_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_win.yml)
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_ubuntu.yml)

# static_ffmpeg


## Version
FFMPEG Version: 5.0


## About

Problem: You develop on Windows/MacOS/Linux. You want an ffmpeg
that works on all the platforms but now you have to go and special
case your program installation to handle each platforms ability
to get the ffmpeg download. For example:
  * Win32: `choco install ffmpeg`
  * MacOS: `brew install ffmpeg`
  * Linux: `sudo apt-get install ffmpeg`

If you want to be able to quitely (re)install a python package silently and
automatically using ffmpeg, well you are out of luck... until now.

## Api

```
import os
from static_ffmpeg import run
ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
# ffmpeg, ffprobe will be paths to ffmpeg and ffprobe.
os.system(f"{ffmpeg} -version")
os.system(f"{ffprobe} -version")
```

Or, after installing static_ffmpeg in your current python environment,
use `static_ffmpeg`, `static_ffprobe` from the command line.

## Pre-installation (optional)

To easily setup a virtual environment, please see this installation script:
https://raw.githubusercontent.com/zackees/static_ffmpeg/main/setupvirtualenv.py

## Installation

To use simply do `pip install static-ffmpeg` and then after this is done you
can try running `static_ffmpeg -version` and/or `static_ffprobe -version` to test out
that the version has been installed.

Once this package is installed, the `static_ffmpeg` and `static_ffprobe` command
will be available. This command simply passes all arguments to
a real ffmpeg/ffprobe. Call static_ffmpeg like you would call ffmpeg in your project
and it should just work, or bypass the stub and use the ffmpeg/ffprobe directly by getting
the path via `run.get_or_fetch_platform_executables_else_raise()`


## Binary source
  * https://github.com/zackees/ffmpeg_bins

## Testing

  * Clone this project `git clone https://github.com/zackees/static_ffmpeg`
  * Then setup the virtual env using the script `python virtualenvsetup.py`
  * Then activate `. venv/bin/activate`
  * Then run tox `tox`

## Testing work arounds
  * You may get an error like 'Interpretor not found'
    * The solution it install the python interpretor of this type, like so
      * https://www.python.org/downloads/release/python-3810/
  * Ubuntu: `ModuleNotFoundError: No module named 'virtualenv.seed.via_app_data'
    * Uninstall the pip on your system and reinstall:
      * `pip3 uninstall virtualenv`
      * `pip3 install virtualenv`

## Release History
  * 2.0:
    * ffmpeg upgraded to 5.0
    * added ffprobe (static_ffprobe or get run.get_platform_executables_or_raise() to get the binary location)
    * Now downloads platform specific binary to reduce install size (reduced 2/3rds of the install size vs 1.0)
  * 1.0:
    * ffmpeg 4.4 released + tests
