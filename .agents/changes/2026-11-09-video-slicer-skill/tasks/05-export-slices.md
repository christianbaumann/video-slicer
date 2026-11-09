---
id: 05
dependencies:
- 01
status: in-progress
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

* [ ] Add a pure function that builds `0001_00-12-34.png` names from sequence number and segment `start`
* [ ] Add `export.py --workdir <dir> --output <dir> --keep 1,3,7` that reads `candidates.json` and copies the kept files to the output directory, ordered by `start`
* [ ] Add unit tests for the names and tests with a hand-written `candidates.json` and small PNG files. This task needs no video

## Verification

* [ ] A candidate with `start` 754.2 as the first kept candidate gives `0001_00-12-34.png`
* [ ] A talk position over one hour formats correctly, for example `01-02-03`
* [ ] `--keep 7,1,3` gives files numbered in time order
* [ ] A number that is not in `candidates.json` exits with a nonzero status, names the number and writes no files
* [ ] `uv run pytest` passes
