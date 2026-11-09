import json
import subprocess
import sys
from pathlib import Path

import pytest

import candidates
from media import run_ffmpeg

SCRIPT = Path(candidates.__file__)
CROP = "800:600:50:40"
CLI_TIMEOUT = 180
BLUE = (0x20, 0x20, 0x80)
COLOR_TOLERANCE = 12


def segs(*pairs):
    return [{"start": s, "end": e} for s, e in pairs]


def test_frame_time_is_half_second_before_end():
    assert candidates.build_candidates(segs((5.0, 9.96)))[0]["frame_time"] == 9.46


def test_frame_time_of_short_segment_is_start():
    assert candidates.build_candidates(segs((5.0, 5.3)))[0]["frame_time"] == 5.0


def test_ninth_candidate_wraps_to_second_row():
    result = candidates.build_candidates(segs(*[(i * 3, i * 3 + 2) for i in range(9)]), columns=8)
    assert (result[8]["number"], result[8]["row"], result[8]["column"]) == (9, 1, 0)
    assert result[8]["file"] == "candidates/0009.png"


def run_cli(*args):
    return subprocess.run([sys.executable, str(SCRIPT), *map(str, args)],
                          capture_output=True, text=True, timeout=CLI_TIMEOUT)


def pixel(path, x, y):
    out = subprocess.run(
        ["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"crop=1:1:{x}:{y}",
         "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
        capture_output=True, timeout=30).stdout
    return tuple(out)


def test_cli_writes_cropped_frames_sheet_and_map(synthetic_talk, tmp_path):
    (tmp_path / "segments.json").write_text(json.dumps(segs((0, 9.96), (10, 19.96), (20, 30))))
    result = run_cli(synthetic_talk, "--workdir", tmp_path, "--crop", CROP)
    assert result.returncode == 0, result.stderr
    assert "row 0 column 1: #2 00:00:10" in result.stdout
    data = json.loads((tmp_path / "candidates.json").read_text())
    assert [c["number"] for c in data] == [1, 2, 3]
    assert (tmp_path / "contact-sheet.png").exists()
    blue = tmp_path / data[1]["file"]
    size = run_ffmpeg(["-i", blue, "-f", "null", "-"], 30)
    assert "800x600" in size
    assert all(abs(a - b) <= COLOR_TOLERANCE for a, b in zip(pixel(blue, 10, 10), BLUE))


def test_contact_sheet_holds_many_candidates(synthetic_talk, tmp_path):
    count = 50
    (tmp_path / "segments.json").write_text(
        json.dumps(segs(*[(i * 0.5, i * 0.5 + 1) for i in range(count)])))
    assert run_cli(synthetic_talk, "--workdir", tmp_path, "--crop", CROP).returncode == 0
    info = run_ffmpeg(["-i", tmp_path / "contact-sheet.png", "-f", "null", "-"], 30)
    cols, rows = candidates.GRID_COLUMNS, 7
    width = candidates.THUMBNAIL_WIDTH * cols
    assert f"{width}x{rows * 240}" in info


@pytest.mark.parametrize("content", [None, "[]", "not json"])
def test_bad_segments_file_fails_briefly(synthetic_talk, tmp_path, content):
    if content is not None:
        (tmp_path / "segments.json").write_text(content)
    result = run_cli(synthetic_talk, "--workdir", tmp_path, "--crop", CROP)
    assert result.returncode != 0
    assert "Traceback" not in result.stderr
    assert result.stderr.startswith("error:")


ODD_CROP = "801:601:3:5"
FIRST_SLIDE = (0x20, 0x30, 0x40)
THIRD_SLIDE = (0x20, 0x40, 0x20)
BLACK = (0, 0, 0)
TILE_INSET = 10


def tile_pixel(workdir, row, column):
    height = candidates.THUMBNAIL_WIDTH * 3 // 4
    return pixel(workdir / "contact-sheet.png",
                 column * candidates.THUMBNAIL_WIDTH + TILE_INSET, row * height + TILE_INSET)


def close(actual, expected):
    return all(abs(a - b) <= COLOR_TOLERANCE for a, b in zip(actual, expected))


def run_with_segments(video, workdir, segments, crop=CROP):
    (workdir / "segments.json").write_text(json.dumps(segments))
    result = run_cli(video, "--workdir", workdir, "--crop", crop)
    assert result.returncode == 0, result.stderr


def test_rerun_with_fewer_segments_drops_stale_frames(synthetic_talk, tmp_path):
    run_with_segments(synthetic_talk, tmp_path, segs(*[(11 + i, 12 + i) for i in range(4)]))
    run_with_segments(synthetic_talk, tmp_path, segs((21, 22), (23, 24)))
    assert sorted(p.name for p in (tmp_path / "candidates").glob("*.png")) == ["0001.png", "0002.png"]
    assert close(tile_pixel(tmp_path, 0, 1), THIRD_SLIDE)
    assert close(tile_pixel(tmp_path, 0, 2), BLACK)


def test_odd_crop_keeps_exact_dimensions(synthetic_talk, tmp_path):
    run_with_segments(synthetic_talk, tmp_path, segs((0, 9.96)), ODD_CROP)
    info = run_ffmpeg(["-i", tmp_path / "candidates" / "0001.png", "-f", "null", "-"], 30)
    assert "801x601" in info


def test_partly_filled_last_row_maps_tiles_by_colour(synthetic_talk, tmp_path):
    first_row = [(i, i + 1) for i in range(8)]
    run_with_segments(synthetic_talk, tmp_path, segs(*first_row, (21, 22)))
    assert close(tile_pixel(tmp_path, 0, 7), FIRST_SLIDE)
    assert close(tile_pixel(tmp_path, 1, 0), THIRD_SLIDE)
    assert close(tile_pixel(tmp_path, 1, 1), BLACK)
