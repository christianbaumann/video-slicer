---
id: 02
dependencies: []
status: done
owner: s-9c2e
branch: task/2026-11-09-second-video-evaluation-02
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

* [x] Export commit `b77c7c0` with `git archive` to a temp folder, and use its `SKILL.md` and `scripts/` for all runs
* [x] Run the exported skill twice, each time in a fresh agent that does not see the reference PDF. Output and work directory are in a temp folder, and the work directory stays after the run
* [x] Render the 35 pages of the PDF to images in a temp folder
* [x] For each run, start a fresh judge agent that sees only the exported PNGs, the kept work directory and the page images, and classifies every page and every PNG as defined in the design
* [x] Count pages 23, 26 and 29 ("DEMO TIME") as one slide. One PNG finds all three **Note:** Listed per page and counted as one slide in the Findings.
* [x] Classify host slides as `host slide`, and exported IDE, terminal and browser frames as `extra` **Note:** 11 host slides in run 1, 10 in run 2. No IDE, terminal or browser frame was exported.
* [x] Record for each run whether the 137-candidate contact sheet caused review errors, for example unreadable titles or wrong grid positions **Note:** See "Contact sheet size" in `results/baseline-video-2.md`.
* [x] Write `results/baseline-video-2.md` in the result format

## Verification

* [x] Each of the 35 reference pages has one status in each run **Note:** Verified via script and an independent verifier.
* [x] Each exported PNG maps to a reference page or has a class **Note:** Verified via script and an independent verifier (37 and 35 PNGs).
* [x] Each error has one error step **Note:** Verified via script. The 8 detection pages are 6 distinct slides, confirmed from frames at 2 fps.
* [x] Each run records crop, segment count, candidate count, exported count and a crop check **Note:** Verified against `segments.json`, `candidates.json` and the output folders.
* [x] The agents that ran the skill had no access to the PDF **Note:** Verified from the tool calls of the skill-run agents: no call names a PDF, `pdftoppm`, `.agents/` or the page images.
* [x] The results state whether the contact sheet size caused review errors **Note:** Yes. The sheet made reading harder and caused no review error in either run.
* [x] No new file is in `../music-transcriber/`, and `.claude/skills/video-slicer/` in this repo is unchanged by this task **Note:** Verified via `find -newer` on the claim timestamp and `git diff --stat main...HEAD` for the skill folder.
