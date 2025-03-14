"""
Tests that https://github.com/zackees/static_ffmpeg/issues/9 is resolved. This bug did not allow spaces in the names.
"""

import os
import subprocess
import unittest

_HERE = os.path.dirname(os.path.abspath(__file__))
_TEST_FILE = os.path.join(_HERE, "bug 9.mp4")
_OUT_FILE = os.path.join(_HERE, "test_clip_out.mp4")


class static_Bug9Tester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def test_platform_executable(self) -> None:
        subprocess.call(
            [
                "static_ffmpeg",  # call ffmpeg
                "-ss",
                "0:00",  # our clip starts here
                "-i",
                _TEST_FILE,  # this is the video to be converted
                "-t",
                "1",  # how long our clip is
                "-threads",
                "4",  # use 4 threads for the video conversion
                "-c:v",
                "libvpx-vp9",  # c[odec]:v[ideo] - we use libvpx cause we want webm
                "-c:a",
                "libvorbis",  # c[odec]:a[udio] - this is the one everyone else was using
                "-b:v",
                "400k",  # reccomended video bitrate
                "-b:a",
                "192k",  # reccomended audio bitrate
                "-deadline",
                "good",  # setting for quality vs. speed (best, good, realtime (fastest)); boundry for quality vs. time set the following settings
                "-qmin",
                "0",  # quality minimum boundry. (lower means better)
                "-qmax",
                "50",  # quality maximum boundry (higher means worse)
                _OUT_FILE,  # file to be written out
            ]
        )
        if os.path.exists(_OUT_FILE):
            os.remove(_OUT_FILE)


if __name__ == "__main__":
    unittest.main()
