---
id: 04
dependencies:
- 01
status: done
owner: s-a41c
branch: task/2026-11-09-video-slicer-skill-04
---

# Task 04: Build candidates

`candidates.py` turns `segments.json` into cropped candidate frames, one contact sheet and a grid map, so Claude can review all candidates at once.

## References

* `design.md#frame-to-keep`
* `design.md#candidate-review`
* `design.md#contact-sheet-labels`
* `design.md#file-structure-and-interfaces`
* Touches: `.claude/skills/video-slicer/scripts/candidates.py`, `tests/test_candidates.py`

## Work

* [x] Add a pure function that maps segments to candidate records with `number`, `start`, `frame_time` (`max(start, end - 0.5)`), `file`, `row` and `column`. **Note:** `build_candidates(segments, columns)`; `frame_time` is rounded to 3 decimals.
* [x] Add `candidates.py <video> --workdir <dir> --crop W:H:X:Y` that reads `segments.json` and writes `candidates/0001.png`, ..., `contact-sheet.png` and `candidates.json`. **Note:** Earlier `candidates/*.png` are removed first, so a rerun with fewer segments shows no stale tiles. `format=rgb24` before `crop` keeps odd sizes and offsets exact.
* [x] Build the sheet with the ffmpeg `tile` filter. Thumbnail width and column count are named constants. **Note:** `THUMBNAIL_WIDTH=320`, `GRID_COLUMNS=8`.
* [x] Print the map from grid position to candidate number and timestamp to stdout. **Note:** Lines look like `row 0 column 1: #2 00:00:10`.
* [x] Add unit tests for the mapping and an integration test with a hand-written `segments.json` and `synthetic_talk`

## Verification

* [x] A segment of 5.0 to 9.96 s has `frame_time` 9.46. **Note:** Verified via unit test.
* [x] A segment shorter than 0.5 s has `frame_time` equal to its `start`. **Note:** Verified via unit test.
* [x] With 9 segments and 8 columns, candidate 9 has `row` 1 and `column` 0. **Note:** Verified via unit test and a CLI run.
* [x] Candidate PNGs have the crop dimensions, and one candidate from the 10 s to 20 s segment is blue. **Note:** Verified via the integration test. A separate verifier also confirmed 801x601 and 1322x741 crops with exact offsets by pixel value.
* [x] A missing or empty `segments.json` exits with a nonzero status and a short error message. **Note:** Verified via a parametrized test and the CLI: exit 1, one-line error, no traceback.
* [x] `uv run pytest` passes. **Note:** Verified by a separate verifier on the rebased branch: 33 passed.
