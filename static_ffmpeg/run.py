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
    return os.path.abspath(os.path.join(SELF_DIR, sys.platform))


def get_platform_executables_or_raise(fix_permissions=True):
    """Either get the executable or raise an error"""
    exe_dir = get_platform_dir()
    if not os.path.exists(exe_dir):
        zip_file = os.path.abspath(os.path.join(SELF_DIR, f"{sys.platform}.zip"))
        with zipfile.ZipFile(zip_file, "r") as zipf:
            zipf.extractall(SELF_DIR)

    ffmpeg_exe = os.path.join(exe_dir, "ffmpeg")
    ffprobe_exe = os.path.join(exe_dir, "ffprobe")
    if sys.platform == "win32":
        ffmpeg_exe = f"{ffmpeg_exe}.exe"
        ffprobe_exe = f"{ffprobe_exe}.exe"

    for exe in [ffmpeg_exe, ffprobe_exe]:
        if (
            fix_permissions
            and sys.platform != "win32"
            and (
                not os.access(exe, os.X_OK) or not os.access(exe, os.R_OK)
            )
        ):
            # Set bits for execution and read for all users.
            exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
            read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IXGRP
            os.chmod(ffmpeg_exe, exe_bits | read_bits)
            assert os.access(exe, os.X_OK), f"Could not execute {exe}"
            assert os.access(
                exe, os.R_OK
            ), f"Could not get read bits of {exe}"
    return ffmpeg_exe, ffprobe_exe


def main_static_ffmpeg():
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    ffmpeg_exe, _ = get_platform_executables_or_raise()
    str_args = " ".join(sys.argv[1:])
    cmd = f"{ffmpeg_exe} {str_args}"
    rtn = os.system(cmd)
    sys.exit(rtn)


def main_static_ffprobe():
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    _, ffprobe = get_platform_executables_or_raise()
    str_args = " ".join(sys.argv[1:])
    cmd = f"{ffprobe} {str_args}"
    rtn = os.system(cmd)
    sys.exit(rtn)
