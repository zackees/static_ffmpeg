
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_macos.yml)
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/Win_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_win.yml)
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_ubuntu.yml)

# static_ffmpeg


## Version
FFMPEG Version: 5.0


## About

Problem: You are making an ffmpeg tool on Windows/MacOS/Linux. You want to bind to a versioned ffmpeg
binary and use it as an api. This tool installs a versioned ffmpeg without requiring elevated privledges.

## Install

`python -m pip install static-ffmpeg`

## Api

In your code, get the binaries:

```
import os
from static_ffmpeg import run
ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
# ffmpeg, ffprobe will be paths to ffmpeg and ffprobe.
os.system(f"{ffmpeg} -version")
os.system(f"{ffprobe} -version")
```

Or run it on the command line by the following:

`static_ffmpeg` or `static_ffprobe`

## Virtual Environment (optional)

To test it in a virtual environment, use this easy helper:

To easily setup a virtual environment, please see this installation script:
https://raw.githubusercontent.com/zackees/static_ffmpeg/main/setupvirtualenv.py


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
