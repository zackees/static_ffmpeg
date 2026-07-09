"""End-to-end encode test.

Guarantees that, on every platform CI runs on, the resolved ffmpeg binary can
actually encode a small video and that ffprobe can read it back. This is the
"small test encoding file" check from issue #20 -- it exercises the real codec
path, not just ``-version``.
"""

import json
import os
import subprocess
import tempfile
import unittest

from static_ffmpeg import run


class EncodeTester(unittest.TestCase):
    def setUp(self) -> None:
        self.ffmpeg, self.ffprobe = (
            run.get_or_fetch_platform_executables_else_raise()
        )

    def test_encode_and_probe_small_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            out = os.path.join(tmp, "out.mp4")
            # Synthesize 1 second of 320x240 test video + a sine tone and encode
            # to H.264/AAC in an mp4 container. Fully self-contained (lavfi
            # sources), so no input asset is required.
            cmd = [
                self.ffmpeg,
                "-y",
                "-f", "lavfi", "-i", "testsrc=size=320x240:rate=15:duration=1",
                "-f", "lavfi", "-i", "sine=frequency=440:duration=1",
                "-c:v", "libx264", "-preset", "ultrafast", "-pix_fmt", "yuv420p",
                "-c:a", "aac",
                "-shortest",
                out,
            ]
            subprocess.check_call(cmd)

            self.assertTrue(os.path.exists(out), "encoder produced no output file")
            self.assertGreater(os.path.getsize(out), 0, "encoded file is empty")

            # Probe it back and assert we have a real video stream.
            probe = subprocess.check_output(
                [
                    self.ffprobe,
                    "-v", "error",
                    "-show_streams",
                    "-of", "json",
                    out,
                ]
            )
            info = json.loads(probe)
            codecs = {s.get("codec_type") for s in info.get("streams", [])}
            self.assertIn("video", codecs, "no video stream in encoded output")


if __name__ == "__main__":
    unittest.main()
