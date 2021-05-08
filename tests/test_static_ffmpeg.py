import unittest
import subprocess

from static_ffmpeg import run

class static_ffmpegTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup = []

    def test_platform_executable(self) -> None:
        run.get_platform_executable_or_raise()

    def test_run_static_ffmpeg(self) -> None:
        subprocess.check_output(['static_ffmpeg', '-version'])


if __name__ == '__main__':
    unittest.main()
