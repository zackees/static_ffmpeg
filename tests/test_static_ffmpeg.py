import shutil
import unittest
import subprocess

from static_ffmpeg import run


class static_ffmpegTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup = []

    def test_platform_executable(self) -> None:
        run.get_platform_executable_or_raise()

    def test_no_fix_permissions(self) -> None:
        run.get_platform_executable_or_raise(False)

    def test_run_static_ffmpeg(self) -> None:
        subprocess.check_output(['static_ffmpeg', '-version'])

import os
import stat
import subprocess
import sys, os
import unittest

from static_ffmpeg import run
import static_ffmpeg


def test_check_path() -> None:
    assert shutil.which("ffmpeg") is not None


class static_ffmpegTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup = []

    def test_platform_executable(self) -> None:
        static_ffmpeg.get_platform_executable_or_raise()

    def test_run_static_ffmpeg(self) -> None:
        subprocess.check_output(["static_ffmpeg", "-version"])

    @unittest.skipIf(sys.platform == "win32", "Only valid for macos and linux")
    def test_permission_bits(self) -> None:
        ffmpeg_exe = static_ffmpeg.get_platform_executable_or_raise()
        mode = os.stat(ffmpeg_exe).st_mode
        exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
        read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IXGRP
        self.assertEqual(exe_bits, mode & exe_bits, "FFMPEG does not have the right executable bits")
        self.assertEquals(read_bits, mode & read_bits, "FFMPEG does not have the right read bits")


if __name__ == "__main__":
    unittest.main()



if __name__ == '__main__':
    unittest.main()
