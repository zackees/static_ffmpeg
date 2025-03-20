"""
add_paths() Adds ffmpeg and ffprobe to the path, overriding any system ffmpeg/ffprobe.
"""

import os
import shutil

from .run import get_or_fetch_platform_executables_else_raise


def _has(name: str) -> bool:
    """Check if the path has the name"""
    return shutil.which(name) is not None


def add_paths(weak=False, download_dir=None) -> bool:
    """Add the ffmpeg executable to the path"""
    if weak:
        has_ffmpeg = _has("ffmpeg")
        has_ffprobe = _has("ffprobe")
        if has_ffmpeg and has_ffprobe:
            return False
    ffmpeg, _ = get_or_fetch_platform_executables_else_raise(download_dir=download_dir)
    ffmpeg_path = os.path.dirname(ffmpeg)
    if ffmpeg_path not in os.environ["PATH"]:
        os.environ["PATH"] = os.pathsep.join([ffmpeg_path, os.environ["PATH"]])
    return True
