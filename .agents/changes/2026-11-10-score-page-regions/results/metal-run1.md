# Metal score run 1

Video: Metal_arranged_by_Sean_O_Loughlin-[oumRCgkJAIU].mkv (1280x720, 5:55). Work dir and output: this folder (`slices/` = exported PNGs). Scripts from the worktree `score-page-regions-04`.

## Crop boxes
- Region 0 (left page): `536:720:101:0`
- Region 1 (right page): `536:720:643:0`
- Corners verified at 4x on sample s01 for both boxes: no border, black bar or logo inside. Page 1 on screen is x 99..638 and 642..1181; the box stays 2-3 px inside. Logo (Hal Leonard, bottom right) lies outside region 1.

## Counts
- Candidates: 82 (41 per region roughly; 3 s to 5:47)
- Kept: 35 (pages 2 to 36)
- Dropped: 47 (2 cover halves, 1 blank, 44 repeats)

## Kept PNGs
| file | time | region | candidate | printed page |
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
| 0023_00-03-38.png | 00:03:38 | 0 | #49 | 24 |
| 0024_00-03-44.png | 00:03:44 | 1 | #51 | 25 |
| 0025_00-04-08.png | 00:04:08 | 0 | #53 | 26 |
| 0026_00-04-18.png | 00:04:18 | 1 | #55 | 27 |
| 0027_00-04-25.png | 00:04:25 | 0 | #58 | 28 |
| 0028_00-04-32.png | 00:04:32 | 1 | #59 | 29 |
| 0029_00-04-41.png | 00:04:41 | 0 | #62 | 30 |
| 0030_00-04-47.png | 00:04:47 | 1 | #63 | 31 |
| 0031_00-04-56.png | 00:04:56 | 0 | #66 | 32 |
| 0032_00-05-05.png | 00:05:05 | 1 | #70 | 33 |
| 0033_00-05-17.png | 00:05:17 | 0 | #72 | 34 |
| 0034_00-05-26.png | 00:05:26 | 1 | #76 | 35 |
| 0035_00-05-38.png | 00:05:38 | 0 | #77 | 36 |

## Check against printed page numbers
- Pages 2 to 36 each exactly once, in order, none missing, no repeats (verified by reading the "Metal - N" footer of every exported PNG, and by PSNR of the footer-confirmed same-page candidates against the kept one: all 38.4 dB or more).
- Page 1 has no printed number: it is the cover (see below), not exported.
- Page 36 is the last page; video ends 5:55 with it.
- Misses: none. Repeats in output: none.
- Notes on the dropped repeats: each page turn gives one segment per region, and a page stays visible while the other turns, so 44 of 82 candidates repeat a page. 35 were flagged `same-as`. 9 were not flagged (PSNR 38.4 to 40.6 dB against the previous same-region frame, mostly just under 40): #46, #47, #64, #67, #69, #71, #73, #79, #82. Footer page number matched the kept frame in each case and difference images (#44/#46, #63/#64, #66/#67, #72/#73) were black (encoder noise). All 44 repeats have PSNR 38.4 dB or more against the kept frame of their page.
- No page-curl frame appeared as a candidate that was kept (kept frames of the 6 pages without any repeat, #3 #22 #36 #53 #58 #62, were viewed at full size: clean).

## Cover
- Cover (title page "METAL!" / instrumentation) is shown centred across both regions: #1 (region 0) shows its left half with black on the left, #2 (region 1) its right half with black on the right. Both dropped as "cover cut in half" and named here for the report. No PNG for the cover.

## Drops
| # | time | region | reason |
|---|---|---|---|
| #1 | 00:00:01 | 0 | cover, cut in half (left half) |
| #2 | 00:00:01 | 1 | cover, cut in half (right half) |
| #6 | 00:00:22 | 1 | repeat of page 3 (kept #4); PSNR checked vs #4 |
| #7 | 00:00:24 | 0 | repeat of page 4 (kept #5); PSNR checked vs #5 |
| #10 | 00:00:42 | 1 | repeat of page 5 (kept #8); PSNR checked vs #8 |
| #12 | 00:00:54 | 0 | repeat of page 6 (kept #9); PSNR checked vs #9 |
| #14 | 00:01:05 | 1 | repeat of page 7 (kept #11); PSNR checked vs #11 |
| #15 | 00:01:09 | 0 | repeat of page 8 (kept #13); PSNR checked vs #13 |
| #18 | 00:01:27 | 1 | repeat of page 9 (kept #16); PSNR checked vs #16 |
| #20 | 00:01:39 | 0 | repeat of page 10 (kept #17); PSNR checked vs #17 |
| #21 | 00:01:39 | 1 | repeat of page 11 (kept #19); PSNR checked vs #19 |
| #23 | 00:01:48 | 1 | repeat of page 11 (kept #19); PSNR checked vs #19 |
| #25 | 00:01:59 | 1 | repeat of page 13 (kept #24); PSNR checked vs #24 |
| #27 | 00:02:09 | 1 | repeat of page 13 (kept #24); PSNR checked vs #24 |
| #28 | 00:02:11 | 0 | repeat of page 14 (kept #26); PSNR checked vs #26 |
| #30 | 00:02:25 | 1 | repeat of page 15 (kept #29); PSNR checked vs #29 |
| #32 | 00:02:30 | 1 | repeat of page 15 (kept #29); PSNR checked vs #29 |
| #33 | 00:02:32 | 0 | repeat of page 16 (kept #31); PSNR checked vs #31 |
| #35 | 00:02:41 | 1 | repeat of page 17 (kept #34); PSNR checked vs #34 |
| #37 | 00:02:45 | 1 | repeat of page 17 (kept #34); PSNR checked vs #34 |
| #39 | 00:02:53 | 1 | repeat of page 19 (kept #38); PSNR checked vs #38 |
| #40 | 00:03:03 | 1 | repeat of page 19 (kept #38); PSNR checked vs #38 |
| #42 | 00:03:11 | 0 | repeat of page 20 (kept #41); PSNR checked vs #41 |
| #45 | 00:03:20 | 1 | repeat of page 21 (kept #43); PSNR checked vs #43 |
| #46 | 00:03:23 | 0 | repeat of page 22 (kept #44); PSNR checked vs #44 |
| #47 | 00:03:23 | 1 | repeat of page 21 (kept #43); PSNR checked vs #43 |
| #50 | 00:03:38 | 1 | repeat of page 23 (kept #48); PSNR checked vs #48 |
| #52 | 00:03:44 | 0 | repeat of page 24 (kept #49); PSNR checked vs #49 |
| #54 | 00:04:08 | 1 | repeat of page 25 (kept #51); PSNR checked vs #51 |
| #56 | 00:04:20 | 1 | repeat of page 27 (kept #55); PSNR checked vs #55 |
| #57 | 00:04:25 | 1 | repeat of page 27 (kept #55); PSNR checked vs #55 |
| #60 | 00:04:35 | 1 | repeat of page 29 (kept #59); PSNR checked vs #59 |
| #61 | 00:04:40 | 1 | repeat of page 29 (kept #59); PSNR checked vs #59 |
| #64 | 00:04:50 | 1 | repeat of page 31 (kept #63); PSNR checked vs #63 |
| #65 | 00:04:56 | 1 | repeat of page 31 (kept #63); PSNR checked vs #63 |
| #67 | 00:04:59 | 0 | repeat of page 32 (kept #66); PSNR checked vs #66 |
| #68 | 00:04:59 | 1 | repeat of page 31 (kept #63); PSNR checked vs #63 |
| #69 | 00:05:05 | 0 | repeat of page 32 (kept #66); PSNR checked vs #66 |
| #71 | 00:05:17 | 1 | repeat of page 33 (kept #70); PSNR checked vs #70 |
| #73 | 00:05:20 | 0 | repeat of page 34 (kept #72); PSNR checked vs #72 |
| #74 | 00:05:20 | 1 | repeat of page 33 (kept #70); PSNR checked vs #70 |
| #75 | 00:05:26 | 0 | repeat of page 34 (kept #72); PSNR checked vs #72 |
| #78 | 00:05:38 | 1 | repeat of page 35 (kept #76); PSNR checked vs #76 |
| #79 | 00:05:41 | 0 | repeat of page 36 (kept #77); PSNR checked vs #77 |
| #80 | 00:05:41 | 1 | repeat of page 35 (kept #76); PSNR checked vs #76 |
| #81 | 00:05:45 | 1 | no page: black right region with logo edge at video end |
| #82 | 00:05:47 | 0 | repeat of page 36 (kept #77); PSNR checked vs #77 |

## SKILL.md problems
1. Step 5 "Scores": "Candidates marked `same-as #M`, after a check ... Keep the candidate if a note, bar or page number differs." No rule for the 40 dB cut: here 9 repeats had 38.4-40.6 dB without the hint. Suggest: "Candidates without the hint can repeat too (about 38 to 40 dB on this video). Read the printed page number of every kept candidate; two candidates with the same page number are one page."
2. Printed page number is the cheapest reliable check but SKILL.md never says to use it. At 320 px thumbnails it is unreadable. Suggest, in Scores: "Read page numbers from the footer: crop the bottom-left corner of each candidate and tile the crops, e.g. `ffmpeg -framerate 1 -start_number N -i candidates/%04d.png -vf "crop=80:20:X:Y,scale=320:80,tile=4x11" -frames:v 1 foot.png` (adjust X:Y to the page-number text)." I did this; without it the dedupe would have been guesswork.
3. Cover: the Scores bullet says "cover shown cut in half or in the centre" but here the cover gives two candidates (#1 left half, #2 right half), one per region. Suggest: "A centred cover gives one candidate per region; drop both and name them."
4. Step 2 corner check: "box corner shifted outward by 20 px" is impossible at the video top/bottom edge (Y=0, bottom at 720). Suggest: "At the frame edge, crop from the edge instead."
5. Step 2 corner check commands show one crop per corner for one box only; for two boxes the instruction "repeat" is implicit. Also the 4-image hstack/vstack needs `[0][1]` labels as written (ok), but I had to infer to run it twice (once per box). Suggest: "Do this per box."
6. Step 6 says to `rm -rf "$WORK"` and defaults output to `<video>-slices/` next to the video. Task said output into work dir and not to write elsewhere. I wrote `slices/` inside the work dir and did not delete the work dir (needed for this evaluation). SKILL.md has no instruction for output inside the work dir; no real problem.
7. Step 5 intro lists drop reasons for slides (demo, build steps). For scores, "Earlier steps of a slide build" and "live demo" do not apply; the section "Scores" says "Also drop" so a reader may be unsure whether the general rules apply. Suggest: "For scores, only the Scores rules below apply." (Minor.)
8. Step 1 says the montage shows 12 frames in 4 columns; here 480 px per thumbnail gives page edges only roughly (+-3 px at 2.67x). The corner check in step 2 was needed and worked. No change.
9. Step 4 time column `HH:MM:SS` is the segment start, not the frame time (frame is 0.5 s before segment end). With a printed page number as the reference this does not matter, but the "Time" of a kept PNG is when the page appears. Fine as is.
