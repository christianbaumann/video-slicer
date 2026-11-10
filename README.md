# video-slicer

A Claude Code skill that turns a recording of a talk or lecture into one cropped PNG per relevant content change, usually one per slide.

ffmpeg finds the stable segments of the video. Claude finds the crop box from sample frames and reviews the candidates: it drops frames with no slide, live demo frames, repeats, and earlier steps of a slide build.

## Requirements

- Claude Code
- `ffmpeg` and `ffprobe` on `PATH` (with the `freezedetect` filter)
- `python3` 3.10 or newer (scripts use the standard library only)
- `uv`, for the tests only

## Usage

In this repository, ask Claude Code to slice a video, for example "slice /path/to/talk.mp4 into slides". The skill in `.claude/skills/video-slicer/SKILL.md` runs.

To use it elsewhere, copy `.claude/skills/video-slicer/` into `~/.claude/skills/` or a project's `.claude/skills/`.

Output: `<video>-slices/0001_00-12-34.png`, ... next to the video. The number gives the order, the timestamp is when the slide appears. Frames have the full resolution of the crop box. The work directory is deleted after export.

One crop box is used for the whole video. If the samples show other slide layouts, Claude warns you.

`.mp4` and `.mkv` videos work. For a score video with two pages side by side, Claude sets one crop box per page and the output has one PNG per page in reading order. It drops the cover if it is not a full page, page-curl frames, and pages that repeat the previous page of the same side.

Limit: slides shown for under 2 s (for example flipped through quickly) get no candidate. Lower `--min-seconds` in `detect.py` finds them but multiplies the candidates.

## Evaluation

Two recordings were checked against the PDFs of their talks, two blind runs each. Video 1: all 30 pages found in both runs (the other 7 of 37 are repeats, a build step and Q&A, dropped by rule). Video 2: 26 of 34 pages found in both runs; the 8 missed pages are six slides shown under 2 s each. Details: `.agents/changes/2026-11-09-second-video-evaluation/results/after-fixes.md`.

## Tests

```bash
uv run pytest
```
