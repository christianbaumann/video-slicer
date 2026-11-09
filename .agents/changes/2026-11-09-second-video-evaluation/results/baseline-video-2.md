# Baseline: video 2 (OpenRewrite)

Skill under test: commit b77c7c0. Video 2 (OpenRewrite talk, 35 reference pages). Two blind runs, each with a fresh agent that did not see the PDF, and a fresh judge per run. Host slides (sponsor and organizer slides not in the PDF) are listed under "PNG with no reference page" and are not counted in the totals.

## Run 1

Crop: 1590:894:0:108 | Segments: 137 | Candidates: 137 | Exported: 37
Crop check: pass. All 37 PNGs are 1590x894, no border or webcam strip inside, no slide content cut (title bars, summit footer and slide edges complete; host slides full-frame).

| Reference page | Status | PNG or candidate | Error step |
|---|---|---|---|
| 1 | found | 0005_00-01-09.png | |
| 2 | found | 0006_00-01-53.png | |
| 3 | found | 0007_00-02-12.png | |
| 4 | found | 0008_00-02-53.png | |
| 5 | found | 0009_00-03-32.png | |
| 6 | found | 0010_00-03-55.png | |
| 7 | found | 0011_00-04-58.png | |
| 8 | found | 0012_00-06-18.png | |
| 9 | found | 0013_00-07-32.png | |
| 10 | found | 0014_00-08-48.png | |
| 11 | found | 0015_00-09-44.png | |
| 12 | found | 0016_00-10-22.png | |
| 13 | found | 0017_00-11-15.png | |
| 14 | found | 0018_00-11-41.png | |
| 15 | found | 0019_00-13-18.png | |
| 16 | found | 0020_00-14-56.png | |
| 17 | found | 0021_00-15-30.png | |
| 18 | found | 0022_00-16-11.png | |
| 19 | found | 0023_00-16-55.png | |
| 20 | found | 0024_00-18-07.png | |
| 21 | found | 0032_00-21-25.png | |
| 22 | detection error | none (flipped past ~00:34:45-00:34:58) | detection |
| 23 | detection error | none (flipped past ~00:34:45-00:34:58) | detection |
| 24 | detection error | none (flipped past ~00:34:45-00:34:58) | detection |
| 25 | detection error | none (flipped past ~00:34:45-00:34:58) | detection |
| 26 | detection error | none (flipped past ~00:34:45-00:34:58) | detection |
| 27 | detection error | none (flipped past ~00:34:45-00:34:58) | detection |
| 28 | detection error | none (flipped past ~00:34:45-00:34:58) | detection |
| 29 | detection error | none (flipped past ~00:34:45-00:34:58) | detection |
| 30 | found | 0033_00-34-54.png | |
| 31 | found | 0034_00-35-01.png | |
| 32 | found | 0035_00-36-15.png | |
| 33 | found | 0036_00-37-31.png | |
| 34 | found | 0037_00-38-15.png | |
| 35 | not shown | none | |

| PNG with no reference page | Class |
|---|---|
| 0001_00-00-03.png | host slide |
| 0002_00-00-18.png | host slide |
| 0003_00-00-47.png | host slide |
| 0004_00-01-03.png | host slide |
| 0025_00-18-38.png | host slide |
| 0026_00-19-21.png | host slide |
| 0027_00-19-25.png | host slide |
| 0028_00-19-33.png | host slide |
| 0029_00-19-51.png | host slide |
| 0030_00-20-36.png | host slide |
| 0031_00-20-39.png | host slide |

Totals: found 26, missed 8 (detection 8), not shown 1, rule conflict 0, extra 0

## Run 2

Crop: 1584:890:4:110 | Segments: 135 | Candidates: 135 | Exported: 35
Crop check: pass. No border inside, no content cut; the dark strips at the top of the IDE vs OpenRewrite and Why not using AI? slides are part of the slide artwork (same in the reference).

| Reference page | Status | PNG or candidate | Error step |
|---|---|---|---|
| 1 | found | 0005_00-01-09.png | |
| 2 | found | 0006_00-01-53.png | |
| 3 | found | 0007_00-02-13.png | |
| 4 | found | 0008_00-02-53.png | |
| 5 | found | 0009_00-03-32.png | |
| 6 | found | 0010_00-03-55.png | |
| 7 | found | 0011_00-04-58.png | |
| 8 | found | 0012_00-06-18.png | |
| 9 | found | 0013_00-07-32.png | |
| 10 | found | 0014_00-08-48.png | |
| 11 | found | 0015_00-09-44.png | |
| 12 | found | 0016_00-10-22.png | |
| 13 | found | 0017_00-11-15.png | |
| 14 | found | 0018_00-11-41.png | |
| 15 | found | 0019_00-13-18.png | |
| 16 | found | 0020_00-14-56.png | |
| 17 | found | 0021_00-15-30.png | |
| 18 | found | 0022_00-16-11.png | |
| 19 | found | 0023_00-16-55.png | |
| 20 | review error | #41, #42 | review |
| 21 | found | 0030_00-21-25.png | |
| 22 | detection error | none (video 2086-2094 s) | detection |
| 23 | detection error | none (video 2086-2094 s) | detection |
| 24 | detection error | none (video 2086-2094 s) | detection |
| 25 | detection error | none (video 2086-2094 s) | detection |
| 26 | detection error | none (video 2086-2094 s) | detection |
| 27 | detection error | none (video 2086-2094 s) | detection |
| 28 | detection error | none (video 2086-2094 s) | detection |
| 29 | detection error | none (video 2086-2094 s) | detection |
| 30 | found | 0031_00-34-54.png | |
| 31 | found | 0032_00-35-01.png | |
| 32 | found | 0033_00-36-15.png | |
| 33 | found | 0034_00-37-31.png | |
| 34 | found | 0035_00-38-15.png | |
| 35 | not shown | | |

| PNG with no reference page | Class |
|---|---|
| 0001_00-00-03.png | host slide |
| 0002_00-00-18.png | host slide |
| 0003_00-00-47.png | host slide |
| 0004_00-01-03.png | host slide |
| 0024_00-18-38.png | host slide |
| 0025_00-19-25.png | host slide |
| 0026_00-19-33.png | host slide |
| 0027_00-19-51.png | host slide |
| 0028_00-20-28.png | host slide |
| 0029_00-20-39.png | host slide |

Totals: found 25, missed 9 (review 1, detection 8, frame choice 0), not shown 1, rule conflict 0, extra 0

## Findings

- Detection errors, pages 22 to 29: these eight pages are six distinct slides, because pages 23, 26 and 29 are the one DEMO TIME slide. The speaker flips through them within 2086 to 2094 s (00:34:46 to 00:34:54), then Modern ES6 follows from about 2094 s. Measured at 2 fps: Legacy JUnit 4 about 1.5 s, DEMO TIME about 1 s, Modern JUnit 5 about 1.5 s, Legacy Selenium about 2 s, DEMO TIME about 0.5 s, Modern Selenium about 0.5 s, Legacy JavaScript about 1 s. Each slide is shown about 0.5 to 2 s, all at or below the freezedetect minimum duration of 2 s, so no segment exists and no candidate shows them. Both runs have this error. The run 1 table rows give ~00:34:45-00:34:58 as written by its judge; the measured values above are the correct ones.
- Page 35 (Demos, GitHub link): status `not shown`. The run 2 judge searched the video (1085 to 2938 s) and found no frame of it. The run 1 judge did not scan the video, so for run 1 the status rests on the candidate set and on run 2's scan of the same video.
- Page 20 (Pause), run 2 only: the review agent dropped candidates #41 and #42 as break frames, although they show the Pause slide. Run 1 kept it (0024_00-18-07.png). This is run-to-run variance in the review step, not a rule conflict.
- Segment counts differ (137 and 135) because the two runs chose different crops (1590:894:0:108 and 1584:890:4:110).

## Contact sheet size

- Run 1: the sheet has 8 columns and 18 rows. Reading it was tedious, but grid positions from the printed map were not in doubt. All build-step judgements (Who is that guy, TACON agenda, Recipe Catalog sticker) needed the 480 px re-reads. No review errors.
- Run 2: rows were counted by eye and were off by one around rows 4 to 6 at first (for example #36/#37 and the Pause frames); corrected with the 480 px sheets. Several pairs (#36/#37, #13/#14, #53/#54, #27 to #29, #9/#43) were not decidable on the small sheet. The one review error (page 20, #41/#42) was a wrong decision on a clearly visible frame, not a misread sheet.
- Conclusion: the sheet size made reading harder and cost extra re-reads in both runs, but it caused no review error in either run.
