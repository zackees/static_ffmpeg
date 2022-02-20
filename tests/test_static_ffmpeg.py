import os
import stat
import subprocess
import sys
import unittest

from static_ffmpeg import run


class static_ffmpegTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup = []

    def test_platform_executable(self) -> None:
        run.get_or_fetch_platform_executables_else_raise()

    def test_run_static_ffmpeg(self) -> None:
        subprocess.check_output(["static_ffmpeg", "-version"])

    def test_run_static_ffprobe(self) -> None:
        subprocess.check_output(["static_ffprobe", "-version"])
    
    def test_run_no_shell(self) -> None:
        ffmpeg_exe, ffprobe_exe = run.get_or_fetch_platform_executables_else_raise()
        subprocess.check_output([ffmpeg_exe, '-version'])
        subprocess.check_output([ffprobe_exe, '-version'])

    @unittest.skipIf(sys.platform == "win32", "Only valid for macos and linux")
    def test_permission_bits(self) -> None:
        ffmpeg_exe, ffprobe_exe = run.get_or_fetch_platform_executables_else_raise()
        for exe in [ffmpeg_exe, ffprobe_exe]:
            mode = os.stat(exe).st_mode
            exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
            read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IXGRP
            self.assertEqual(
                exe_bits,
                mode & exe_bits,
                "FFMPEG does not have the right executable bits",
            )
            self.assertEqual(
                read_bits, mode & read_bits, "FFMPEG does not have the right read bits"
            )


if __name__ == "__main__":
    unittest.main()
