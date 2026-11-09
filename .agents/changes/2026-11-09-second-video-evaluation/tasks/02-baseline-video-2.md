---
id: 02
dependencies: []
---

# Task 02: Baseline video 2

The error list of the frozen skill on the OpenRewrite recording exists, with each error assigned to one pipeline step.

## References

* `design.md#test-data`
* `design.md#findings-in-video-2`
* `design.md#evaluation-loop`
* `design.md#result-format`
* `design.md#baseline`
* `design.md#output-location`
* `design.md#judge`
* `design.md#pages-not-shown`
* `design.md#fixes-only-with-evidence`
* Touches: `.agents/changes/2026-11-09-second-video-evaluation/results/baseline-video-2.md`
* Reads only: `../music-transcriber/testdata/` (video and PDF of video 2), commit `b77c7c0`

## Work

* [ ] Export commit `b77c7c0` with `git archive` to a temp folder, and use its `SKILL.md` and `scripts/` for all runs
* [ ] Run the exported skill twice, each time in a fresh agent that does not see the reference PDF. Output and work directory are in a temp folder, and the work directory stays after the run
* [ ] Render the 35 pages of the PDF to images in a temp folder
* [ ] For each run, start a fresh judge agent that sees only the exported PNGs, the kept work directory and the page images, and classifies every page and every PNG as defined in the design
* [ ] Count pages 23, 26 and 29 ("DEMO TIME") as one slide. One PNG finds all three
* [ ] Classify host slides as `host slide`, and exported IDE, terminal and browser frames as `extra`
* [ ] Record for each run whether the 137-candidate contact sheet caused review errors, for example unreadable titles or wrong grid positions
* [ ] Write `results/baseline-video-2.md` in the result format

## Verification

* [ ] Each of the 35 reference pages has one status in each run
* [ ] Each exported PNG maps to a reference page or has a class
* [ ] Each error has one error step
* [ ] Each run records crop, segment count, candidate count, exported count and a crop check
* [ ] The agents that ran the skill had no access to the PDF
* [ ] The results state whether the contact sheet size caused review errors
* [ ] No new file is in `../music-transcriber/`, and `.claude/skills/video-slicer/` in this repo is unchanged by this task
