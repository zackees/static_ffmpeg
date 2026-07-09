"""
Manifest-based artifact resolution for static_ffmpeg.

This implements the client half of the migration described in
https://github.com/zackees/static_ffmpeg/issues/20 : instead of hard-coding one
download URL per platform, the client detects a *platform tuple*
(``os`` / ``arch`` / ``libc``) and resolves it against a ``manifest.json``
catalog (see https://github.com/zackees/manifest.json for the format).

Design constraints (from the issue):

* **Backward compatibility is absolute.** This module is *best effort*. If the
  manifest is disabled, unreachable, malformed, or does not describe the current
  platform, the caller falls back to the legacy hard-coded URL. Existing
  installs -- which never call this module at all -- are unaffected because the
  legacy ``ffmpeg_bins`` URLs are never moved or mutated.
* **Integrity is verified.** Every asset carries a ``sha256`` which the caller
  checks after download.
* **Linux distinguishes glibc from musl**, so we can ship both a glibc-2.17
  baseline build and a musl build for the same architecture.

The default manifest URL is intentionally empty until ``ffmpeg-bins2`` and its
CDN front-end are live; set ``STATIC_FFMPEG_MANIFEST_URL`` to opt in early, or
flip ``DEFAULT_MANIFEST_URL`` once the infrastructure exists.
"""

import glob
import hashlib
import os
import platform
import subprocess
import sys
from typing import Dict, List, NamedTuple, Optional

import requests  # type: ignore

# Published ffmpeg-bins2 catalog. Resolution is still best-effort: platforms not
# listed here (currently Windows and musl -- pending forge build fixes) and any
# fetch/parse failure fall back to the legacy hard-coded URLs, so existing and
# unlisted-platform installs are never broken. Override via the environment.
DEFAULT_MANIFEST_URL = (
    "https://raw.githubusercontent.com/zackees/ffmpeg-bins2/main/manifest.json"
)

# The channel a fresh install pulls from. Existing installs pin their resolved
# version in installed.crumb and are never silently upgraded.
DEFAULT_CHANNEL = "latest-stable"

TOOL_NAME = "ffmpeg"


class Asset(NamedTuple):
    """A single downloadable artifact resolved from the manifest."""

    url: str
    sha256: Optional[str]
    filename: Optional[str] = None
    size_bytes: Optional[int] = None
    version: Optional[str] = None


def manifest_url() -> str:
    """Return the manifest URL, or "" if manifest resolution is disabled."""
    return os.environ.get("STATIC_FFMPEG_MANIFEST_URL", DEFAULT_MANIFEST_URL)


def _detect_arch() -> str:
    """Normalise ``platform.machine()`` into a manifest arch token."""
    machine = platform.machine().lower()
    if machine in ("arm64", "aarch64"):
        return "arm64"
    if machine in ("x86_64", "amd64", "x64"):
        return "x86_64"
    return machine


def _detect_linux_libc() -> str:
    """
    Best-effort detection of glibc vs musl on Linux.

    ``platform.libc_ver()`` reports glibc reliably but returns empty for musl
    (musl has no gnu_get_libc_version symbol), so we corroborate with ``ldd``
    and, as a last resort, the presence of the musl dynamic loader.
    """
    try:
        libc_name, _ = platform.libc_ver()
        if libc_name and "glibc" in libc_name.lower():
            return "glibc"
    except OSError:
        pass

    try:
        proc = subprocess.run(
            ["ldd", "--version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=5,
            check=False,
        )
        text = proc.stdout.decode("utf-8", "replace").lower()
        if "musl" in text:
            return "musl"
        if "glibc" in text or "gnu libc" in text or "gnu c library" in text:
            return "glibc"
    except (OSError, subprocess.SubprocessError):
        pass

    if glob.glob("/lib/ld-musl-*") or glob.glob("/usr/lib/ld-musl-*"):
        return "musl"

    # Default assumption for Linux is glibc.
    return "glibc"


def get_platform_tuple() -> Dict[str, str]:
    """
    Detect the current platform as a manifest tuple.

    Returns a dict with ``os`` and ``arch`` always present, and ``libc`` present
    on Linux (``glibc`` or ``musl``).
    """
    arch = _detect_arch()
    if sys.platform == "win32":
        return {"os": "windows", "arch": arch}
    if sys.platform == "darwin":
        return {"os": "macos", "arch": arch}
    if sys.platform == "linux":
        return {"os": "linux", "arch": arch, "libc": _detect_linux_libc()}
    return {"os": sys.platform, "arch": arch}


def _tuple_matches(query: Dict[str, str], candidate: Dict[str, object]) -> bool:
    """
    Manifest matching rule: two tuples match iff every field *present in the
    candidate* is equal to the query. Fields absent from the candidate act as
    wildcards, so a manifest may omit ``libc`` to match any Linux libc.
    """
    for key, value in candidate.items():
        if key not in query:
            return False
        if str(query[key]) != str(value):
            return False
    return True


def _resolve_asset_from_catalog(
    catalog: dict, query: Dict[str, str], channel: str
) -> Optional[Asset]:
    """Resolve ``query`` against an already-parsed Catalog document."""
    if catalog.get("tool") not in (None, TOOL_NAME):
        return None

    channels = catalog.get("channels", {})
    releases = catalog.get("releases", [])
    if not releases:
        return None

    target_version = channels.get(channel, channel)

    release = None
    for candidate in releases:
        if candidate.get("version") == target_version:
            release = candidate
            break
    if release is None:
        # Fall back to the newest release (releases are newest-first).
        release = releases[0]

    for entry in release.get("platforms", []):
        candidate_tuple = entry.get("platform", {})
        if not _tuple_matches(query, candidate_tuple):
            continue
        asset = entry.get("asset", {})
        urls = asset.get("urls") or []
        if not urls:
            continue
        return Asset(
            url=urls[0],
            sha256=asset.get("sha256"),
            filename=asset.get("filename"),
            size_bytes=asset.get("size_bytes"),
            version=release.get("version"),
        )
    return None


def resolve_asset(
    query: Optional[Dict[str, str]] = None,
    channel: str = DEFAULT_CHANNEL,
    url: Optional[str] = None,
    timeout: int = 30,
) -> Optional[Asset]:
    """
    Resolve the current (or given) platform to an :class:`Asset` via the
    manifest. Returns ``None`` -- never raises -- when resolution is disabled or
    fails for any reason, so the caller can fall back to legacy behaviour.
    """
    src = url if url is not None else manifest_url()
    if not src:
        return None
    if query is None:
        query = get_platform_tuple()

    try:
        resp = requests.get(src, timeout=timeout)
        resp.raise_for_status()
        catalog = resp.json()
    except (requests.RequestException, ValueError):
        return None

    try:
        return _resolve_asset_from_catalog(catalog, query, channel)
    except (AttributeError, TypeError, KeyError):
        return None


def sha256_of_file(path: str, chunk_size: int = 1024 * 1024) -> str:
    """Return the lowercase hex sha256 digest of a file."""
    digest = hashlib.sha256()
    with open(path, "rb") as file_d:
        for chunk in iter(lambda: file_d.read(chunk_size), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_sha256(path: str, expected: Optional[str]) -> None:
    """
    Raise ``ValueError`` if ``path`` does not match ``expected`` sha256.

    A ``None``/empty ``expected`` is treated as "no integrity data available"
    and passes silently, matching legacy downloads that carry no checksum.
    """
    if not expected:
        return
    actual = sha256_of_file(path)
    if actual.lower() != expected.lower():
        raise ValueError(
            f"sha256 mismatch for {path}: expected {expected}, got {actual}"
        )


def platform_keys_for(query: Dict[str, str]) -> List[str]:
    """Human-readable description of a platform tuple, for logging/errors."""
    parts = [query.get("os", "?"), query.get("arch", "?")]
    if "libc" in query:
        parts.append(query["libc"])
    return parts
