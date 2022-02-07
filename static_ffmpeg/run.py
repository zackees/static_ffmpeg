"""
    Entry point for running the ffmpeg executable.
"""


import os
import stat
import sys
import zipfile

SELF_DIR = os.path.dirname(__file__)
ARCHIVE_ZIP = os.path.join(SELF_DIR, "archive.zip")
VALID_PLATFORMS = ["win32", "linux", "darwin"]


def get_platform_dir():
    """Either get the executable or raise an error"""
    if sys.platform not in VALID_PLATFORMS:
        raise OSError(f"Please implement static_ffmpeg for {sys.platform}")
    return os.path.join(SELF_DIR, sys.platform)


def get_platform_executable_or_raise(fix_permissions=True):
    """Either get the executable or raise an error"""
    exe_dir = get_platform_dir()
    if not os.path.exists(exe_dir):
        with zipfile.ZipFile(ARCHIVE_ZIP, "r") as zip_ref:
            zip_ref.extractall(SELF_DIR)

    ffmpeg_exe = os.path.join(exe_dir, "ffmpeg")
    if sys.platform == "win32":
        ffmpeg_exe = f"{ffmpeg_exe}.exe"

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
        assert os.access(ffmpeg_exe, os.R_OK), f"Could not get read bits of {ffmpeg_exe}"
    return ffmpeg_exe


def main():
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    ffmpeg_exe = get_platform_executable_or_raise()
    str_args = " ".join(sys.argv[1:])
    cmd = f"{ffmpeg_exe} {str_args}"
    rtn = os.system(cmd)
    sys.exit(rtn)
