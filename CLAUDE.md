# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Status

Implemented. Design: `.agents/changes/2026-11-09-video-slicer-skill/design.md`. Evaluation on two recordings against reference PDFs: `.agents/changes/2026-11-09-second-video-evaluation/results/` (`after-fixes.md` has the final numbers). Score mode (one crop box per page): `.agents/changes/2026-11-10-score-page-regions/design.md`, Metal video runs in `results/` there (`metal.md` is the final run).

## Commands

- Tests: `uv run pytest` (needs ffmpeg and ffprobe on `PATH`)
- Run: follow `.claude/skills/video-slicer/SKILL.md`. Scripts: `python3 .claude/skills/video-slicer/scripts/{samples,detect,candidates,export}.py`, each with `--help`.

## Purpose

A Claude Code skill that turns a recording of a talk or lecture into one cropped PNG per relevant content change, usually one per slide. Score videos (two sheet music pages side by side) give one PNG per page.

## Architecture

`.claude/skills/video-slicer/SKILL.md` holds the judgement steps. Small scripts in `.claude/skills/video-slicer/scripts/` (standard library only, pytest) hold the ffmpeg calls and output parsing. They exchange data only through files in a work directory.

Pipeline:

1. ffmpeg extracts 10 to 12 evenly spaced frames. Claude finds the crop box from a montage. For two pages side by side it sets one box per page (same size).
2. ffmpeg runs `crop` + `freezedetect` on the video, once per box (`--crop` repeats; segments carry a `region` index, sorted by start, then region). Each stable segment is one candidate.
3. ffmpeg extracts the frame 0.5 s before each segment ends, cropped by its region, and builds one contact sheet. `candidates.json` has `region`, `psnr` and `same_as` (previous candidate of the same region at 40 dB or more).
4. Claude reads the sheet and drops frames with no slide, live demo frames, repeats, and earlier steps of a slide build. For scores it also drops frames without a full page (cover cut in half), page-curl frames, and repeats. The printed page number decides whether two candidates are one page.

## Non-obvious facts

- `select=scene` loses small changes such as one new bullet, and `cropdetect` cannot find a slide area. Do not replace `freezedetect` or Claude's crop step with them.
- `freezedetect` defaults are `n=-50dB`, `d=2`. `-30dB` merged different dark slides on the test recording.
- `freezedetect` with `d=2` misses slides shown for under 2 s. On video 2, six slides shown 0.5 to 2 s each (2086 to 2094 s) get no segment. `d=0.5` finds them but raises candidates from 52 to 113 on video 1 and from 137 to 282 on video 2, mostly camera and demo frames. `d` stays 2 by decision.
- The last segment can have no `freeze_end`. Use the video duration.
- Score videos with half-turn page changes: one crop box makes every candidate a spread and repeats each page. Per-page regions fix this. About half of the region segments repeat a page, hence the `same-as` hint. `freezedetect` skips the page-curl animation, so some curl frames still appear as candidates.
- The 40 dB `same-as` cut misses repeats: on the Metal video 9 of 44 repeats got no hint (about 38 to 40 dB, encoder noise). The printed page number catches all of them. Thumbnails are too small to read it, so SKILL.md tiles footer crops.
- A centred score cover spans both page boxes and gives one candidate per region, each half a cover.
- Scripts do not check the file extension. `.mkv` works (test in `tests/test_mkv.py`).
- The installed ffmpeg has no `drawtext` filter. Contact sheets use `tile`, and grid positions map to candidates.

## Test data

The two real test recordings (Tesena Fest talk, OpenRewrite meet-up talk) and their reference PDFs are in the `music-transcriber` repo under `testdata/`. Read it only: write nothing into that repo.

`test-data/` in this repo holds the Metal score video (`.mkv`, AV1, 1280x720, 5:55, two pages side by side). It is untracked (`.gitignore`). No reference PDF; check against the page numbers printed on the score.
