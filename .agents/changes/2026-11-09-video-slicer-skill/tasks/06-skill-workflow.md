---
id: 06
dependencies:
- 02
- 03
- 04
- 05
status: done
owner: s-a41c
branch: task/2026-11-09-video-slicer-skill-06
---

# Task 06: Skill workflow

A user can run the skill on a recording and get one cropped PNG per relevant content change.

## References

* `design.md#pipeline`
* `design.md#crop-box`
* `design.md#candidate-review`
* `design.md#layout-changes`
* `design.md#evaluation`
* `design.md#open-points`
* Touches: `.claude/skills/video-slicer/SKILL.md`, `CLAUDE.md`, `README.md`

## Work

* [x] Add `SKILL.md` with the command sequence and the judgement steps: find the crop box inside any slide border, then magnify the corners 4x with an ffmpeg `crop,scale` command. **Note:** Followed on the real recording by the implementer and a separate verifier.
* [x] Describe the review rules in `SKILL.md`: drop frames with no slide, repeats and earlier steps of a slide build, and open full-size frames when the sheet does not show a difference. **Note:** `SKILL.md` adds examples of "no slide" (audience, Q&A, screen-share pages, black or transition frames), a 480 px sheet command, and PSNR thresholds for repeats (40 dB or more same, below 20 dB different). These go beyond the design's wording and do not contradict it.
* [x] Describe the warning for other slide layouts, and the default output `<video>-slices/` next to the video with its work directory removed after export. **Note:** The layout warning was not exercised, because the test recording has one layout.
* [x] Update `CLAUDE.md`: replace the design-only status with the real test and run commands
* [x] Add `README.md` with purpose, requirements (ffmpeg, ffprobe, uv for tests) and usage

## Verification

* [x] Running the skill on `/Users/christian.baumann/git_repos/_own/music-transcriber/testdata/` recording writes all output outside the `music-transcriber` repo, and `music-transcriber` has no new files. **Note:** Verified in two runs with work and output directories in the session scratchpad; no new entry came from either run.
* [x] With a crop near `1320:740:100:170`, detection gives about 52 candidates. **Note:** Verified in two runs: 52 segments, about 31 s.
* [ ] (manual testing required) The final set has about 34 PNGs, with no frames that have no slide and no repeated slides. **Note:** Not met as written. Two independent reviews kept 31 and 30, not about 34. Neither set has a frame with no slide or a repeated slide. They differ only in the green `#tesenafest2025` title card (candidate 1), which the design does not cover. A person needs to confirm the kept set and decide whether the expected count should change.
* [x] The five "Elements" slides are present as separate PNGs. **Note:** Verified in two runs: candidates 13 to 17.
* [x] File names give order and a timestamp that matches the slide position in the talk. **Note:** Verified by PSNR against video frames before and after three segment starts: 10 to 17 dB before, 41 to 42 dB after.
* [x] `uv run pytest` passes. **Note:** Verified by a separate verifier on the rebased branch: 33 passed.
