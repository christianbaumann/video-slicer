---
id: 03
dependencies:
- 01
status: done
owner: s-a41c
branch: task/2026-11-09-video-slicer-skill-03
---

# Task 03: Detect segments

`detect.py` finds the stable segments in the cropped video and writes `segments.json`.

## References

* `design.md#change-detection`
* `design.md#detection-settings`
* `design.md#file-structure-and-interfaces`
* Touches: `.claude/skills/video-slicer/scripts/detect.py`, `tests/test_detect.py`

## Work

* [x] Add a pure function that parses `freeze_start` and `freeze_end` from `metadata=print` output into segments. **Note:** `parse_segments(output, duration)` reads the `lavfi.freezedetect.freeze_*=` lines and ignores the `freeze_start: X` log lines.
* [x] Set the `end` of a last segment that has no `freeze_end` to the video duration
* [x] Add `detect.py <video> --workdir <dir> --crop W:H:X:Y [--noise-db -50] [--min-seconds 2]` that writes `segments.json`
* [x] Keep the defaults as named constants, and use a timeout that allows a full-length talk. **Note:** `DEFAULT_NOISE_DB`, `DEFAULT_MIN_SECONDS`, `DETECT_TIMEOUT = 3600`.
* [x] Validate the `--crop` format
* [x] Add unit tests for the parser and an integration test with `synthetic_talk`. **Note:** 7 tests in `tests/test_detect.py`.

## Verification

* [x] The parser returns the correct segments for a captured output sample. **Note:** Verified via the parser test on real ffmpeg output; a separate verifier reproduced the same lines from a new clip.
* [x] A last segment with no `freeze_end` ends at the video duration. **Note:** Verified via the parser test and a CLI run: `[{start:0.0,end:2.8},{start:2.8,end:7.0}]`.
* [x] With `synthetic_talk` and crop `960:720:0:0`, `segments.json` has 4 segments with boundaries near 5 s, 10 s and 20 s. **Note:** Verified via `test_detect_on_synthetic_talk`.
* [x] Movement outside the crop does not add segments. **Note:** Verified via `test_movement_outside_crop_adds_no_segments`.
* [x] An invalid `--crop` value exits with a nonzero status and a short error message. **Note:** Verified via the parametrized test and the CLI: exit 2, no traceback, nothing written.
* [x] `uv run pytest` passes. **Note:** Verified on the rebased branch: 15 passed.

Additional check: the real recording with crop `1320:740:100:170` and defaults took 32 s and gave 52 segments, matching `design.md#evaluation`. The `--noise-db` and `--min-seconds` overrides were confirmed by hand and have no regression test.
