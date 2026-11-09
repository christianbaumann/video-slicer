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
