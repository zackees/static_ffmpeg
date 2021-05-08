import json
import os
import sys
import tempfile
import unittest
import subprocess

import requests

from pyffmpeg import run

class PyFFMPEGTester(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cleanup = []

    def tearDown(self):
        for cleanup in self.cleanup:
            try:
                cleanup()
            except BaseException as be:
                print(str(be))
        self.cleanup = []

    def create_tmp(self, suffix) -> str:
        tmp_file = tempfile.NamedTemporaryFile(prefix='pyffmpeg_', suffix=suffix, delete=False)
        tmp_file.close()
        self.cleanup.append(lambda: os.remove(tmp_file.name))
        return os.path.abspath(tmp_file.name)

    def test_platform_executable(self) -> None:
        run.get_platform_executable_or_raise()

    def test_run_pyffmpeg(self) -> None:
        cmd = f'pyffmpeg -version'
        subprocess.check_output(cmd)


if __name__ == '__main__':
    unittest.main()
