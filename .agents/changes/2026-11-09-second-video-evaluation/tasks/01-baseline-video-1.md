---
id: 01
dependencies: []
status: in-progress
owner: s-9c2e
branch: task/2026-11-09-second-video-evaluation-01
---

# Task 01: Baseline video 1

The error list of the frozen skill on the Tesena recording exists, with each error assigned to one pipeline step.

## References

* `design.md#test-data`
* `design.md#evaluation-loop`
* `design.md#result-format`
* `design.md#baseline`
* `design.md#output-location`
* `design.md#judge`
* `design.md#reference-conflicts`
* `design.md#pages-not-shown`
* Touches: `.agents/changes/2026-11-09-second-video-evaluation/results/baseline-video-1.md`
* Reads only: `../music-transcriber/testdata/` (video and PDF of video 1), commit `b77c7c0`

## Work

* [ ] Export commit `b77c7c0` with `git archive` to a temp folder, and use its `SKILL.md` and `scripts/` for all runs
* [ ] Run the exported skill twice, each time in a fresh agent that does not see the reference PDF. Output and work directory are in a temp folder, and the work directory stays after the run
* [ ] Render the 37 pages of the PDF to images in a temp folder
* [ ] For each run, start a fresh judge agent that sees only the exported PNGs, the kept work directory and the page images, and classifies every page and every PNG as defined in the design
* [ ] Apply the known conflicts: pages 34 to 37 are `rule conflict` (Q&A), page 17 is `rule conflict` (build step) if page 18 is found, and the judge decides for pages 19 to 22 and records why
* [ ] Classify the green `#tesenafest2025` title card, if exported, as an extra PNG, because it is not in the reference
* [ ] Write `results/baseline-video-1.md` in the result format

## Verification

* [ ] Each of the 37 reference pages has one status in each run
* [ ] Each exported PNG maps to a reference page or has a class
* [ ] Each error has one error step
* [ ] Each run records crop, segment count, candidate count, exported count and a crop check
* [ ] The agents that ran the skill had no access to the PDF
* [ ] No new file is in `../music-transcriber/`, and `.claude/skills/video-slicer/` in this repo is unchanged by this task
