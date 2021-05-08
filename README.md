# pyffmpeg

FFMPEG Version: 4.4

Problem: You develop on Windows/MacOS/Linux. You want an ffmpeg
that works on all the platforms but now you have to go and special
case your program installation to handle each platforms ability
to get the ffmpeg download.

This tool is designed to make this easier, as easy as doing
`pip install .` and then running `pyffmpeg --version` to test this out.

At this first launch, this program only supports Win32 (the motivation
for this project) but other platforms will be supported as well.

A note about Win32: we are using a pre-built binary and it may go
stale. Feel free to fork this package up and update the ffmpeg, run
tox and then do a pull request on this package.

Once this package is installed, the pyffmpeg command will
be available. This command simply passes all arguments to
a real ffmpeg. Call pyffmpeg like you would call ffmpeg in your project
and it should just work.

# Binary source
  * MacOS (Intel): https://evermeet.cx/pub/ffmpeg/
  * MacOS (Arm): TODO: https://osxexperts.net/
  * Windows: (My computer download)
  * Linux: https://johnvansickle.com/ffmpeg/

# Testing

  * Clone this project `git clone https://github.com/zackees/pyffmpeg`
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