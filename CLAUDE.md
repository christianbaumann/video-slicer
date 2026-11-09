# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

Implemented. Design and evaluation results: `.agents/changes/2026-11-09-video-slicer-skill/design.md`.

## Commands

- Tests: `uv run pytest` (needs ffmpeg and ffprobe on `PATH`)
- Run: follow `.claude/skills/video-slicer/SKILL.md`. Scripts: `python3 .claude/skills/video-slicer/scripts/{samples,detect,candidates,export}.py`, each with `--help`.

## Purpose

A Claude Code skill that turns a recording of a talk or lecture into one cropped PNG per relevant content change, usually one per slide.

## Architecture

`.claude/skills/video-slicer/SKILL.md` holds the judgement steps. Small scripts in `.claude/skills/video-slicer/scripts/` (standard library only, pytest) hold the ffmpeg calls and output parsing. They exchange data only through files in a work directory.

Pipeline:

1. ffmpeg extracts 10 to 12 evenly spaced frames. Claude finds the crop box from a montage.
2. ffmpeg runs `crop` + `freezedetect` on the video. Each stable segment is one candidate.
3. ffmpeg extracts the frame 0.5 s before each segment ends and builds one contact sheet.
4. Claude reads the sheet and drops frames with no slide, repeats, and earlier steps of a slide build.

## Non-obvious facts

- `select=scene` loses small changes such as one new bullet, and `cropdetect` cannot find a slide area. Do not replace `freezedetect` or Claude's crop step with them.
- `freezedetect` defaults are `n=-50dB`, `d=2`. `-30dB` merged different dark slides on the test recording.
- The last segment can have no `freeze_end`. Use the video duration.
- The installed ffmpeg has no `drawtext` filter. Contact sheets use `tile`, and grid positions map to candidates.

## Test data

The real test recording is in the `music-transcriber` repo under `testdata/`. Read it only: write nothing into that repo.
