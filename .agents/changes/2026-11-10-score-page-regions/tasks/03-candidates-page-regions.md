---
id: 03
dependencies: []
status: done
owner: s-3c9e
branch: task/2026-11-10-score-page-regions-03
---

# Task 03: Candidates per page region with same-as hint

`candidates.py` crops each candidate frame with its region's crop box and marks candidates that repeat the previous candidate of the same region, so review sees one thumbnail per page and the likely repeats.

## References

* `design.md#candidatespy`
* `design.md#crop-boxes-must-have-equal-size`
* `design.md#same-as-hint-decision-stays-with-claude`
* Touches: `.claude/skills/video-slicer/scripts/candidates.py`, `tests/test_candidates.py`
* Reads only: `tests/conftest.py` (`synthetic_talk`), `.claude/skills/video-slicer/scripts/media.py`

## Work

* [x] Make `--crop` repeatable; reject crops with different `W:H` and segments whose `region` has no crop. A segment without `region` counts as region 0 **Note:** `validate_crops`; verified via parametrized `test_bad_crops_or_regions_fail_briefly`; missing `region` read as 0.
* [x] Crop each candidate frame with the crop of its segment's region; store `region` in each candidate **Note:** Verified via `test_two_crops_cut_each_candidate_from_its_region`.
* [x] Compute PSNR against the previous candidate of the same region (ffmpeg `psnr`, via `run_ffmpeg`); store `psnr` and `same_as` with `SAME_AS_MIN_DB = 40`; `null` for the first candidate of a region **Note:** Unit tests with injected measure (`test_same_as_points_to_previous_candidate_of_same_region`, `test_same_as_threshold_is_inclusive`) plus CLI test with real ffmpeg. PSNR capped at `PSNR_MAX_DB = 100` because ffmpeg prints `inf` for identical frames; stored to 1 decimal.
* [x] Extend `format_map`: show `region N` only with 2 or more crops; show `same-as #N (D dB)` in every mode **Note:** `format_map(candidates, crop_count=1)`; verified via `test_map_shows_region_only_with_several_crops_and_same_as_always`.
* [x] Write tests: unit tests for map formatting and same-as selection, CLI tests with hand-written `segments.json` on `synthetic_talk` using two crop boxes at different positions **Note:** Unit and CLI tests in `tests/test_candidates.py`.

## Verification

* [x] With two crops, each candidate PNG shows the content of its own region (pixel check against the fixture colours) **Note:** Pixel check against `FIRST_SLIDE`, `BLUE`, `GRAY` in `test_two_crops_cut_each_candidate_from_its_region`.
* [x] Two candidates of one region with unchanged content get `same_as` set; a candidate after a content change does not **Note:** `test_same_as_set_for_unchanged_region_and_not_after_change` gives `same_as` `[None, None, None, 2]`.
* [x] Crops with different `W:H`, or a segment with `region: 2` and two crops, exit 1 with a short message and no traceback **Note:** `test_bad_crops_or_regions_fail_briefly`: exit 1, stderr starts with `error:`, no traceback.
* [x] With one crop, the map has no `region` text and `test_cli_writes_cropped_frames_sheet_and_map` still passes **Note:** `test_single_crop_map_has_no_region_text`; `test_cli_writes_cropped_frames_sheet_and_map` passes.
* [x] `uv run pytest` passes **Note:** 49 passed on the rebased state including tasks 01 and 02.
