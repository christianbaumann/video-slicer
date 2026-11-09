import json
import subprocess
import sys
from pathlib import Path

import pytest

from detect import parse_segments

DETECT = Path(__file__).parent.parent / ".claude/skills/video-slicer/scripts/detect.py"
CROP = "960:720:0:0"

# Captured from ffmpeg: freezedetect + metadata=print on a 7 s clip that changes at 2.8 s.
SAMPLE_OUTPUT = """\
[Parsed_metadata_1 @ 0x9d101cd80] frame:50   pts:50      pts_time:2
[Parsed_metadata_1 @ 0x9d101cd80] lavfi.freezedetect.freeze_start=0
[Parsed_metadata_1 @ 0x9d101cd80] frame:70   pts:70      pts_time:2.8
[Parsed_metadata_1 @ 0x9d101cd80] lavfi.freezedetect.freeze_duration=2.8
[Parsed_metadata_1 @ 0x9d101cd80] lavfi.freezedetect.freeze_end=2.8
[Parsed_metadata_1 @ 0x9d101cd80] frame:120  pts:120     pts_time:4.8
[Parsed_metadata_1 @ 0x9d101cd80] lavfi.freezedetect.freeze_start=2.8
"""


def run_detect(*args):
    return subprocess.run(
        [sys.executable, DETECT, *map(str, args)], capture_output=True, text=True, timeout=120
    )


def test_parse_segments_from_captured_output():
    assert parse_segments(SAMPLE_OUTPUT, 7.0) == [
        {"start": 0.0, "end": 2.8},
        {"start": 2.8, "end": 7.0},
    ]


def test_parse_segments_without_freezes_is_empty():
    assert parse_segments("frame:1 pts_time:0.04", 7.0) == []


def test_detect_on_synthetic_talk(synthetic_talk, tmp_path):
    result = run_detect(synthetic_talk, "--workdir", tmp_path, "--crop", CROP)
    assert result.returncode == 0, result.stderr
    segments = json.loads((tmp_path / "segments.json").read_text())
    assert len(segments) == 4
    assert [s["start"] for s in segments] == pytest.approx([0, 5, 10, 20], abs=0.3)
    assert segments[-1]["end"] == pytest.approx(30, abs=0.5)


def test_movement_outside_crop_adds_no_segments(synthetic_talk, tmp_path):
    result = run_detect(synthetic_talk, "--workdir", tmp_path, "--crop", "1280:720:0:0")
    assert result.returncode == 0, result.stderr
    assert json.loads((tmp_path / "segments.json").read_text()) == []


@pytest.mark.parametrize("crop", ["960x720+0+0", "960:720:0", "a:b:c:d"])
def test_invalid_crop_exits_nonzero_with_short_message(crop, tmp_path):
    result = run_detect("video.mp4", "--workdir", tmp_path, "--crop", crop)
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
    assert "--crop" in result.stderr
