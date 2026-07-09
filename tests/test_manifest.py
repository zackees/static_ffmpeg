"""Offline unit tests for the manifest resolver (no network access)."""

import hashlib
import json
import os
import tempfile
import unittest

from static_ffmpeg import manifest

_REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_EXAMPLE_MANIFEST = os.path.join(_REPO_ROOT, "manifest.example.json")

_ALL_TARGETS = [
    {"os": "windows", "arch": "x86_64"},
    {"os": "windows", "arch": "arm64"},
    {"os": "macos", "arch": "x86_64"},
    {"os": "macos", "arch": "arm64"},
    {"os": "linux", "arch": "x86_64", "libc": "glibc"},
    {"os": "linux", "arch": "arm64", "libc": "glibc"},
    {"os": "linux", "arch": "x86_64", "libc": "musl"},
    {"os": "linux", "arch": "arm64", "libc": "musl"},
]


def _catalog():
    """A minimal but representative Catalog document for ffmpeg."""
    return {
        "kind": "Catalog",
        "schema_version": 1,
        "tool": "ffmpeg",
        "channels": {"latest-stable": "8.0.1"},
        "releases": [
            {
                "version": "8.0.1",
                "platforms": [
                    {
                        "platform": {"os": "windows", "arch": "x86_64"},
                        "asset": {
                            "filename": "win_x64.zip",
                            "sha256": "aa" * 32,
                            "size_bytes": 123,
                            "urls": ["https://cdn.example/ffmpeg/8.0.1/win_x64.zip"],
                        },
                    },
                    {
                        "platform": {"os": "linux", "arch": "x86_64", "libc": "musl"},
                        "asset": {
                            "filename": "linux_x64_musl.zip",
                            "sha256": "bb" * 32,
                            "urls": [
                                "https://cdn.example/ffmpeg/8.0.1/linux_x64_musl.zip"
                            ],
                        },
                    },
                    {
                        "platform": {"os": "linux", "arch": "x86_64", "libc": "glibc"},
                        "asset": {
                            "filename": "linux_x64_glibc217.zip",
                            "sha256": "cc" * 32,
                            "urls": [
                                "https://cdn.example/ffmpeg/8.0.1/linux_x64_glibc217.zip"
                            ],
                        },
                    },
                ],
            }
        ],
    }


class ManifestTester(unittest.TestCase):
    def test_platform_tuple_has_os_and_arch(self) -> None:
        tup = manifest.get_platform_tuple()
        self.assertIn("os", tup)
        self.assertIn("arch", tup)
        # Linux must carry libc so glibc/musl builds can be distinguished.
        if tup["os"] == "linux":
            self.assertIn(tup["libc"], ("glibc", "musl"))

    def test_resolves_musl_vs_glibc(self) -> None:
        cat = _catalog()
        musl = manifest._resolve_asset_from_catalog(
            cat, {"os": "linux", "arch": "x86_64", "libc": "musl"}, "latest-stable"
        )
        glibc = manifest._resolve_asset_from_catalog(
            cat, {"os": "linux", "arch": "x86_64", "libc": "glibc"}, "latest-stable"
        )
        assert musl is not None and glibc is not None
        self.assertIn("musl", musl.url)
        self.assertIn("glibc", glibc.url)
        self.assertEqual(musl.version, "8.0.1")

    def test_resolves_windows(self) -> None:
        asset = manifest._resolve_asset_from_catalog(
            _catalog(), {"os": "windows", "arch": "x86_64"}, "latest-stable"
        )
        assert asset is not None
        self.assertTrue(asset.url.endswith("win_x64.zip"))
        self.assertEqual(asset.sha256, "aa" * 32)

    def test_unknown_platform_returns_none(self) -> None:
        asset = manifest._resolve_asset_from_catalog(
            _catalog(), {"os": "plan9", "arch": "sparc"}, "latest-stable"
        )
        self.assertIsNone(asset)

    def test_disabled_manifest_returns_none(self) -> None:
        # An empty manifest URL means resolution is disabled: it must be a
        # no-op that returns None so the caller falls back to the legacy URL.
        self.assertIsNone(manifest.resolve_asset(url=""))

    def test_default_manifest_url_points_at_ffmpeg_bins2(self) -> None:
        # The published catalog is the ffmpeg-bins2 manifest.
        self.assertIn("ffmpeg-bins2", manifest.DEFAULT_MANIFEST_URL)
        self.assertTrue(manifest.DEFAULT_MANIFEST_URL.endswith("manifest.json"))

    def test_example_manifest_resolves_all_eight_targets(self) -> None:
        # The shipped example manifest documents the client contract; every one
        # of the 8 issue-#20 targets must resolve to a distinct asset URL.
        with open(_EXAMPLE_MANIFEST, "r", encoding="utf-8") as file_d:
            catalog = json.load(file_d)
        urls = set()
        for target in _ALL_TARGETS:
            asset = manifest._resolve_asset_from_catalog(
                catalog, target, "latest-stable"
            )
            self.assertIsNotNone(asset, f"no asset for {target}")
            assert asset is not None
            self.assertTrue(asset.url.startswith("https://"))
            urls.add(asset.url)
        self.assertEqual(len(urls), len(_ALL_TARGETS), "targets must be distinct")

    def test_verify_sha256_ok_and_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "blob.bin")
            data = b"static-ffmpeg-test-payload"
            with open(path, "wb") as file_d:
                file_d.write(data)
            good = hashlib.sha256(data).hexdigest()
            manifest.verify_sha256(path, good)  # should not raise
            manifest.verify_sha256(path, None)  # no checksum -> passes
            with self.assertRaises(ValueError):
                manifest.verify_sha256(path, "00" * 32)


if __name__ == "__main__":
    unittest.main()
