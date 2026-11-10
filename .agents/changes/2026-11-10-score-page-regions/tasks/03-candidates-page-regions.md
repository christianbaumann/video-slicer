---
id: 03
dependencies: []
status: in-progress
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

* [ ] Make `--crop` repeatable; reject crops with different `W:H` and segments whose `region` has no crop. A segment without `region` counts as region 0
* [ ] Crop each candidate frame with the crop of its segment's region; store `region` in each candidate
* [ ] Compute PSNR against the previous candidate of the same region (ffmpeg `psnr`, via `run_ffmpeg`); store `psnr` and `same_as` with `SAME_AS_MIN_DB = 40`; `null` for the first candidate of a region
* [ ] Extend `format_map`: show `region N` only with 2 or more crops; show `same-as #N (D dB)` in every mode
* [ ] Write tests: unit tests for map formatting and same-as selection, CLI tests with hand-written `segments.json` on `synthetic_talk` using two crop boxes at different positions

## Verification

* [ ] With two crops, each candidate PNG shows the content of its own region (pixel check against the fixture colours)
* [ ] Two candidates of one region with unchanged content get `same_as` set; a candidate after a content change does not
* [ ] Crops with different `W:H`, or a segment with `region: 2` and two crops, exit 1 with a short message and no traceback
* [ ] With one crop, the map has no `region` text and `test_cli_writes_cropped_frames_sheet_and_map` still passes
* [ ] `uv run pytest` passes
