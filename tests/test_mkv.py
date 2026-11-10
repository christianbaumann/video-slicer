import json
import subprocess
import sys
from pathlib import Path

import pytest

import detect
import samples
from conftest import GENERATION_TIMEOUT, HEIGHT, WIDTH
from media import probe_duration, run_ffmpeg

SCRIPTS = Path(detect.__file__).parent
DURATION = 12
CHANGE_TIME = 6
FIRST_COLOR = "0x203040"
SECOND_COLOR = "0x202080"
FULL_CROP = f"{WIDTH}:{HEIGHT}:0:0"
SAMPLE_COUNT = 4


@pytest.fixture(scope="module")
def mkv_video(tmp_path_factory):
    path = tmp_path_factory.mktemp("mkv") / "talk.mkv"
    graph = (f"drawbox=x=0:y=0:w={WIDTH}:h={HEIGHT}:color={SECOND_COLOR}:t=fill"
             f":enable='gte(t,{CHANGE_TIME})'")
    run_ffmpeg(
        ["-f", "lavfi", "-i",
         f"color=c={FIRST_COLOR}:s={WIDTH}x{HEIGHT}:r=10:d={DURATION}",
         "-vf", graph, "-pix_fmt", "yuv420p", path],
        GENERATION_TIMEOUT,
    )
    return path


def run_script(module, *args):
    return subprocess.run([sys.executable, SCRIPTS / f"{module}.py", *map(str, args)],
                          capture_output=True, text=True, timeout=120)


def test_probe_duration_of_mkv(mkv_video):
    assert probe_duration(mkv_video) == pytest.approx(DURATION, abs=0.5)


def test_samples_run_on_mkv(mkv_video, tmp_path):
    result = run_script("samples", mkv_video, "--workdir", tmp_path, "--count", SAMPLE_COUNT)
    assert result.returncode == 0, result.stderr
    assert len(list((tmp_path / "samples").glob("s*.png"))) == SAMPLE_COUNT
    assert (tmp_path / "montage.png").exists()


def test_detect_finds_segments_on_mkv(mkv_video, tmp_path):
    result = run_script("detect", mkv_video, "--workdir", tmp_path, "--crop", FULL_CROP)
    assert result.returncode == 0, result.stderr
    segments = json.loads((tmp_path / "segments.json").read_text())
    assert [s["start"] for s in segments] == pytest.approx([0, CHANGE_TIME], abs=0.3)
    assert segments[-1]["end"] == pytest.approx(DURATION, abs=0.5)
