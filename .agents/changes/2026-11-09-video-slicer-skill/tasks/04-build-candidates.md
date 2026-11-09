---
id: 04
dependencies:
- 01
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

* [ ] Add a pure function that maps segments to candidate records with `number`, `start`, `frame_time` (`max(start, end - 0.5)`), `file`, `row` and `column`
* [ ] Add `candidates.py <video> --workdir <dir> --crop W:H:X:Y` that reads `segments.json` and writes `candidates/0001.png`, ..., `contact-sheet.png` and `candidates.json`
* [ ] Build the sheet with the ffmpeg `tile` filter. Thumbnail width and column count are named constants
* [ ] Print the map from grid position to candidate number and timestamp to stdout
* [ ] Add unit tests for the mapping and an integration test with a hand-written `segments.json` and `synthetic_talk`

## Verification

* [ ] A segment of 5.0 to 9.96 s has `frame_time` 9.46
* [ ] A segment shorter than 0.5 s has `frame_time` equal to its `start`
* [ ] With 9 segments and 8 columns, candidate 9 has `row` 1 and `column` 0
* [ ] Candidate PNGs have the crop dimensions, and one candidate from the 10 s to 20 s segment is blue
* [ ] A missing or empty `segments.json` exits with a nonzero status and a short error message
* [ ] `uv run pytest` passes
