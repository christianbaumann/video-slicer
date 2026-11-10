---
id: 02
dependencies: []
---

# Task 02: Detect segments per page region

`detect.py` accepts several crop boxes and writes one segment list for all regions, each segment tagged with its region and in reading order.

## References

* `design.md#half-turn-page-pattern`
* `design.md#detectpy`
* `design.md#one-freezedetect-pass-per-region`
* `design.md#repeatable---crop-with-a-region-index`
* Touches: `.claude/skills/video-slicer/scripts/detect.py`, `tests/test_detect.py`, `tests/conftest.py` (new two-page fixture)

## Work

* [ ] Add a session fixture `synthetic_score` to `tests/conftest.py`: two equal page areas side by side that change in turn (left, right, left) and once both at the same moment, with background noise like `synthetic_talk`. Use named constants for page positions and change times
* [ ] Make `--crop` repeatable in `detect.py`; validate each value with `CROP_PATTERN`
* [ ] Run one `freezedetect` pass per crop and tag each segment with `region` (index of the crop on the command line)
* [ ] Sort all segments by `start`, then `region`, and write them to `segments.json`
* [ ] Keep one-crop behaviour: same segments as before, each with `region: 0`
* [ ] Update the unit tests of `parse_segments` and add tests for tagging and ordering (unit level where possible, one CLI test on `synthetic_score`)

## Verification

* [ ] On `synthetic_score` with left and right crops, `segments.json` lists one segment per page change, with the region of the page that changed, in time order
* [ ] At the moment both pages change, the region 0 segment comes before the region 1 segment
* [ ] With one `--crop`, `test_detect_on_synthetic_talk` still finds 4 segments at 0, 5, 10 and 20 s
* [ ] An invalid value in any of several `--crop` arguments exits non-zero with a short message and no traceback
* [ ] `uv run pytest` passes
