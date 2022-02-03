import os
from .run import get_platform_executable_or_raise

__all__ = ['get_platform_executable_or_raise']

try:
    dir = get_platform_executable_or_raise()
    os.environ["PATH"] += os.pathsep + os.path.dirname(dir)
except:
    raise RuntimeError(f"Failed to add static_ffmpeg path {dir} to the system path")
