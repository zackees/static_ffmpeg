"""
add_paths() Adds ffmpeg and ffprobe to the path, overriding any system ffmpeg/ffprobe.
"""

import shutil
import os
from .run import get_or_fetch_platform_executables_else_raise


def add_paths(weak=False) -> bool:
    """Add the ffmpeg executable to the path"""
    if weak:
        if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
            return False
    ffmpeg, _ = get_or_fetch_platform_executables_else_raise()
    os.environ["PATH"] = os.pathsep.join([os.path.dirname(ffmpeg), os.environ["PATH"]])
    return True
