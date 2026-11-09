---
name: video-slicer
description: Turns a recording of a talk or lecture into one cropped PNG per slide or relevant content change. Use when the user wants slides, screenshots or key frames extracted from a presentation video.
---

# video-slicer

Needs `ffmpeg`, `ffprobe` and `python3`. `SCRIPTS` below is the `scripts/` folder next to this file.

Defaults unless the user says otherwise:

- Output: `<video>-slices/` next to the video, e.g. `talk.mp4` gives `talk-slices/`.
- Work directory: a new temp directory (`WORK=$(mktemp -d)`), removed after export.

Step 3 takes about 30 s for a 44 min video. Give it a timeout of at least 10 minutes.

## 1. Sample frames

```bash
python3 "$SCRIPTS/samples.py" "<video>" --workdir "$WORK"
```

Read `$WORK/montage.png` (12 frames, 4 columns, evenly spaced). Check:

- Where the slides are. Ignore speaker box, conference frame, logos.
- Whether all slides share one layout. If some samples show another layout (different slide area, slides in a different position), warn the user: one crop box is used for the whole video, and slides in other layouts are cut off or missed. Continue only with the main layout.

## 2. Find the crop box

Estimate `W:H:X:Y` in video pixels from the montage (each thumbnail is 480 px wide, so multiply by video width / 480). The box lies inside any slide border and is 16:9 for most slides.

Verify the corners at 4x. Crop a 100x60 area around each corner of the box (box corner shifted outward by 20 px, so the border is visible) and join the four into one image:

```bash
cd "$WORK"
ffmpeg -y -i samples/s01.png -vf "crop=100:60:X1:Y1,scale=400:240:flags=neighbor" tl.png   # repeat for tr, bl, br
ffmpeg -y -i tl.png -i tr.png -i bl.png -i br.png -filter_complex "[0][1]hstack[a];[2][3]hstack[b];[a][b]vstack" corners.png
```

Read `corners.png`. A cell shows 100x60 video pixels at 4x, so video position = crop origin + cell offset / 4. Move the box until no border, speaker or background remains inside and no slide content is cut. Repeat on a second sample if a corner is unclear.

## 3. Detect stable segments

```bash
python3 "$SCRIPTS/detect.py" "<video>" --workdir "$WORK" --crop W:H:X:Y
```

Writes `segments.json`. Each stable segment is one candidate. Defaults: `--noise-db -50 --min-seconds 2`. Do not loosen the noise value to `-30`: it merges different dark slides. A slide shown for under 2 s is not found.

## 4. Build the contact sheet

```bash
python3 "$SCRIPTS/candidates.py" "<video>" --workdir "$WORK" --crop W:H:X:Y
```

Prints one line per candidate: `row R column C: #N HH:MM:SS`. Rows and columns are zero-based in `$WORK/contact-sheet.png` (8 columns). No numbers are printed on the sheet, so count grid positions and use the printed map.

## 5. Review

Read `contact-sheet.png`. Decide per candidate. Drop:

- Frames with no slide: full-screen speaker, audience, Q&A or screen-share pages, black or transition frames.
- Live demo frames: IDE, terminal or browser content that fills the shared screen. Keep a slide that shows a screenshot or code inside slide layout (a slide title, footer or logo).
- Repeats: the same slide as an earlier kept candidate (a camera cut can split one slide into several segments). Keep the earliest.
- Earlier steps of a slide build: keep only the final state (the last of the build) and drop the steps before it.

Keep every other candidate, including slides that look similar but differ in content (for example several dark slides in a row).

The 320 px thumbnails are small. Re-read groups of 12 at 480 px when titles or progress markers are unreadable (`N` is the first candidate number, then 13, 25, ...):

```bash
ffmpeg -y -framerate 1 -start_number N -i "$WORK/candidates/%04d.png" -vf "scale=480:-2,tile=4x3" -frames:v 1 "$WORK/big-N.png"
```

If that still does not show whether two candidates differ (small text, one extra bullet), read the full-size frames `$WORK/candidates/NNNN.png` of both, or compare them: `ffmpeg -i A.png -i B.png -lavfi psnr -f null -` (about 40 dB or more means the same slide, below 20 dB means different content). Do not guess.

## 6. Export

```bash
python3 "$SCRIPTS/export.py" --workdir "$WORK" --output "<video>-slices" --keep 1,3,7
```

Writes `0001_HH-MM-SS.png`, ... in time order. The sequence number gives the order, the timestamp is the moment the slide appears. The files are at full crop resolution.

Then remove the work directory (`rm -rf "$WORK"`) and report to the user: output path, crop box, candidate count, kept count, dropped candidates with reasons, and any layout warning.
