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


LEFT_CROP = "300:100:500:0"
RIGHT_CROP = "300:100:970:0"
GRAY = (0x30, 0x30, 0x30)


def region(number, region_index, start=0):
    return {"number": number, "region": region_index, "file": f"{number}.png", "start": start,
            "row": 0, "column": number - 1}


def test_same_as_points_to_previous_candidate_of_same_region():
    items = [region(1, 0), region(2, 1), region(3, 0), region(4, 1)]
    scores = {("1.png", "3.png"): 45.0, ("2.png", "4.png"): 12.0}
    candidates.mark_same_as(items, lambda a, b: scores[(a, b)])
    assert [c["same_as"] for c in items] == [None, None, 1, None]
    assert [c["psnr"] for c in items] == [None, None, 45.0, 12.0]


def test_same_as_threshold_is_inclusive():
    items = [region(1, 0), region(2, 0)]
    candidates.mark_same_as(items, lambda a, b: candidates.SAME_AS_MIN_DB)
    assert items[1]["same_as"] == 1


def test_map_shows_region_only_with_several_crops_and_same_as_always():
    item = {**region(4, 1, 28), "same_as": 2, "psnr": 45.2}
    assert candidates.format_map([item], 2) == "row 0 column 3: #4 00:00:28 region 1 same-as #2 (45 dB)"
    assert candidates.format_map([item], 1) == "row 0 column 3: #4 00:00:28 same-as #2 (45 dB)"
    assert candidates.format_map([{**item, "same_as": None}], 1) == "row 0 column 3: #4 00:00:28"


def run_regions(video, workdir, segments, *crops):
    (workdir / "segments.json").write_text(json.dumps(segments))
    return run_cli(video, "--workdir", workdir, *[arg for c in crops for arg in ("--crop", c)])


def test_two_crops_cut_each_candidate_from_its_region(synthetic_talk, tmp_path):
    segments = [{"start": 0, "end": 9.96, "region": 0}, {"start": 0, "end": 9.96, "region": 1},
                {"start": 10, "end": 19.96, "region": 0}, {"start": 22, "end": 29, "region": 1}]
    result = run_regions(synthetic_talk, tmp_path, segments, LEFT_CROP, RIGHT_CROP)
    assert result.returncode == 0, result.stderr
    files = [tmp_path / f"candidates/{n:04d}.png" for n in range(1, 5)]
    assert close(pixel(files[0], 10, 10), FIRST_SLIDE)
    assert close(pixel(files[1], 10, 10), GRAY)
    assert close(pixel(files[2], 10, 10), BLUE)
    assert close(pixel(files[3], 10, 10), GRAY)
    assert "region 1" in result.stdout


def test_same_as_set_for_unchanged_region_and_not_after_change(synthetic_talk, tmp_path):
    segments = [{"start": 0, "end": 9.96, "region": 0}, {"start": 0, "end": 9.96, "region": 1},
                {"start": 12, "end": 19.96, "region": 0}, {"start": 12, "end": 19.96, "region": 1}]
    result = run_regions(synthetic_talk, tmp_path, segments, LEFT_CROP, RIGHT_CROP)
    assert result.returncode == 0, result.stderr
    data = json.loads((tmp_path / "candidates.json").read_text())
    assert [c["same_as"] for c in data] == [None, None, None, 2]
    assert data[3]["psnr"] >= candidates.SAME_AS_MIN_DB
    assert data[2]["psnr"] < candidates.SAME_AS_MIN_DB
    assert "same-as #2" in result.stdout


def test_single_crop_map_has_no_region_text(synthetic_talk, tmp_path):
    result = run_regions(synthetic_talk, tmp_path, segs((0, 9.96)), CROP)
    assert result.returncode == 0, result.stderr
    assert "region" not in result.stdout


@pytest.mark.parametrize("segments, crops", [
    (segs((0, 5)), ["300:100:0:0", "200:100:0:0"]),
    ([{"start": 0, "end": 5, "region": 2}], [LEFT_CROP, RIGHT_CROP]),
    ([{"start": 0, "end": 5, "region": 1}], [LEFT_CROP]),
])
def test_bad_crops_or_regions_fail_briefly(synthetic_talk, tmp_path, segments, crops):
    result = run_regions(synthetic_talk, tmp_path, segments, *crops)
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert result.stderr.startswith("error:")
