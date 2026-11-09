---
id: 03
dependencies:
- 01
---

# Task 03: Detect segments

`detect.py` finds the stable segments in the cropped video and writes `segments.json`.

## References

* `design.md#change-detection`
* `design.md#detection-settings`
* `design.md#file-structure-and-interfaces`
* Touches: `.claude/skills/video-slicer/scripts/detect.py`, `tests/test_detect.py`

## Work

* [ ] Add a pure function that parses `freeze_start` and `freeze_end` from `metadata=print` output into segments
* [ ] Set the `end` of a last segment that has no `freeze_end` to the video duration
* [ ] Add `detect.py <video> --workdir <dir> --crop W:H:X:Y [--noise-db -50] [--min-seconds 2]` that writes `segments.json`
* [ ] Keep the defaults as named constants, and use a timeout that allows a full-length talk
* [ ] Validate the `--crop` format
* [ ] Add unit tests for the parser and an integration test with `synthetic_talk`

## Verification

* [ ] The parser returns the correct segments for a captured output sample
* [ ] A last segment with no `freeze_end` ends at the video duration
* [ ] With `synthetic_talk` and crop `960:720:0:0`, `segments.json` has 4 segments with boundaries near 5 s, 10 s and 20 s
* [ ] Movement outside the crop does not add segments
* [ ] An invalid `--crop` value exits with a nonzero status and a short error message
* [ ] `uv run pytest` passes
