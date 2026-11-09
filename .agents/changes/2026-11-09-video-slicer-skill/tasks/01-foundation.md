---
id: 01
dependencies: []
status: in-progress
owner: s-a41c
branch: task/2026-11-09-video-slicer-skill-01
---

# Task 01: Foundation

Scripts can call ffmpeg and ffprobe through one tested wrapper, and tests can run against a generated talk video.

## References

* `design.md#file-structure-and-interfaces`
* `design.md#packaging`
* Touches: `.claude/skills/video-slicer/scripts/media.py`, `tests/conftest.py`, `tests/test_media.py`, `pyproject.toml`, `.gitignore`

## Work

* [ ] Add `pyproject.toml` with pytest as a `uv` dev dependency and `.claude/skills/video-slicer/scripts` on the pytest `pythonpath`
* [ ] Add `.gitignore` for the virtual environment and Python and pytest caches
* [ ] Add `media.py` with `run_ffmpeg(args, timeout)`, `probe_duration(video)` and a `MediaToolError` type for tool failures and timeouts
* [ ] Add a session-scoped `synthetic_talk` fixture in `tests/conftest.py`: a 30 s video from `lavfi` with slide changes at 10 s and 20 s, a small bullet at 5 s, a speaker box moving right of x=960, and noise on all frames. Do not use `drawtext`, because the installed ffmpeg does not have it
* [ ] Add tests in `tests/test_media.py`

## Verification

* [ ] `uv run pytest` passes
* [ ] `probe_duration` returns about 30 s for `synthetic_talk`
* [ ] A nonexistent input raises `MediaToolError`, and its message has no stack trace
* [ ] A command that passes its timeout raises `MediaToolError`
* [ ] Production code imports only the standard library
