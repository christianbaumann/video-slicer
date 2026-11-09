import math
import struct
import subprocess
import sys
from pathlib import Path

import pytest

import samples
from conftest import HEIGHT, WIDTH

SCRIPT = Path(samples.__file__)


def png_size(path):
    return struct.unpack(">II", path.read_bytes()[16:24])


def run_script(*args):
    return subprocess.run([sys.executable, SCRIPT, *map(str, args)],
                          capture_output=True, text=True, timeout=120)


def test_sample_times_exclude_start_and_end():
    assert samples.sample_times(130, 12) == pytest.approx(range(10, 130, 10))


def test_samples_and_montage(synthetic_talk, tmp_path):
    result = run_script(synthetic_talk, "--workdir", tmp_path, "--count", 12)
    assert result.returncode == 0, result.stderr
    frames = sorted((tmp_path / "samples").glob("s*.png"))
    assert [f.name for f in frames] == [f"s{n:02d}.png" for n in range(1, 13)]
    assert {png_size(f) for f in frames} == {(WIDTH, HEIGHT)}
    thumb_height = round(samples.THUMBNAIL_WIDTH * HEIGHT / WIDTH)
    rows = math.ceil(12 / samples.MONTAGE_COLUMNS)
    assert png_size(tmp_path / "montage.png") == (
        samples.MONTAGE_COLUMNS * samples.THUMBNAIL_WIDTH, rows * thumb_height)


def test_failure_exits_nonzero_with_short_message(tmp_path):
    broken = tmp_path / "broken.mp4"
    broken.write_text("not a video")
    result = run_script(broken, "--workdir", tmp_path / "work")
    assert result.returncode == 1
    assert result.stderr.startswith("error:")
    assert "Traceback" not in result.stderr
