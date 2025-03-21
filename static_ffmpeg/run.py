"""
Entry point for running the ffmpeg executable.
"""

import os
import stat
import subprocess
import sys
import zipfile
from datetime import datetime
from typing import Tuple

import requests  # type: ignore
from filelock import FileLock, Timeout
from progress.bar import Bar  # type: ignore
from progress.spinner import Spinner  # type: ignore

TIMEOUT = 10 * 60  # Wait upto 10 minutes to validate install
# otherwise break the lock and install anyway.

SELF_DIR = os.path.abspath(os.path.dirname(__file__))
LOCK_FILE = os.path.join(SELF_DIR, "lock.file")


PLATFORM_ZIP_FILES = {
    "win32": "https://github.com/zackees/ffmpeg_bins/raw/main/v5.0/win32.zip",
    "darwin": "https://github.com/zackees/ffmpeg_bins/raw/main/v5.0/darwin.zip",
    "linux": "https://github.com/zackees/ffmpeg_bins/raw/main/v5.0/linux.zip",
}


def check_system() -> None:
    """Friendly error if there's a problem with the system configuration."""
    if sys.platform not in PLATFORM_ZIP_FILES:
        raise OSError(f"Please implement static_ffmpeg for {sys.platform}")


def get_platform_http_zip() -> str:
    """Return the download link for the current platform"""
    check_system()
    return PLATFORM_ZIP_FILES[sys.platform]


def get_platform_dir() -> str:
    """Either get the executable or raise an error"""
    check_system()
    return os.path.join(SELF_DIR, "bin", sys.platform)


def download_file(url: str, local_path: str) -> str:
    """Downloads a file to the give path."""
    # NOTE the stream=True parameter below
    print(f"Downloading {url} -> {local_path}")
    chunk_size = (1024 * 1024) // 4
    with requests.get(url, stream=True, timeout=TIMEOUT) as req:
        req.raise_for_status()
        spinner: Spinner | Bar = Spinner("ffmpeg: ")
        size = -1
        try:
            size = int(req.headers.get("content-length", 0))
            spinner = Bar("ffmpeg: ", max=size, suffix="%(percent).1f%% - %(eta)ds")
        except ValueError:
            pass
        with open(local_path, "wb") as file_d:
            with spinner as spinner:
                for chunk in req.iter_content(chunk_size):
                    file_d.write(chunk)
                    spinner.next(len(chunk))
            sys.stdout.write(f"\nDownload of {url} -> {local_path} completed.\n")
    return local_path


def get_or_fetch_platform_executables_else_raise(
    fix_permissions=True, download_dir=None
) -> Tuple[str, str]:
    """Either get the executable or raise an error"""
    lock = FileLock(LOCK_FILE, timeout=TIMEOUT)  # pylint: disable=E0110
    try:
        with lock.acquire():
            return _get_or_fetch_platform_executables_else_raise_no_lock(
                fix_permissions=fix_permissions, download_dir=download_dir
            )
    except Timeout:
        sys.stderr.write(
            f"{__file__}: Warning, could not acquire lock at {LOCK_FILE}\n"
        )
        return _get_or_fetch_platform_executables_else_raise_no_lock(
            fix_permissions=fix_permissions, download_dir=download_dir
        )


def _get_or_fetch_platform_executables_else_raise_no_lock(
    fix_permissions=True, download_dir=None
) -> Tuple[str, str]:
    """Either get the executable or raise an error, internal api"""
    exe_dir = download_dir if download_dir else get_platform_dir()
    installed_crumb = os.path.join(exe_dir, "installed.crumb")
    if not os.path.exists(installed_crumb):
        # All zip files store their platform executables in a folder
        # like "win32" or "darwin" or "linux" inside the executable. So root
        # the install one level up from that same directory.
        install_dir = os.path.dirname(exe_dir)
        os.makedirs(exe_dir, exist_ok=True)
        url = get_platform_http_zip()
        local_zip = exe_dir + ".zip"
        download_file(url, local_zip)
        print(f"Extracting {local_zip} -> {install_dir}")
        with zipfile.ZipFile(local_zip, mode="r") as zipf:
            zipf.extractall(install_dir)
        try:
            os.remove(local_zip)
        except OSError as err:
            print(f"{__file__}: Error could not remove {local_zip} because of {err}")
        with open(installed_crumb, "wt") as filed:  # pylint: disable=W1514
            filed.write(f"installed from {url} on {str(datetime.now())}")
    ffmpeg_exe = os.path.join(exe_dir, "ffmpeg")
    ffprobe_exe = os.path.join(exe_dir, "ffprobe")
    if sys.platform == "win32":
        ffmpeg_exe = f"{ffmpeg_exe}.exe"
        ffprobe_exe = f"{ffprobe_exe}.exe"
    for exe in [ffmpeg_exe, ffprobe_exe]:
        if (
            fix_permissions
            and sys.platform != "win32"
            and (not os.access(exe, os.X_OK) or not os.access(exe, os.R_OK))
        ):
            # Set bits for execution and read for all users.
            exe_bits = stat.S_IXOTH | stat.S_IXUSR | stat.S_IXGRP
            read_bits = stat.S_IRUSR | stat.S_IRGRP | stat.S_IXGRP
            os.chmod(exe, exe_bits | read_bits)
            assert os.access(exe, os.X_OK), f"Could not execute {exe}"
            assert os.access(exe, os.R_OK), f"Could not get read bits of {exe}"
    return ffmpeg_exe, ffprobe_exe


def main_static_ffmpeg() -> None:
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    ffmpeg_exe, _ = get_or_fetch_platform_executables_else_raise()
    rtn: int = subprocess.call([ffmpeg_exe] + sys.argv[1:])
    sys.exit(rtn)


def main_static_ffprobe() -> None:
    """Entry point for running static_ffmpeg, which delegates to ffmpeg."""
    _, ffprobe = get_or_fetch_platform_executables_else_raise()
    rtn: int = subprocess.call([ffprobe] + sys.argv[1:])
    sys.exit(rtn)


def main_print_paths() -> None:
    """Entry point for printing ffmpeg paths"""
    ffmpeg_exe, ffprobe_exe = get_or_fetch_platform_executables_else_raise()
    print(f"FFMPEG={ffmpeg_exe}")
    print(f"FFPROBE={ffprobe_exe}")
    sys.exit(0)


if __name__ == "__main__":
    get_or_fetch_platform_executables_else_raise()
