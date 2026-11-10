---
id: 04
dependencies:
- 02
- 03
---

# Task 04: Score mode in SKILL.md and evaluation on the Metal video

The skill tells Claude when and how to use page regions and how to review score pages. A run on the Metal video yields each score page once, in order.

## References

* `design.md#target-behaviour`
* `design.md#skillmd`
* `design.md#claude-decides-on-score-mode-from-the-montage`
* `design.md#cover-cut-in-half-is-dropped`
* `design.md#evaluation`
* Touches: `.claude/skills/video-slicer/SKILL.md`, `CLAUDE.md`, `README.md`, `.gitignore`, `tests/test_score_pipeline.py` (new), `.agents/changes/2026-11-10-score-page-regions/results/` (new)
* Reads only: `tests/conftest.py` (`synthetic_score` from task 02), `test-data/Metal_arranged_by_Sean_O_Loughlin-[oumRCgkJAIU].mkv`

## Work

* [ ] Add `tests/test_score_pipeline.py`: `detect.py` then `candidates.py` with two crops on `synthetic_score`; assert one candidate per page change in reading order
* [ ] `SKILL.md` steps 1 and 2: two pages side by side means one crop box per page, same size; pass all boxes to steps 3 and 4
* [ ] `SKILL.md` step 5: add the "Scores" subsection (no full page, page-curl frames, `same-as` after a check) and explain the `region` and `same-as` parts of the map
* [ ] `SKILL.md` defaults: name `.mkv` next to `.mp4`
* [ ] Run the skill on the Metal video with a fresh agent; write `results/metal.md` with crop boxes, candidate count, kept count, kept pages against the printed page numbers, and drops with reasons
* [ ] Fix `SKILL.md` wording where the run shows errors; re-run once after a fix
* [ ] Update `CLAUDE.md` (pipeline, non-obvious facts, test data) and `README.md` usage
* [ ] Keep `test-data/` out of git (`.gitignore`)

## Verification

* [ ] `tests/test_score_pipeline.py` passes
* [ ] The Metal run keeps every printed score page exactly once, in page order, or `results/metal.md` lists each miss or repeat with its cause
* [ ] The cover is dropped and named in the report
* [ ] A one-crop run of the existing pipeline still follows the unchanged talk rules (`SKILL.md` diff only adds to them)
* [ ] `git status` shows no file under `test-data/`
* [ ] `uv run pytest` passes
