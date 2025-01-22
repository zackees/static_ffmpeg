import unittest

from static_ffmpeg import _add_paths


class static_ffmpeg_add_paths_weak(unittest.TestCase):

    def test_add_weak(self) -> None:
        _add_paths._has = lambda name: True
        installed: bool = _add_paths.add_paths(weak=True)
        self.assertFalse(installed)


if __name__ == "__main__":
    unittest.main()
