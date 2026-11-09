---
id: 02
dependencies:
- 01
status: done
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

* [x] Add a pure function that computes `count` evenly spaced timestamps from a duration, excluding the start and the end of the video. **Note:** `sample_times(duration, count)`.
* [x] Add `samples.py <video> --workdir <dir> [--count 12]` that writes `samples/s01.png`, ... and `montage.png`. **Note:** Stale `sNN.png` files stay if a later run in the same workdir uses a smaller `--count`; the montage still uses only the current samples.
* [x] Build the montage with the ffmpeg `tile` filter. Thumbnail width and column count are named constants. **Note:** `THUMBNAIL_WIDTH=480`, `MONTAGE_COLUMNS=4`.
* [x] Add unit tests for the timestamps and an integration test with `synthetic_talk`

## Verification

* [x] For a duration of 130 s and `--count 12`, timestamps are 10, 20, ... 120 s. **Note:** Verified via `test_sample_times_exclude_start_and_end`, and by a separate verifier reading burned-in clock labels in a montage from the CLI.
* [x] With `synthetic_talk`, `--count 12` writes 12 PNGs at 1280x720. **Note:** Verified via the integration test and a CLI run started from `/`.
* [x] `montage.png` exists and has the expected grid dimensions. **Note:** Verified at 1920x810 (4x3 tiles of 480x270), and the verifier viewed the grid.
* [x] A failed ffmpeg call exits with a nonzero status and a short error message. **Note:** Verified with a garbage `.mp4` and a missing file: exit 1, one-line `error:` message, no traceback.
* [x] `uv run pytest` passes. **Note:** Verified by a separate verifier on the rebased branch: 8 passed.
