import pytest

from media import MediaToolError, probe_duration, run_ffmpeg


def test_probe_duration_of_synthetic_talk(synthetic_talk):
    assert probe_duration(synthetic_talk) == pytest.approx(30, abs=0.5)


def test_probe_duration_of_missing_file_raises_without_traceback(tmp_path):
    with pytest.raises(MediaToolError) as error:
        probe_duration(tmp_path / "missing.mp4")
    assert "Traceback" not in str(error.value)


def test_run_ffmpeg_failure_raises(tmp_path):
    with pytest.raises(MediaToolError):
        run_ffmpeg(["-i", tmp_path / "missing.mp4", tmp_path / "out.png"], 10)


def test_run_ffmpeg_timeout_raises(tmp_path):
    args = ["-f", "lavfi", "-i", "testsrc=s=1920x1080:d=600", "-f", "null", "-"]
    with pytest.raises(MediaToolError, match="timed out"):
        run_ffmpeg(args, 0.5)


def _speaker_centroid_x(video, time, tmp_path):
    raw = tmp_path / f"strip{time}.rgb"
    width, height = 320, 240
    run_ffmpeg(["-ss", time, "-i", video, "-frames:v", 1,
                "-vf", f"crop={width}:{height}:960:200",
                "-pix_fmt", "rgb24", "-f", "rawvideo", raw], 20)
    data = raw.read_bytes()
    columns = [
        x for i in range(0, len(data), 3)
        for x in [(i // 3) % width]
        if data[i] > 180 and 140 < data[i + 1] < 220 and data[i + 2] < 160
    ]
    assert columns, "no speaker pixels right of x=960"
    return sum(columns) / len(columns)


def test_speaker_box_moves_right_of_slide_area(synthetic_talk, tmp_path):
    early = _speaker_centroid_x(synthetic_talk, 2, tmp_path)
    late = _speaker_centroid_x(synthetic_talk, 20, tmp_path)
    assert late - early > 100
