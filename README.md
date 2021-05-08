# pyffmpeg

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

# Testing

  * After cloning this project, cd into the main directory and run `tox`