---
id: 02
dependencies:
- 01
status: in-progress
owner: s-a41c
branch: task/2026-11-09-video-slicer-skill-02
---

# Task 02: Sample frames

`samples.py` writes evenly spaced full-size frames and one montage, so Claude can find the crop box.

## References

* `design.md#crop-box`
* `design.md#file-structure-and-interfaces`
* Touches: `.claude/skills/video-slicer/scripts/samples.py`, `tests/test_samples.py`

## Work

* [ ] Add a pure function that computes `count` evenly spaced timestamps from a duration, excluding the start and the end of the video
* [ ] Add `samples.py <video> --workdir <dir> [--count 12]` that writes `samples/s01.png`, ... and `montage.png`
* [ ] Build the montage with the ffmpeg `tile` filter. Thumbnail width and column count are named constants
* [ ] Add unit tests for the timestamps and an integration test with `synthetic_talk`

## Verification

* [ ] For a duration of 130 s and `--count 12`, timestamps are 10, 20, ... 120 s
* [ ] With `synthetic_talk`, `--count 12` writes 12 PNGs at 1280x720
* [ ] `montage.png` exists and has the expected grid dimensions
* [ ] A failed ffmpeg call exits with a nonzero status and a short error message
* [ ] `uv run pytest` passes
