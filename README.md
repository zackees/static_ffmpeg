
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/MacOS_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_macos.yml)
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/Win_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_win.yml)
[![Actions Status](https://github.com/zackees/static_ffmpeg/workflows/Ubuntu_Tests/badge.svg)](https://github.com/zackees/static_ffmpeg/actions/workflows/push_ubuntu.yml)

# static-ffmpeg

The easiest way to get ffmpeg v5 installed through python.

## Install

```bash
> pip install static-ffmpeg
```

## Usage

```py
import static_ffmpeg
# ffmpeg installed on first call to add_paths(), threadsafe.
static_ffmpeg.add_paths()  # blocks until files are downloaded
# or static_ffmpeg.add_paths(weak=True) to only add if ffmpeg/ffprobe not already on path
# Now ffmpeg and ffprobe will use static_ffmpeg versions.
os.system("ffmpeg -i myfile.mp4 ...")
```

Or if you want more lazy behavior to install on first use, or you don't want to modify system paths, use `static_ffmpeg`


```py
import static_ffmpeg
# ffmpeg installed on first call, threadsafe.
os.system("static_ffmpeg -i myfile.mp4 ...")
```

You can also use it on the command line

```bash
> pip install static-ffmpeg
> static_ffmpeg -i file.mp4 ...
> static_ffprobe ...
> static_ffmpeg_paths
FFMPEG=c:\users\niteris\dev\static_ffmpeg\static_ffmpeg\bin\win32\ffmpeg.exe
FFPROBE=c:\users\niteris\dev\static_ffmpeg\static_ffmpeg\bin\win32\ffprobe.exe
```

## About

This tool installs binaries for ffmpeg and ffprobe binary (with all plugins and codecs) into the running platform. The platform binaries are installed on first use and is done without requiring elevated permissions.

This package is designed to allow tools that rely on `ffmpeg` to have a fully featured `ffmpeg` available by just including this package. No seperate install of ffmpeg is needed.

### Without this library...

Your ffmpeg tool would have to rely on the user to install `ffmpeg`, with the right build settings to ensure your tool functions correctly. This is a major pain for ffmpeg based tools (missing codecs for example) and this library solves this problem.

As of now, binaries are available for:
  * `win32` (Windows)
  * `darwin` (MacOS)
  * `linux` (From Ubuntu 20LTS)
  * Pull requests to support for other platforms are welcome! Too add support please see related git repo: [ffmpeg_bins](https://github.com/zackees/ffmpeg_bins).

There is both an python api and a command line api. After installing this package the command line aliases will be available:

  * `static_ffmpeg` operates just like `ffmpeg`
  * `static_ffprobe` operates just like `ffprobe`.
  * `static_ffmpeg_paths` prints out the paths of the ffmpeg binaries.

```bash
> static_ffmpeg_paths
FFMPEG=c:\users\niteris\dev\static_ffmpeg\static_ffmpeg\bin\win32\ffmpeg.exe
FFPROBE=c:\users\niteris\dev\static_ffmpeg\static_ffmpeg\bin\win32\ffprobe.exe
```


## Api

Here's how to get the binaries and execute them.

```py
# Using the alias method
import os
# Platform binaries will be installed the first run.
os.system("static_ffmpeg -version")  # static_ffmpeg is an alias for this tools ffmpeg.
os.system("static_ffprobe -version")
```


```py
# Using the program location method
import subprocess
from static_ffmpeg import run
# Platform binaries are installed on the first run of below.
ffmpeg, ffprobe = run.get_or_fetch_platform_executables_else_raise()
# ffmpeg, ffprobe will be paths to ffmpeg and ffprobe.
subprocess.check_output([ffmpeg, "-version"])
subprocess.check_output([ffprobe, "-version"])
```



## Testing

  * Clone this project `git clone https://github.com/zackees/static_ffmpeg`
  * `cd static_ffmpeg`
  * Then run tox `tox`


## Virtual Environment (optional)

To test it in a virtual environment, use this easy helper:

To easily setup a virtual environment, please run
```bash
python setupvirtualenv.py
```

Then run `./activate.sh` to activate the shell.

## Binary source
  * https://github.com/zackees/ffmpeg_bins

## Version

ffmpeg and ffprobe are both version: 5.0

## Release History
  * 2.7: Bugfix, increase the timeout to download for slow connections to 10 minutes.
  * 2.6: Bugfix, `add_paths(...)` can now be called multiple times without polluting the os env path.
  * 2.5: `add_paths()` now has optional `weak` parameter (default False). If True then `ffmpeg/ffprobe` binaries are only only if either `ffmpeg` OR `ffprobe` doesn't already exist on path
  * 2.3: Adds `static_ffmpeg.add_paths()`
  * 2.2: Addressed [bug 9](https://github.com/zackees/static_ffmpeg/issues/9) in some cases static_ffmpeg couldn't handle spaces in mp4 names.
  * 2.1: Addressed [bug 7](https://github.com/zackees/static_ffmpeg/issues/7) on Win32 for not handling spaces in directory names in the site packages path.
  * 2.0:
    * ffmpeg upgraded to 5.0
    * added ffprobe (static_ffprobe or get run.get_platform_executables_or_raise() to get the binary location)
    * Now downloads platform specific binary to reduce install size (reduced 2/3rds of the install size vs 1.0)
  * 1.0:
    * ffmpeg 4.4 released + tests
