# video-slicer

A Claude Code skill that turns a recording of a talk or lecture into one cropped PNG per relevant content change, usually one per slide.

ffmpeg finds the stable segments of the video. Claude finds the crop box from sample frames and reviews the candidates: it drops frames with no slide, repeats, and earlier steps of a slide build.

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

## Tests

```bash
uv run pytest
```
