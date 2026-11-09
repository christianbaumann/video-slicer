---
id: 04
dependencies:
- 01
- 02
- 03
status: in-progress
owner: s-9c2e
branch: task/2026-11-09-second-video-evaluation-04
---

# Task 04: Fix loop and final results

The skill is improved where the baseline shows errors, and the final results show the effect on both recordings.

## References

* `design.md#evaluation-loop`
* `design.md#result-format`
* `design.md#targets`
* `design.md#change-method`
* `design.md#fixes-only-with-evidence`
* `design.md#results`
* `design.md#open-points`
* `results/baseline-video-1.md`, `results/baseline-video-2.md`
* Touches: `.claude/skills/video-slicer/SKILL.md`, `.agents/changes/2026-11-09-second-video-evaluation/results/after-fixes.md`, `CLAUDE.md`, `README.md`
* Touches only if the baseline shows the need: `.claude/skills/video-slicer/scripts/detect.py`, `.claude/skills/video-slicer/scripts/candidates.py`, and their files in `tests/`

## Work

* [ ] Group the errors of both baselines by pipeline step, and order the steps by error count
* [ ] Apply one fix at a time, for the largest error class first. Re-run both videos after each fix, with task 03 as the first change to measure
* [ ] Change `detect.py` settings only for detection errors. Make the review in groups a `SKILL.md` change only if task 02 shows that the contact sheet size caused review errors
* [ ] Add unit tests before any script change
* [ ] Run the final skill twice per video, with fresh agents and a fresh judge per run, and write `results/after-fixes.md` in the result format, with a comparison to the baseline
* [ ] Update the non-obvious facts in `CLAUDE.md` and the usage in `README.md` where the fixes change them

## Verification

* [ ] Each final run has no missed slide among the slides shown, or `results/after-fixes.md` lists each remaining miss with its cause
* [ ] Each final run has at most 2 extra PNGs per video, or the results list the excess with its cause
* [ ] Each final run passes the crop check
* [ ] No fix made the other video worse than its baseline, and the results show the numbers per fix
* [ ] `uv run pytest` passes
* [ ] No new file is in `../music-transcriber/`
