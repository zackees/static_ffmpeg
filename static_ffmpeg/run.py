"""
    Entry point for running the ffmpeg executable.
"""


import os
import stat
import sys

SELF_DIR = os.path.dirname(__file__)


def get_platform_executable_or_raise(fix_permissions=True):
    """Either get the executable or raise an error"""
    if sys.platform == "win32":
        ffmpeg_exe = os.path.join(SELF_DIR, "win32", "ffmpeg.exe")
    elif sys.platform == "linux":
        ffmpeg_exe = os.path.join(SELF_DIR, "linux", "ffmpeg")
    elif sys.platform == "darwin":
        ffmpeg_exe = os.path.join(SELF_DIR, "macos_x64", "ffmpeg")
    else:
        raise OSError(f"Please implement static_ffmpeg for {sys.platform}")

    if (
        fix_permissions
        and sys.platform != "win32"
        and (not os.access(ffmpeg_exe, os.X_OK) or not os.access(ffmpeg_exe, os.R_OK))
    ):
        # Set bits for execution and read for all users.
        exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
        read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IXGRP
        os.chmod(ffmpeg_exe, exe_bits | read_bits)
        assert os.access(ffmpeg_exe, os.X_OK), f"Could not execute {ffmpeg_exe}"
        assert os.access(ffmpeg_exe, os.R_OK), f"Could not get read of {ffmpeg_exe}"
    return ffmpeg_exe


def main():
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    ffmpeg_exe = get_platform_executable_or_raise()
    str_args = " ".join(sys.argv[1:])
    cmd = f"{ffmpeg_exe} {str_args}"
    rtn = os.system(cmd)
    sys.exit(rtn)
