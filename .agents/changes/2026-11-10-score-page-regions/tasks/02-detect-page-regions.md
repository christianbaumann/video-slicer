---
id: 02
dependencies: []
status: done
owner: s-3c9e
branch: task/2026-11-10-score-page-regions-02
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

* [x] Add a session fixture `synthetic_score` to `tests/conftest.py`: two equal page areas side by side that change in turn (left, right, left) and once both at the same moment, with background noise like `synthetic_talk`. Use named constants for page positions and change times **Note:** `synthetic_score`: 50 s, two 600x700 pages with noise; left changes at 0/10/30/40 s, right at 0/20/40 s.
* [x] Make `--crop` repeatable in `detect.py`; validate each value with `CROP_PATTERN` **Note:** Verified via `test_invalid_crop_among_several_exits_nonzero` and the parametrized invalid-crop test.
* [x] Run one `freezedetect` pass per crop and tag each segment with `region` (index of the crop on the command line) **Note:** Verified via `test_detect_on_synthetic_score_with_two_regions`.
* [x] Sort all segments by `start`, then `region`, and write them to `segments.json` **Note:** Verified via `test_tag_and_sort_orders_by_start_then_region` and the CLI test.
* [x] Keep one-crop behaviour: same segments as before, each with `region: 0` **Note:** `test_detect_on_synthetic_talk` now also asserts `region: 0`.
* [x] Update the unit tests of `parse_segments` and add tests for tagging and ordering (unit level where possible, one CLI test on `synthetic_score`) **Note:** `parse_segments` unchanged, so its tests unchanged; new unit tests for `tag_and_sort` plus one CLI test on `synthetic_score`.

## Verification

* [x] On `synthetic_score` with left and right crops, `segments.json` lists one segment per page change, with the region of the page that changed, in time order **Note:** Verified via `test_detect_on_synthetic_score_with_two_regions` (region 0 starts 0/10/30/40 s, region 1 starts 0/20/40 s, tolerance 0.3 s, sorted).
* [x] At the moment both pages change, the region 0 segment comes before the region 1 segment **Note:** Same test asserts regions `[0, 1]` for segments starting after 39 s.
* [x] With one `--crop`, `test_detect_on_synthetic_talk` still finds 4 segments at 0, 5, 10 and 20 s **Note:** Verified via `test_detect_on_synthetic_talk`.
* [x] An invalid value in any of several `--crop` arguments exits non-zero with a short message and no traceback **Note:** Verified via `test_invalid_crop_among_several_exits_nonzero`; manual CLI run gave rc=2 and a one-line argparse error.
* [x] `uv run pytest` passes **Note:** 37 passed (verify subagent, rebased state).
