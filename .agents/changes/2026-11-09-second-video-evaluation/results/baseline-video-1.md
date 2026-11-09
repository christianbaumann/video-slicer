# Baseline results: video 1 (Tesena)

Skill under test: commit b77c7c0. Video 1 (Tesena Fest 2025, 37-page reference PDF). Two blind runs with fresh agents that had no access to the PDF, and a fresh judge per run.

## Deviation from the design

The design and task say pages 19 to 22 are two alternating titles. They are four different slides (PSNR about 13 dB between pages), all found in both runs. The alternating pair is pages 22 to 25: p22 and p24 are near-identical (PSNR 41.3 dB), p23 and p25 too (42.2 dB). Both judges classed p24 and p25 as `rule conflict: repeat`.

## Run 1

Crop: 1316:738:102:171 | Segments: 52 | Candidates: 52 | Exported: 30
Crop check: pass. No border (edge pixels are slide grey, no green frame), no content cut; text and toolbar icons are complete and match the reference layout.

| Reference page | Status | PNG or candidate | Error step |
|---|---|---|---|
| 1 | found | 0001_00-01-20.png (#2) | |
| 2 | found | 0002_00-01-54.png (#3) | |
| 3 | found | 0003_00-02-51.png (#4) | |
| 4 | found | 0004_00-03-24.png (#6) | |
| 5 | found | 0005_00-05-49.png (#11) | |
| 6 | found | 0006_00-06-19.png (#12) | |
| 7 | found | 0007_00-06-36.png (#13) | |
| 8 | found | 0008_00-06-57.png (#14) | |
| 9 | found | 0009_00-07-24.png (#15) | |
| 10 | found | 0010_00-08-11.png (#16) | |
| 11 | found | 0011_00-08-53.png (#17) | |
| 12 | found | 0012_00-09-19.png (#18) | |
| 13 | found | 0013_00-10-08.png (#21) | |
| 14 | found | 0014_00-13-24.png (#22) | |
| 15 | found | 0015_00-14-21.png (#23) | |
| 16 | found | 0016_00-15-31.png (#24) | |
| 17 | rule conflict: build step | #26 (build step of p18) | |
| 18 | found | 0017_00-16-17.png (#27) | |
| 19 | found | 0018_00-17-23.png (#28) | |
| 20 | found | 0019_00-18-07.png (#29) | |
| 21 | found | 0020_00-19-24.png (#30) | |
| 22 | found | 0021_00-22-02.png (#32) | |
| 23 | found | 0022_00-24-01.png (#36) | |
| 24 | rule conflict: repeat | #33-#35 (identical to p22) | |
| 25 | rule conflict: repeat | #36 (identical to p23) | |
| 26 | found | 0023_00-25-24.png (#39) | |
| 27 | found | 0024_00-27-41.png (#40) | |
| 28 | found | 0025_00-29-13.png (#41) | |
| 29 | found | 0026_00-30-32.png (#42) | |
| 30 | found | 0027_00-31-29.png (#43) | |
| 31 | found | 0028_00-32-17.png (#44) | |
| 32 | found | 0029_00-34-15.png (#45) | |
| 33 | found | 0030_00-36-41.png (#46) | |
| 34 | rule conflict: Q&A | #48 | |
| 35 | rule conflict: Q&A | #49 | |
| 36 | rule conflict: Q&A | #50 | |
| 37 | rule conflict: Q&A | #51 | |

| PNG with no reference page | Class |
|---|---|
| none | |

Totals: found 30, missed 0, not shown 0, rule conflict 7, extra 0

### Notes

- Page numbers follow the 37 reference images. Pages 19-22 (Documentation/Copilot, Comments & Commits, Files & Code, Update External Files) are four different slides, no alternation: all found (PNGs 0018-0021).
- The alternating pair is actually pages 22-25 (Update External Files / Number of Changes). p24 equals p22 and p25 equals p23 (RMSE under 1%, same text and highlight boxes), so they are repeats: rule conflict: repeat.
- p17 (Documentation - The Bad without koala) is an earlier build step of p18 (found): rule conflict: build step.
- p34-37 are slido Q&A pages (candidates 48-51): rule conflict: Q&A. The green #tesenafest2025 title card (#1, #52) was not exported.
- Candidate-to-PNG mapping verified by pixel comparison. PNG file times are segment starts, not frame times.

## Run 2

Crop: 1320:740:100:170 | Segments: 52 | Candidates: 52 | Exported: 31
Crop check: pass. Edge rows/columns are slide grey, no green reference border inside; no content cut (title, progress bar, @AgentAJ all complete in every PNG).

| Reference page | Status | PNG or candidate | Error step |
|---|---|---|---|
| 1 | found | 0002_00-01-20.png |  |
| 2 | found | 0003_00-01-54.png |  |
| 3 | found | 0004_00-02-51.png |  |
| 4 | found | 0005_00-03-24.png |  |
| 5 | found | 0006_00-05-49.png |  |
| 6 | found | 0007_00-06-19.png |  |
| 7 | found | 0008_00-06-36.png |  |
| 8 | found | 0009_00-06-57.png |  |
| 9 | found | 0010_00-07-24.png |  |
| 10 | found | 0011_00-08-11.png |  |
| 11 | found | 0012_00-08-53.png |  |
| 12 | found | 0013_00-09-19.png |  |
| 13 | found | 0014_00-10-08.png |  |
| 14 | found | 0015_00-13-24.png |  |
| 15 | found | 0016_00-14-21.png |  |
| 16 | found | 0017_00-15-31.png |  |
| 17 | rule conflict: build step | #26 |  |
| 18 | found | 0018_00-16-17.png |  |
| 19 | found | 0019_00-17-23.png |  |
| 20 | found | 0020_00-18-07.png |  |
| 21 | found | 0021_00-19-24.png |  |
| 22 | found | 0022_00-22-02.png |  |
| 23 | found | 0023_00-24-01.png |  |
| 24 | rule conflict: repeat | #33 (same as p22) |  |
| 25 | rule conflict: repeat | #36 (same as p23) |  |
| 26 | found | 0024_00-25-24.png |  |
| 27 | found | 0025_00-27-41.png |  |
| 28 | found | 0026_00-29-13.png |  |
| 29 | found | 0027_00-30-32.png (#42) | |
| 30 | found | 0028_00-31-29.png |  |
| 31 | found | 0029_00-32-17.png |  |
| 32 | found | 0030_00-34-15.png |  |
| 33 | found | 0031_00-36-41.png |  |
| 34 | rule conflict: Q&A |  |  |
| 35 | rule conflict: Q&A |  |  |
| 36 | rule conflict: Q&A |  |  |
| 37 | rule conflict: Q&A |  |  |

| PNG with no reference page | Class |
|---|---|
| 0001_00-00-00.png | extra (green #tesenafest2025 title card, not in reference) |

Totals: found 30, missed 0, not shown 0, rule conflict 7 (p17 build step, p24/p25 repeat, p34-37 Q&A), extra 1

Judge classification of p29 was overruled by the main agent (see Notes).

### Notes

- Page 19-22 as numbered in the reference: p19 Documentation (Copilot), p20 Comments & Commits, p21 Files & Code, p22 Update External Files. All have their own PNG (found); they are not alternating titles. The alternating pair is p22/p23 vs p24/p25 (Update External Files / Number of Changes shown twice).
- p24 (Update External Files, second time): identical content to p22 (PNG 0022, candidates #32-#35), so repeat -> rule conflict: repeat. p25 (Number of Changes, second time): identical to p23 (PNG 0023, #36), repeat -> rule conflict: repeat.
- p17 (Documentation - The Bad without koala) = #26; p18 found (0018, #27) so build step conflict.
- p29 (Run the software): PNG 0027_00-30-32.png (#42) is found. The judge first classed it as frame choice error (wipe transition). Overruled: reference p29 has the same half-grey, half-white split layout, so it is the slide design.
- 0001 is the green #tesenafest2025 title card: extra by the given rule. It is full-bleed, so the 1320x740 crop cuts off the last "5" of the title (run 2 report).
- Run 1 did not export the title card (dropped #1 and #52 as bumper cards), so it has no extra PNG.
