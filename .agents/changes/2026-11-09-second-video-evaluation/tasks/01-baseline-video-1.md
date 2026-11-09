---
id: 01
dependencies: []
status: done
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

* [x] Export commit `b77c7c0` with `git archive` to a temp folder, and use its `SKILL.md` and `scripts/` for all runs
* [x] Run the exported skill twice, each time in a fresh agent that does not see the reference PDF. Output and work directory are in a temp folder, and the work directory stays after the run
* [x] Render the 37 pages of the PDF to images in a temp folder
* [x] For each run, start a fresh judge agent that sees only the exported PNGs, the kept work directory and the page images, and classifies every page and every PNG as defined in the design
* [x] Apply the known conflicts: pages 34 to 37 are `rule conflict` (Q&A), page 17 is `rule conflict` (build step) if page 18 is found, and the judge decides for pages 19 to 22 and records why **Note:** Pages 19 to 22 are four different slides, all found. The alternating pair is at pages 22 to 25. See "Deviation from the design" in `results/baseline-video-1.md`.
* [x] Classify the green `#tesenafest2025` title card, if exported, as an extra PNG, because it is not in the reference **Note:** Exported in run 2 only, class `extra`.
* [x] Write `results/baseline-video-1.md` in the result format

## Verification

* [x] Each of the 37 reference pages has one status in each run **Note:** Verified via script and an independent verifier.
* [x] Each exported PNG maps to a reference page or has a class **Note:** Verified via script and an independent verifier (30 and 31 PNGs).
* [x] Each error has one error step **Note:** Neither run has an error row. The run 2 judge's frame choice error on page 29 was overruled, because the reference has the same split layout.
* [x] Each run records crop, segment count, candidate count, exported count and a crop check **Note:** Verified against `segments.json`, `candidates.json` and the output folders.
* [x] The agents that ran the skill had no access to the PDF **Note:** Verified from the tool calls of the skill-run agents: no call names a PDF, `pdftoppm`, `.agents/` or the page images.
* [x] No new file is in `../music-transcriber/`, and `.claude/skills/video-slicer/` in this repo is unchanged by this task **Note:** Verified via `find -newer` on the claim timestamp and `git diff --stat b77c7c0` for the skill folder.
