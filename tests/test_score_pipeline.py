import json
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).parent.parent / ".claude/skills/video-slicer/scripts"
CROPS = ("600:700:20:10", "600:700:660:10")
PAGE_STARTS = [(0, 0), (0, 1), (10, 0), (20, 1), (30, 0), (40, 0), (40, 1)]
PAGE_COLORS = [(0x20, 0x30, 0x40), (0x40, 0x60, 0x40), (0x20, 0x20, 0x80), (0x60, 0x40, 0x60),
               (0x20, 0x40, 0x20), (0x80, 0x20, 0x20), (0x80, 0x60, 0x20)]
START_TOLERANCE = 0.3
COLOR_TOLERANCE = 12
CLI_TIMEOUT = 180


def run_script(name, video, workdir):
    crops = [arg for crop in CROPS for arg in ("--crop", crop)]
    result = subprocess.run([sys.executable, str(SCRIPTS / name), str(video),
                             "--workdir", str(workdir), *crops],
                            capture_output=True, text=True, timeout=CLI_TIMEOUT)
    assert result.returncode == 0, result.stderr
    return result


def pixel(path, x, y):
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"crop=1:1:{x}:{y}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, timeout=30).stdout
    return tuple(out)


def test_two_page_regions_give_one_candidate_per_page_in_reading_order(synthetic_score, tmp_path):
    run_script("detect.py", synthetic_score, tmp_path)
    run_script("candidates.py", synthetic_score, tmp_path)
    data = json.loads((tmp_path / "candidates.json").read_text())
    assert [c["region"] for c in data] == [region for _, region in PAGE_STARTS]
    assert [c["start"] for c in data] == pytest.approx([start for start, _ in PAGE_STARTS],
                                                       abs=START_TOLERANCE)
    assert [c["same_as"] for c in data] == [None] * len(PAGE_STARTS)
    for candidate, expected in zip(data, PAGE_COLORS):
        actual = pixel(tmp_path / candidate["file"], 10, 10)
        assert all(abs(a - b) <= COLOR_TOLERANCE for a, b in zip(actual, expected))
