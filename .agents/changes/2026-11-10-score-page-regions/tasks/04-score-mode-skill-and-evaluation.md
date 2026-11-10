---
id: 04
dependencies:
- 02
- 03
status: done
owner: s-3c9e
branch: task/2026-11-10-score-page-regions-04
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

* [x] Add `tests/test_score_pipeline.py`: `detect.py` then `candidates.py` with two crops on `synthetic_score`; assert one candidate per page change in reading order **Note:** Asserts 7 candidates (0 L, 0 R, 10 L, 20 R, 30 L, 40 L, 40 R), no `same_as`, colour per page.
* [x] `SKILL.md` steps 1 and 2: two pages side by side means one crop box per page, same size; pass all boxes to steps 3 and 4 **Note:** Step 1 layout check; step 2 one box per page, left first, same `W:H`, corner check per box and at frame edges; steps 3 and 4 repeat `--crop`.
* [x] `SKILL.md` step 5: add the "Scores" subsection (no full page, page-curl frames, `same-as` after a check) and explain the `region` and `same-as` parts of the map **Note:** Scores subsection plus map explanation in step 4. After run 1 it also covers repeats below 40 dB (printed page number decides), a footer-tile recipe, and the cover giving one candidate per region.
* [x] `SKILL.md` defaults: name `.mkv` next to `.mp4` **Note:** Output default names `talk.mp4` or `talk.mkv`.
* [x] Run the skill on the Metal video with a fresh agent; write `results/metal.md` with crop boxes, candidate count, kept count, kept pages against the printed page numbers, and drops with reasons **Note:** Fresh Sonnet agent; run 1 in `results/metal-run1.md`, final run in `results/metal.md`.
* [x] Fix `SKILL.md` wording where the run shows errors; re-run once after a fix **Note:** Run 1 output was correct, but 9 repeats had no `same-as` hint (38 to 41 dB) and the cover/corner-check wording was unclear; fixed, re-run once (run 2). Remaining wording suggestions from run 2 are listed in `results/metal.md` and not applied.
* [x] Update `CLAUDE.md` (pipeline, non-obvious facts, test data) and `README.md` usage **Note:** Pipeline, half-turn pattern, `.mkv` fact, untracked `test-data/` note; README usage paragraph.
* [x] Keep `test-data/` out of git (`.gitignore`) **Note:** `.gitignore` entry `test-data/`.

## Verification

* [x] `tests/test_score_pipeline.py` passes **Note:** Verify subagent: 1 passed.
* [x] The Metal run keeps every printed score page exactly once, in page order, or `results/metal.md` lists each miss or repeat with its cause **Note:** Both runs: printed pages 2 to 36, each once, in order; 35 kept of 82/83 candidates. Verify subagent spot-checked 4 PNG footers.
* [x] The cover is dropped and named in the report **Note:** Candidates #1 and #2 (cover halves) dropped and named in both reports.
* [x] A one-crop run of the existing pipeline still follows the unchanged talk rules (`SKILL.md` diff only adds to them) **Note:** Verified via SKILL.md diff review: only additions plus the `.mkv` Output default line. No full one-crop talk re-run was done.
* [x] `git status` shows no file under `test-data/` **Note:** `git status --short` on main is empty after merge; `git check-ignore` matches `test-data/`.
* [x] `uv run pytest` passes **Note:** 50 passed on the rebased state.
