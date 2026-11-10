---
id: 01
dependencies: []
status: done
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

* [x] Add `tests/test_mkv.py` with a module-local fixture that writes a short synthetic video in an `.mkv` container. Generate it with `run_ffmpeg` like `synthetic_talk`; do not change `tests/conftest.py` **Note:** Module-scoped fixture writes a 12 s 1280x720 `.mkv` via `run_ffmpeg`; colour change at 6 s; reuses conftest constants.
* [x] Test that `probe_duration` returns the duration of the `.mkv` **Note:** Asserted within 0.5 s of 12 s.
* [x] Test that `samples.py` and `detect.py` run on the `.mkv` and find the expected segments **Note:** samples: 4 PNGs + montage; detect: 2 segments starting ~0 s and ~6 s, last ending ~12 s.
* [x] Leave all production code and `SKILL.md` unchanged (task 04 updates the docs) **Note:** Verified via `git diff --stat main...HEAD` (only `tests/test_mkv.py`).

## Verification

* [x] The new tests pass with the installed ffmpeg **Note:** Verified via `uv run pytest tests/test_mkv.py` (3 passed).
* [x] The new tests fail when the fixture path is replaced by a file that is not a video (spot check, then revert) **Note:** Implementer and verifier each replaced the fixture output with a text file; all 3 tests failed; reverted.
* [x] No file outside `tests/test_mkv.py` changed **Note:** Verified via `git diff --stat main...HEAD`.
* [x] `uv run pytest` passes **Note:** 36 passed (verify subagent, rebased state).
