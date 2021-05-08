# static_ffmpeg


## Version
FFMPEG Version: 4.4

## About

Problem: You develop on Windows/MacOS/Linux. You want an ffmpeg
that works on all the platforms but now you have to go and special
case your program installation to handle each platforms ability
to get the ffmpeg download. For example:
  * Win32: download binary
  * MacOS: `brew install ffmpeg`
  * Linux: `sudo apt-get install ffmpeg`

If you want to be able to quitely (re)install a python package silently and
automatically using ffmpeg, well you are out of luck... until now.

## Pre-installation (optional)

To easily setup a virtual environment, please see this installation script:
https://raw.githubusercontent.com/zackees/static_ffmpeg/main/setupvirtualenv.py

## Installation

To use simply do `pip install static-ffmpeg` and then after this is done you
can try running `static_ffmpeg -version` to test out that the version has been
installed.

Once this package is installed, the `static_ffmpeg` command will
be available. This command simply passes all arguments to
a real ffmpeg. Call static_ffmpeg like you would call ffmpeg in your project
and it should just work.

## Warning - Big

  * All three binaries for Win32/OSX/Linux ffmpeg are included. Though if you 
    need ffmpeg then you probably have a large disk anyway.

## Binary source
  * MacOS (Intel): https://evermeet.cx/pub/ffmpeg/
  * MacOS (Arm): TODO: https://osxexperts.net/
  * Windows: (My computer download)
  * Linux: https://johnvansickle.com/ffmpeg/

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