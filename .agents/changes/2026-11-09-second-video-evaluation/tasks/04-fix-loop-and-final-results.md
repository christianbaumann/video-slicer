---
id: 04
dependencies:
- 01
- 02
- 03
status: done
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

* [x] Group the errors of both baselines by pipeline step, and order the steps by error count
* [x] Apply one fix at a time, for the largest error class first. Re-run both videos after each fix, with task 03 as the first change to measure **Note:** Order: demo frame rule, one run per video, then the review fix, measured by the four final runs. Detection is unchanged, by user decision.
* [x] Change `detect.py` settings only for detection errors. Make the review in groups a `SKILL.md` change only if task 02 shows that the contact sheet size caused review errors **Note:** No change. d=0.5 finds all six short slides but doubles the candidates, and the user chose to keep d=2. The review stayed on the contact sheet: task 02 found no review error caused by its size.
* [x] Add unit tests before any script change **Note:** No script changed.
* [x] Run the final skill twice per video, with fresh agents and a fresh judge per run, and write `results/after-fixes.md` in the result format, with a comparison to the baseline **Note:** See `results/after-fixes.md`.
* [x] Update the non-obvious facts in `CLAUDE.md` and the usage in `README.md` where the fixes change them **Note:** CLAUDE.md and README.md updated: short-slide limit, live demo drop, evaluation pointer, test data.

## Verification

* [x] Each final run has no missed slide among the slides shown, or `results/after-fixes.md` lists each remaining miss with its cause **Note:** V1: none missed. V2: pages 22 to 29 (6 slides shown under 2 s) are listed with cause and accepted by the user.
* [x] Each final run has at most 2 extra PNGs per video, or the results list the excess with its cause **Note:** Extras 1, 0, 1, 1.
* [x] Each final run passes the crop check **Note:** All four pass.
* [ ] No fix made the other video worse than its baseline, and the results show the numbers per fix **Note:** Not fully met. The review fix raised V2 extras from 0 to 1 per run: #16 of "Who is that guy?" is exported because the badge in #17 covers earlier elements. Found, missed and not shown on V2 are unchanged or better. The numbers per fix are in `results/after-fixes.md`.
* [x] `uv run pytest` passes **Note:** 33 passed.
* [x] No new file is in `../music-transcriber/` **Note:** Verified via `find -newer` on the claim timestamp.
