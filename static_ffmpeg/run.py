"""
    Entry point for running the ffmpeg executable.
"""


import os
import sys

import static_ffmpeg

PCKG_PATH = static_ffmpeg.__path__[0]  # type: ignore  # mypy issue #1422


def get_platform_executable_or_raise():
    """Either get the executable or raise an error"""
    if sys.platform == "win32":
        return os.path.join(PCKG_PATH, "win32", "ffmpeg.exe")
    if sys.platform == "linux":
        return os.path.join(PCKG_PATH, "linux", "ffmpeg")
    if sys.platform == "darwin":
        return os.path.join(PCKG_PATH, "macos_x64", "ffmpeg")
    raise OSError(f"Please implement static_ffmpeg for {sys.platform}")


def main():
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    ffmpeg_exe = get_platform_executable_or_raise()
    str_args = " ".join(sys.argv[1:])
    cmd = f"{ffmpeg_exe} {str_args}"
    rtn = os.system(cmd)
    sys.exit(rtn)
