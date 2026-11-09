---
id: 06
dependencies:
- 02
- 03
- 04
- 05
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

* [ ] Add `SKILL.md` with the command sequence and the judgement steps: find the crop box inside any slide border, then magnify the corners 4x with an ffmpeg `crop,scale` command
* [ ] Describe the review rules in `SKILL.md`: drop frames with no slide, repeats and earlier steps of a slide build, and open full-size frames when the sheet does not show a difference
* [ ] Describe the warning for other slide layouts, and the default output `<video>-slices/` next to the video with its work directory removed after export
* [ ] Update `CLAUDE.md`: replace the design-only status with the real test and run commands
* [ ] Add `README.md` with purpose, requirements (ffmpeg, ffprobe, uv for tests) and usage

## Verification

* [ ] Running the skill on `/Users/christian.baumann/git_repos/_own/music-transcriber/testdata/` recording writes all output outside the `music-transcriber` repo, and `music-transcriber` has no new files
* [ ] With a crop near `1320:740:100:170`, detection gives about 52 candidates
* [ ] The final set has about 34 PNGs, with no frames that have no slide and no repeated slides
* [ ] The five "Elements" slides are present as separate PNGs
* [ ] File names give order and a timestamp that matches the slide position in the talk
* [ ] `uv run pytest` passes
