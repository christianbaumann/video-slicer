# Metal score run 2

Output: slices/ in this folder (35 PNGs, 538x716 each). Work files kept here.

## Crop boxes
- Region 0 (left page): `538:716:101:2`
- Region 1 (right page): `538:716:642:2`
- Frame 1280x720; pages at x 99-639 and 641-1181, black bar right of 1181, 1 px grey line at top and bottom edge (hence Y=2, H=716). Corners checked at 4x with `Y=0` crops from the edge.

## Counts
- Candidates: 83 (segments.json). Kept: 35 (pages 2 to 36). Dropped: 48.

## Kept PNGs
| file | time | region | cand | printed page |
|---|---|---|---|---|
| 0001_00-00-05.png | 00:00:05 | 0 | #3 | 2 |
| 0002_00-00-05.png | 00:00:05 | 1 | #4 | 3 |
| 0003_00-00-22.png | 00:00:22 | 0 | #5 | 4 |
| 0004_00-00-28.png | 00:00:28 | 1 | #8 | 5 |
| 0005_00-00-42.png | 00:00:42 | 0 | #9 | 6 |
| 0006_00-00-50.png | 00:00:50 | 1 | #11 | 7 |
| 0007_00-01-04.png | 00:01:04 | 0 | #13 | 8 |
| 0008_00-01-12.png | 00:01:12 | 1 | #16 | 9 |
| 0009_00-01-27.png | 00:01:27 | 0 | #17 | 10 |
| 0010_00-01-35.png | 00:01:35 | 1 | #19 | 11 |
| 0011_00-01-48.png | 00:01:48 | 0 | #22 | 12 |
| 0012_00-01-56.png | 00:01:56 | 1 | #24 | 13 |
| 0013_00-02-09.png | 00:02:09 | 0 | #26 | 14 |
| 0014_00-02-17.png | 00:02:17 | 1 | #29 | 15 |
| 0015_00-02-30.png | 00:02:30 | 0 | #31 | 16 |
| 0016_00-02-39.png | 00:02:39 | 1 | #34 | 17 |
| 0017_00-02-45.png | 00:02:45 | 0 | #36 | 18 |
| 0018_00-02-50.png | 00:02:50 | 1 | #38 | 19 |
| 0019_00-03-05.png | 00:03:05 | 0 | #41 | 20 |
| 0020_00-03-11.png | 00:03:11 | 1 | #43 | 21 |
| 0021_00-03-20.png | 00:03:20 | 0 | #44 | 22 |
| 0022_00-03-29.png | 00:03:29 | 1 | #48 | 23 |
| 0023_00-03-38.png | 00:03:38 | 0 | #50 | 24 |
| 0024_00-03-44.png | 00:03:44 | 1 | #52 | 25 |
| 0025_00-04-08.png | 00:04:08 | 0 | #54 | 26 |
| 0026_00-04-18.png | 00:04:18 | 1 | #56 | 27 |
| 0027_00-04-25.png | 00:04:25 | 0 | #59 | 28 |
| 0028_00-04-32.png | 00:04:32 | 1 | #60 | 29 |
| 0029_00-04-41.png | 00:04:41 | 0 | #63 | 30 |
| 0030_00-04-47.png | 00:04:47 | 1 | #64 | 31 |
| 0031_00-04-56.png | 00:04:56 | 0 | #67 | 32 |
| 0032_00-05-05.png | 00:05:05 | 1 | #71 | 33 |
| 0033_00-05-17.png | 00:05:17 | 0 | #73 | 34 |
| 0034_00-05-26.png | 00:05:26 | 1 | #77 | 35 |
| 0035_00-05-38.png | 00:05:38 | 0 | #78 | 36 |

## Check against printed page numbers (footer "Metal - N")
- Pages 2..36: each exactly once, in order, none missing, no repeats. 35 files = 35 pages. Page 1 never appears (cover is shown instead; not a miss).
- Spreads: left page even, right odd. During a turn the left page changes first (e.g. #5 p4 beside old p3 in #6), so every spread produces repeats; all removed via printed number.
- Hint behaviour: 36 repeats carried `same-as`; 9 repeats had no hint (#46, #47, #65, #68, #70, #72, #74, #80, #83: PSNR below 40 dB on the same page), all caught by the printed page number. No `same-as` candidate differed in page number.
- No page-curl frames seen among kept pages (every kept file shows a full sharp page, footer legible).

## Cover
Dropped and reported: #1 (left region) and #2 (right region), 00:00:01, centred "METAL!" cover (Hal Leonard, Grade 3, instrumentation) split across both regions. Cover is one page that is cut in half in each region.

## Drops
| # | time | region | reason |
|---|---|---|---|
| 1 | 00:00:01 | 0 | cover (centred, spans both regions; left/right halves) |
| 2 | 00:00:01 | 1 | cover (centred, spans both regions; left/right halves) |
| 6 | 00:00:22 | 1 | repeat of page 3 (same-as #4, printed page equals #4) |
| 7 | 00:00:24 | 0 | repeat of page 4 (same-as #5, printed page equals #5) |
| 10 | 00:00:42 | 1 | repeat of page 5 (same-as #8, printed page equals #8) |
| 12 | 00:00:54 | 0 | repeat of page 6 (same-as #9, printed page equals #9) |
| 14 | 00:01:05 | 1 | repeat of page 7 (same-as #11, printed page equals #11) |
| 15 | 00:01:09 | 0 | repeat of page 8 (same-as #13, printed page equals #13) |
| 18 | 00:01:27 | 1 | repeat of page 9 (same-as #16, printed page equals #16) |
| 20 | 00:01:39 | 0 | repeat of page 10 (same-as #17, printed page equals #17) |
| 21 | 00:01:39 | 1 | repeat of page 11 (same-as #19, printed page equals #19) |
| 23 | 00:01:48 | 1 | repeat of page 11 (same-as #21, printed page equals #19) |
| 25 | 00:01:59 | 1 | repeat of page 13 (same-as #24, printed page equals #24) |
| 27 | 00:02:09 | 1 | repeat of page 13 (same-as #25, printed page equals #24) |
| 28 | 00:02:11 | 0 | repeat of page 14 (same-as #26, printed page equals #26) |
| 30 | 00:02:25 | 1 | repeat of page 15 (same-as #29, printed page equals #29) |
| 32 | 00:02:30 | 1 | repeat of page 15 (same-as #30, printed page equals #29) |
| 33 | 00:02:32 | 0 | repeat of page 16 (same-as #31, printed page equals #31) |
| 35 | 00:02:41 | 1 | repeat of page 17 (same-as #34, printed page equals #34) |
| 37 | 00:02:45 | 1 | repeat of page 17 (same-as #35, printed page equals #34) |
| 39 | 00:02:53 | 1 | repeat of page 19 (same-as #38, printed page equals #38) |
| 40 | 00:03:03 | 1 | repeat of page 19 (same-as #39, printed page equals #38) |
| 42 | 00:03:11 | 0 | repeat of page 20 (same-as #41, printed page equals #41) |
| 45 | 00:03:20 | 1 | repeat of page 21 (same-as #43, printed page equals #43) |
| 46 | 00:03:23 | 0 | repeat of page 22 (no hint, same printed page as #44) |
| 47 | 00:03:23 | 1 | repeat of page 21 (no hint, same printed page as #43) |
| 49 | 00:03:36 | 1 | repeat of page 23 (same-as #48, printed page equals #48) |
| 51 | 00:03:40 | 1 | repeat of page 23 (same-as #49, printed page equals #48) |
| 53 | 00:03:44 | 0 | repeat of page 24 (same-as #50, printed page equals #50) |
| 55 | 00:04:08 | 1 | repeat of page 25 (same-as #52, printed page equals #52) |
| 57 | 00:04:20 | 1 | repeat of page 27 (same-as #56, printed page equals #56) |
| 58 | 00:04:25 | 1 | repeat of page 27 (same-as #57, printed page equals #56) |
| 61 | 00:04:35 | 1 | repeat of page 29 (same-as #60, printed page equals #60) |
| 62 | 00:04:40 | 1 | repeat of page 29 (same-as #61, printed page equals #60) |
| 65 | 00:04:50 | 1 | repeat of page 31 (no hint, same printed page as #64) |
| 66 | 00:04:56 | 1 | repeat of page 31 (same-as #65, printed page equals #64) |
| 68 | 00:04:59 | 0 | repeat of page 32 (no hint, same printed page as #67) |
| 69 | 00:04:59 | 1 | repeat of page 31 (same-as #66, printed page equals #64) |
| 70 | 00:05:05 | 0 | repeat of page 32 (no hint, same printed page as #67) |
| 72 | 00:05:17 | 1 | repeat of page 33 (no hint, same printed page as #71) |
| 74 | 00:05:20 | 0 | repeat of page 34 (no hint, same printed page as #73) |
| 75 | 00:05:20 | 1 | repeat of page 33 (same-as #72, printed page equals #71) |
| 76 | 00:05:26 | 0 | repeat of page 34 (same-as #74, printed page equals #73) |
| 79 | 00:05:38 | 1 | repeat of page 35 (same-as #77, printed page equals #77) |
| 80 | 00:05:41 | 0 | repeat of page 36 (no hint, same printed page as #78) |
| 81 | 00:05:41 | 1 | repeat of page 35 (same-as #79, printed page equals #77) |
| 82 | 00:05:45 | 1 | black frame |
| 83 | 00:05:47 | 0 | repeat of page 36 (no hint, same printed page as #78) |
No live-demo, no-slide or slide-build drops apply. Black frame #82 (5:45 region 1) is the end-of-video black.

## SKILL.md problems
1. Step 2 ("Verify the corners"): the `tl/tr/bl/br` commands only show `X1:Y1` placeholders; for two boxes and Y=0 it is unclear whether to still do the shift. Suggest: show the four crop origins formula (X-20,Y-20; X+W-80,Y-20; X-20,Y+H-40; X+W-80,Y+H-40) and say "clamp to 0 / frame size". I used clamped crops from the frame edge, as the Y=0 sentence allows.
2. Step 2: no guidance on a thin grey line at the page top/bottom edge or on gutters between two pages (dark divider at x=639-640). Suggest: "Keep the divider and any 1 px page-edge line outside each box".
3. Step 2/5: the footer-crop coordinates (`W:H:X:Y`) are "adjust to the page number text" with no way given to locate them. Suggest: "read one full-size candidate (candidates/0003.png) and measure the 'Metal - N' text; crop coordinates are relative to the box". I used `90:30:15:672` (worked for both regions).
4. Step 5 Scores: the recipe says "tile 44 at a time" with `tile=4x11`, but the candidate count (83) leaves the second sheet partly empty and black tiles (e.g. #82 black frame) look like missing candidates; say "a black tile is a black candidate frame, not a missing one" and that the final sheet may be padded black.
5. Step 5: "Two candidates with the same printed page number are one page: keep the first" conflicts with the generic "Keep every other candidate". Fine, but a pointer ("this overrides the keep-everything rule for scores") would help. Also unspecified: what to do when the printed page number is unreadable on a blank-looking footer; here it was always readable.
6. Step 5 Scores: the cover sentence says "centred cover spans both regions and gives one candidate per region", which matched #1/#2. The thumbnail of #1 looks like a half cover with black; the rule does not say black bars count as "cut in half" (they do). Suggest adding "black bars on one side of a candidate mean it is half of a cover".
7. Step 6 default output is `<video>-slices/` next to the video; here told to write elsewhere, no issue. The "remove the work directory" instruction was skipped (the task requires keeping it).
8. Step 5 first rule applies to slide talks; for scores the page-number check supersedes it, but the order (generic Drop list first, Scores after) makes the same-as hint look like it only matters when PSNR is unsure. Suggest: "For scores, go straight to the footer tiles; skip the PSNR checks unless the page number differs."

## Recipes
All ffmpeg and script recipes ran as written with no failure. Changes: none to the given commands. The footer tile recipe needed a custom crop (item 3). The first-step sample montage showed the layout was consistent (two pages everywhere), so no layout warning.
