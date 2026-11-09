---
id: 01
dependencies: []
status: done
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

* [x] Add `pyproject.toml` with pytest as a `uv` dev dependency and `.claude/skills/video-slicer/scripts` on the pytest `pythonpath`
* [x] Add `.gitignore` for the virtual environment and Python and pytest caches. **Note:** Also ignores `.agents/worktrees/`.
* [x] Add `media.py` with `run_ffmpeg(args, timeout)`, `probe_duration(video)` and a `MediaToolError` type for tool failures and timeouts. **Note:** `probe_duration` has an optional `timeout` argument that defaults to `PROBE_TIMEOUT`.
* [x] Add a session-scoped `synthetic_talk` fixture in `tests/conftest.py`: a 30 s video from `lavfi` with slide changes at 10 s and 20 s, a small bullet at 5 s, a speaker box moving right of x=960, and noise on all frames. Do not use `drawtext`, because the installed ffmpeg does not have it. **Note:** 1280x720, 10 fps. Slide colours are `0x203040`, `0x202080` (blue, 10 s to 20 s) and `0x204020`. The speaker box uses `overlay`, because `t` in `drawbox` means thickness. With crop `960:720:0:0` and `n=-50dB:d=2`, `freezedetect` gives 0-5, 5-10, 10-20 and 20-end.
* [x] Add tests in `tests/test_media.py`. **Note:** 5 tests, including `test_speaker_box_moves_right_of_slide_area`.

## Verification

* [x] `uv run pytest` passes. **Note:** Verified by a separate verifier on e545c0a: 5 passed.
* [x] `probe_duration` returns about 30 s for `synthetic_talk`. **Note:** Verified via `test_probe_duration_of_synthetic_talk`; verifier measured 30.0.
* [x] A nonexistent input raises `MediaToolError`, and its message has no stack trace. **Note:** Verified via `test_probe_duration_of_missing_file_raises_without_traceback`.
* [x] A command that passes its timeout raises `MediaToolError`. **Note:** Verified via `test_run_ffmpeg_timeout_raises`.
* [x] Production code imports only the standard library. **Note:** Verified by grep over the scripts directory: `media.py` imports only `subprocess`.
