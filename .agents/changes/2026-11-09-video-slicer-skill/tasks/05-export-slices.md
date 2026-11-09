---
id: 05
dependencies:
- 01
status: done
owner: s-a41c
branch: task/2026-11-09-video-slicer-skill-05
---

# Task 05: Export slices

`export.py` writes the candidates that Claude kept as ordered PNGs with a timestamp in the name.

## References

* `design.md#output`
* `design.md#file-structure-and-interfaces`
* Touches: `.claude/skills/video-slicer/scripts/export.py`, `tests/test_export.py`

## Work

* [x] Add a pure function that builds `0001_00-12-34.png` names from sequence number and segment `start`. **Note:** `slice_name(seq, start)` floors the start to whole seconds.
* [x] Add `export.py --workdir <dir> --output <dir> --keep 1,3,7` that reads `candidates.json` and copies the kept files to the output directory, ordered by `start`. **Note:** Duplicate `--keep` numbers collapse to one file. Bad `--keep` text, an unreadable `candidates.json` and a missing candidate PNG give a short error before anything is written.
* [x] Add unit tests for the names and tests with a hand-written `candidates.json` and small PNG files. This task needs no video. **Note:** 7 tests in `tests/test_export.py`.

## Verification

* [x] A candidate with `start` 754.2 as the first kept candidate gives `0001_00-12-34.png`. **Note:** Verified via `test_name_from_first_start` and `test_cli_exports`.
* [x] A talk position over one hour formats correctly, for example `01-02-03`. **Note:** Verified via `test_name_over_one_hour`.
* [x] `--keep 7,1,3` gives files numbered in time order. **Note:** Verified via `test_keep_order_does_not_matter`, which a separate verifier confirmed fails when the sort key is changed to `number`, and through the CLI with matching file contents.
* [x] A number that is not in `candidates.json` exits with a nonzero status, names the number and writes no files. **Note:** Verified via `test_cli_unknown_number_exits_nonzero_without_traceback` and `test_unknown_number_names_it_and_writes_nothing`; the CLI left no output directory.
* [x] `uv run pytest` passes. **Note:** Verified by a separate verifier on the rebased branch: 22 passed.
