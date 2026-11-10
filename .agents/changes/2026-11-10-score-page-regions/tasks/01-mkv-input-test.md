---
id: 01
dependencies: []
status: in-progress
owner: s-3c9e
branch: task/2026-11-10-score-page-regions-01
---

# Task 01: Test .mkv input

An automated test proves that the scripts work on an `.mkv` video. It fails if a later change breaks Matroska input.

## References

* `design.md#mkv-already-works`
* `design.md#mkv-test-only`
* Touches: `tests/test_mkv.py` (new)
* Reads only: `tests/conftest.py` (pattern for the synthetic video), `.claude/skills/video-slicer/scripts/media.py`, `.claude/skills/video-slicer/scripts/samples.py`, `.claude/skills/video-slicer/scripts/detect.py`

## Work

* [ ] Add `tests/test_mkv.py` with a module-local fixture that writes a short synthetic video in an `.mkv` container. Generate it with `run_ffmpeg` like `synthetic_talk`; do not change `tests/conftest.py`
* [ ] Test that `probe_duration` returns the duration of the `.mkv`
* [ ] Test that `samples.py` and `detect.py` run on the `.mkv` and find the expected segments
* [ ] Leave all production code and `SKILL.md` unchanged (task 04 updates the docs)

## Verification

* [ ] The new tests pass with the installed ffmpeg
* [ ] The new tests fail when the fixture path is replaced by a file that is not a video (spot check, then revert)
* [ ] No file outside `tests/test_mkv.py` changed
* [ ] `uv run pytest` passes
