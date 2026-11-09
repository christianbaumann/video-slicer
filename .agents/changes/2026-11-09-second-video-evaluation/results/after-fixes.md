# After fixes: videos 1 and 2

Skill under test: the state of branch `task/2026-11-09-second-video-evaluation-04` (commit 3f2d42a and the ones before it). Video 1 (Tesena Fest 2025, 37-page reference PDF) and video 2 (OpenRewrite talk, 35 reference pages). Two final runs per video, each with a fresh agent that did not see the PDF, and a fresh judge per run. Host slides on video 2 (sponsor and organizer slides not in the PDF) are listed under "PNG with no reference page" and are not counted in the totals. Baselines: `baseline-video-1.md`, `baseline-video-2.md`.

## Comparison per fix

Counts are found / missed / not shown / rule conflict / extra. `missed` is the sum of detection, review and frame choice errors.

| Stage | Run | Found | Missed | Not shown | Rule conflict | Extra |
|---|---|---|---|---|---|---|
| Baseline (b77c7c0) | V1 run 1 | 30 | 0 | 0 | 7 | 0 |
| Baseline | V1 run 2 | 30 | 0 | 0 | 7 | 1 |
| Baseline | V2 run 1 | 26 | 8 | 1 | 0 | 0 |
| Baseline | V2 run 2 | 25 | 9 | 1 | 0 | 0 |
| After demo frame rule (one run per video) | V1 | 29 | 1 | 0 | 7 | 1 |
| After demo frame rule | V2 | 26 | 8 | 1 | 0 | 0 |
| After review fix (final) | V1 run 1 | 30 | 0 | 0 | 7 | 1 |
| After review fix (final) | V1 run 2 | 30 | 0 | 0 | 7 | 0 |
| After review fix (final) | V2 run 1 | 26 | 8 | 1 | 0 | 1 |
| After review fix (final) | V2 run 2 | 26 | 8 | 1 | 0 | 1 |

All numbers match the totals lines of the judge files. Only the baseline runs differ in crop and segment counts (V2 baseline run 2: 135 segments, other runs 137).

## Fix order and effect

1. Demo frame rule (`SKILL.md` step 5): no measured gain. The baseline already dropped demo frames under "screen-share pages", and video 2 stayed at 0 extra. The video 1 run after this rule had one new miss, page 6 (candidate #12, a full GitHub screenshot slide without a title), dropped as an earlier step of the Elements build. That is review variance, not caused by the rule: both baseline runs kept #12.
2. Detection: no change, by the user's decision. See the measurement below. Video 1 had no detection errors and a lower `freezedetect` minimum duration would add candidates there.
3. Review fix (`SKILL.md` step 5: a build step is the same slide as a later candidate with content added, confirmed against the later frame; drop only for a reason the rules name). Page 6 and the Pause slide (page 20) are kept in all four final runs, so the video 1 miss and the video 2 baseline run 2 miss are gone. Side effect that made one number on video 2 worse: both final runs export candidate #16 (0006_00-01-50.png, the "Who is that guy?" slide before the badge appears). The badge in #17 covers elements of #16, so the wording "every element of the earlier frame still present" no longer counts #16 as a build step. Extra PNGs on video 2 rose from 0 to 1 in each run. Video 1 run 1 also has 1 extra, the green #tesenafest2025 title card (0001_00-00-00.png), which run 2 did not export; this is run-to-run variance and also appeared in the baseline run 2.

### Detection measurement (`freezedetect`, n=-50dB, crop as in the runs)

| d (s) | V1 segments | V1 new vs d=2 | V2 segments | V2 new in live demo (00:23:58 to 00:34:37) | V2 new elsewhere | V2 short slides found, of 6 |
|---|---|---|---|---|---|---|
| 2 (current) | 52 | 0 | 137 | 0 | 0 | 0 |
| 1 | 80 | 28 | 187 | 28 | 22 | 3 (Legacy JUnit 4, Modern JUnit 5, Legacy Selenium) |
| 0.5 | 113 | 61 | 282 | 90 | 55 | 6 |
| 0.25 | 262 | 210 | 560 | 193 | 230 | 6 (adds only fragments) |

At d=0.5 the 61 new video 1 segments are mostly camera and stage frames; a few are slide frames (Be aware!, Files & Code, Are you not done yet?, slido Q&A) that I did not compare with the baseline slides. The Modern Selenium segment is exactly 0.5 s, so d=0.5 is the largest value that finds all six, with no margin. Decision: d stays 2.

## Target check

| Target | V1 run 1 | V1 run 2 | V2 run 1 | V2 run 2 |
|---|---|---|---|---|
| Crop check passes | yes | yes | yes | yes |
| At most 2 extra PNGs | yes (1) | yes (0) | yes (1) | yes (1) |
| No missed slide among those shown | yes | yes | no (8 pages) | no (8 pages) |

The video 2 misses are the same in both runs and have one cause, detection. The speaker flips through these slides within 2086 to 2094 s (00:34:46 to 00:34:54), each shown 0.38 to 2 s, below the `freezedetect` minimum of 2 s, so no segment and no candidate exists:

| Reference page | Slide | Shown (s) |
|---|---|---|
| 22 | Legacy JUnit 4 | 2086.4 to 2088.1 |
| 23 | DEMO TIME | 2088.1 to 2088.8 |
| 24 | Modern JUnit 5 | 2088.8 to 2090.7 |
| 25 | Legacy Selenium Waits | 2090.7 to 2092.2 |
| 26 | DEMO TIME | 2092.25 to 2092.9 |
| 27 | Modern Selenium 4 | 2092.9 to 2093.4 |
| 28 | Legacy JavaScript | 2093.4 to 2094.3 |
| 29 | DEMO TIME | 2094.3 to 2094.7 |

Pages 23, 26 and 29 are the one DEMO TIME slide, so these are six distinct slides. Page 35 (Demos, GitHub link) is `not shown`: no candidate and no frame in the video shows it (baseline run 2 scanned the video). The user decided to accept these misses and keep d=2; the limit is documented in `CLAUDE.md` and `README.md`.

## V1 run 1 (crop 1312:738:104:172, 52 segments, 52 candidates, 31 exported)

Crop: 1312:738:104:172 | Segments: 52 | Candidates: 52 | Exported: 31
Crop check: pass - no green border or video background inside any PNG, no slide content cut (only the green title card 0001 is clipped at its right edge, which is the card's own design and it is an extra)

| Reference page | Status | PNG or candidate | Error step |
|---|---|---|---|
| 1 | found | 0002_00-01-20.png | |
| 2 | found | 0003_00-01-54.png | |
| 3 | found | 0004_00-02-51.png | |
| 4 | found | 0005_00-03-24.png | |
| 5 | found | 0006_00-05-49.png | |
| 6 | found | 0007_00-06-19.png | |
| 7 | found | 0008_00-06-36.png | |
| 8 | found | 0009_00-06-57.png | |
| 9 | found | 0010_00-07-24.png | |
| 10 | found | 0011_00-08-11.png | |
| 11 | found | 0012_00-08-53.png | |
| 12 | found | 0013_00-09-19.png | |
| 13 | found | 0014_00-10-08.png | |
| 14 | found | 0015_00-13-24.png | |
| 15 | found | 0016_00-14-21.png | |
| 16 | found | 0017_00-15-31.png | |
| 17 | rule conflict: build step | #26 | |
| 18 | found | 0018_00-16-17.png | |
| 19 | found | 0019_00-17-23.png | |
| 20 | found | 0020_00-18-07.png | |
| 21 | found | 0021_00-19-24.png | |
| 22 | found | 0022_00-22-02.png | |
| 23 | found | 0023_00-24-01.png | |
| 24 | rule conflict: repeat | repeat of page 22 | |
| 25 | rule conflict: repeat | repeat of page 23 | |
| 26 | found | 0024_00-25-24.png | |
| 27 | found | 0025_00-27-41.png | |
| 28 | found | 0026_00-29-13.png | |
| 29 | found | 0027_00-30-32.png | |
| 30 | found | 0028_00-31-29.png | |
| 31 | found | 0029_00-32-17.png | |
| 32 | found | 0030_00-34-15.png | |
| 33 | found | 0031_00-36-41.png | |
| 34 | rule conflict: Q&A | | |
| 35 | rule conflict: Q&A | | |
| 36 | rule conflict: Q&A | | |
| 37 | rule conflict: Q&A | | |

| PNG with no reference page | Class |
|---|---|
| 0001_00-00-00.png | extra |

Totals: 30 found, 0 missed, 0 not shown, 7 rule conflict, 1 extra

## Notes
- No errors among reference pages. Page 17 is candidate #26 (The Bad without koala), replaced by page 18 (found). Pages 24 and 25 repeat 22 and 23. Pages 34-37 are Q&A.
- 0001 is the green #tesenafest2025 title card (not in the reference), so it counts as extra per the known conflicts (error step: review).

## V1 run 2 (crop 1314:736:104:172, 52 segments, 52 candidates, 30 exported)

Crop: 1314:736:104:172 | Segments: 52 | Candidates: 52 | Exported: 30
Crop check: pass. All 30 PNGs are 1314x736; edges are slide background or slide content, no border inside, no content cut (0026 white right edge is the slide's own white panel, also in reference page 29).

| Reference page | Status | PNG or candidate | Error step |
|---|---|---|---|
| 1 | found | 0001_00-01-20.png | |
| 2 | found | 0002_00-01-54.png | |
| 3 | found | 0003_00-02-51.png | |
| 4 | found | 0004_00-03-24.png | |
| 5 | found | 0005_00-05-49.png | |
| 6 | found | 0006_00-06-19.png | |
| 7 | found | 0007_00-06-36.png | |
| 8 | found | 0008_00-06-57.png | |
| 9 | found | 0009_00-07-24.png | |
| 10 | found | 0010_00-08-11.png | |
| 11 | found | 0011_00-08-53.png | |
| 12 | found | 0012_00-09-19.png | |
| 13 | found | 0013_00-10-08.png | |
| 14 | found | 0014_00-13-24.png | |
| 15 | found | 0015_00-14-21.png | |
| 16 | found | 0016_00-15-31.png | |
| 17 | rule conflict: build step | #26 | |
| 18 | found | 0017_00-16-17.png | |
| 19 | found | 0018_00-17-23.png | |
| 20 | found | 0019_00-18-07.png | |
| 21 | found | 0020_00-19-24.png | |
| 22 | found | 0021_00-22-02.png | |
| 23 | found | 0022_00-24-01.png | |
| 24 | rule conflict: repeat | #35 (repeat of page 22) | |
| 25 | rule conflict: repeat | #36 (repeat of page 23) | |
| 26 | found | 0023_00-25-24.png | |
| 27 | found | 0024_00-27-41.png | |
| 28 | found | 0025_00-29-13.png | |
| 29 | found | 0026_00-30-32.png | |
| 30 | found | 0027_00-31-29.png | |
| 31 | found | 0028_00-32-17.png | |
| 32 | found | 0029_00-34-15.png | |
| 33 | found | 0030_00-36-41.png | |
| 34 | rule conflict: Q&A | #48 | |
| 35 | rule conflict: Q&A | #49 | |
| 36 | rule conflict: Q&A | #50 | |
| 37 | rule conflict: Q&A | #51 | |

| PNG with no reference page | Class |
|---|---|
| none | |

Totals: found 30, missed 0, not shown 0, rule conflict 7, extra 0

## Notes
- No errors. All 30 PNGs match one reference page each.
- Page 17: earlier build step of page 18 (same slide, koala not yet added), candidate #26; page 18 is found as 0017.
- Pages 24, 25: repeats of pages 22, 23 (candidates #33-#36 show the same two slides; 0021 and 0022 exported).
- Pages 34-37: Q&A slido frames, candidates #48-#51.
- Green #tesenafest2025 title card (#1, #52) was not exported.

## V2 run 1 (crop 1590:890:2:110, 137 segments, 137 candidates, 37 exported)

Crop: 1590:890:2:110 | Segments: 137 | Candidates: 137 | Exported: 37
Crop check: pass. All 37 PNGs are 1590x890, slides fill the frame with no border inside and no content cut (footer, title bars and edges complete). Host slides show at most a thin dark edge from the recording, no slide content lost.

| Reference page | Status | PNG or candidate | Error step |
|---|---|---|---|
| 1 | found | 0005_00-01-09.png | |
| 2 | found | 0007_00-01-53.png | |
| 3 | found | 0008_00-02-12.png | |
| 4 | found | 0009_00-02-53.png | |
| 5 | found | 0010_00-03-32.png | |
| 6 | found | 0011_00-03-55.png | |
| 7 | found | 0012_00-04-58.png | |
| 8 | found | 0013_00-06-18.png | |
| 9 | found | 0014_00-07-32.png | |
| 10 | found | 0015_00-08-48.png | |
| 11 | found | 0016_00-09-44.png | |
| 12 | found | 0017_00-10-22.png | |
| 13 | found | 0018_00-11-15.png | |
| 14 | found | 0019_00-11-41.png | |
| 15 | found | 0020_00-13-18.png | |
| 16 | found | 0021_00-14-09.png | |
| 17 | found | 0022_00-15-30.png | |
| 18 | found | 0023_00-16-11.png | |
| 19 | found | 0024_00-16-55.png | |
| 20 | found | 0025_00-18-07.png | |
| 21 | found | 0032_00-21-25.png | |
| 22 | detection error | none (not in any candidate) | detection |
| 23 | detection error | none (not in any candidate) | detection |
| 24 | detection error | none (not in any candidate) | detection |
| 25 | detection error | none (not in any candidate) | detection |
| 26 | detection error | none (not in any candidate) | detection |
| 27 | detection error | none (not in any candidate) | detection |
| 28 | detection error | none (not in any candidate) | detection |
| 29 | detection error | none (not in any candidate) | detection |
| 30 | found | 0033_00-34-54.png | |
| 31 | found | 0034_00-35-01.png | |
| 32 | found | 0035_00-36-15.png | |
| 33 | found | 0036_00-37-31.png | |
| 34 | found | 0037_00-38-15.png | |
| 35 | not shown | | |

| PNG with no reference page | Class |
|---|---|
| 0001_00-00-03.png | host slide |
| 0002_00-00-18.png | host slide |
| 0003_00-00-47.png | host slide |
| 0004_00-01-03.png | host slide |
| 0006_00-01-50.png | extra |
| 0026_00-18-38.png | host slide |
| 0027_00-19-25.png | host slide |
| 0028_00-19-33.png | host slide |
| 0029_00-19-51.png | host slide |
| 0030_00-20-28.png | host slide |
| 0031_00-20-39.png | host slide |

Totals: found 26, missed 8 (detection 8, review 0, frame choice 0), not shown 1, rule conflict 0, extra 1 (plus 10 host slides)

## Notes
- Pages 22-29 (Legacy JUnit, Demo, Modern JUnit, Legacy Selenium, Demo, Modern Selenium, Legacy JS, Demo): candidates 126-129 are IDE/terminal, 130 is Pick your live demo (2086 s), 131 is ES6 (2101 s). No candidate shows any of them, so detection error as measured (0.5-2 s each). Pages 23/26/29 are one DEMO TIME slide, each page counted.
- Page 35: candidate 137 (2812 s) is an IDE frame; no candidate shows Demos. not shown.
- Who is that guy: 0006 (motorbike photo build state) is extra; 0007 (badge) matches page 2 and is found.
- Host slides: 0001-0004 (Meet-up, Organisation & Speaker, Agenda, Dein Kompass) and 0026-0031 (Wissen ist wesentlich, Beitrag, Community Days, TACON x2, Elin Grosshans). No review errors.
- Candidates 126-129 (IDE/terminal) and repeat candidates (130 Pick demo, 133 Testing) were correctly dropped.

## V2 run 2 (crop 1592:890:0:110, 137 segments, 137 candidates, 37 exported)

Crop: 1592:890:0:110 | Segments: 137 | Candidates: 137 | Exported: 37
Crop check: pass. No border inside, no content cut on slides (title and footer intact), host slides full-bleed. (Caveat: judge accidentally overwrote exported 0012, 0024, 0037 with montage images; judged from identical candidates #25, #41, #136 instead.)

| Reference page | Status | PNG or candidate | Error step |
|---|---|---|---|
| 1 | found | 0005_00-01-09.png | |
| 2 | found | 0007_00-01-53.png | |
| 3 | found | 0008_00-02-12.png | |
| 4 | found | 0009_00-02-53.png | |
| 5 | found | 0010_00-03-32.png | |
| 6 | found | 0011_00-03-55.png | |
| 7 | found | 0012_00-04-58.png | |
| 8 | found | 0013_00-06-18.png | |
| 9 | found | 0014_00-07-32.png | |
| 10 | found | 0015_00-08-48.png | |
| 11 | found | 0016_00-09-44.png | |
| 12 | found | 0017_00-10-22.png | |
| 13 | found | 0018_00-11-15.png | |
| 14 | found | 0019_00-11-41.png | |
| 15 | found | 0020_00-13-18.png | |
| 16 | found | 0021_00-14-56.png | |
| 17 | found | 0022_00-15-30.png | |
| 18 | found | 0023_00-16-11.png | |
| 19 | found | 0024_00-16-55.png | |
| 20 | found | 0025_00-18-07.png | |
| 21 | found | 0032_00-21-25.png | |
| 22 | detection error | | detection |
| 23 | detection error | | detection |
| 24 | detection error | | detection |
| 25 | detection error | | detection |
| 26 | detection error | | detection |
| 27 | detection error | | detection |
| 28 | detection error | | detection |
| 29 | detection error | | detection |
| 30 | found | 0033_00-34-54.png | |
| 31 | found | 0034_00-35-01.png | |
| 32 | found | 0035_00-36-15.png | |
| 33 | found | 0036_00-37-31.png | |
| 34 | found | 0037_00-38-15.png | |
| 35 | not shown | | |

| PNG with no reference page | Class |
|---|---|
| 0001_00-00-03.png | host slide |
| 0002_00-00-18.png | host slide |
| 0003_00-00-47.png | host slide |
| 0004_00-01-03.png | host slide |
| 0006_00-01-50.png | extra |
| 0026_00-18-38.png | host slide |
| 0027_00-19-25.png | host slide |
| 0028_00-19-33.png | host slide |
| 0029_00-19-51.png | host slide |
| 0030_00-20-24.png | host slide |
| 0031_00-20-39.png | host slide |

Totals: found 26, missed 8, not shown 1, rule conflict 0, extra 1

## Notes
- Pages 22-29: no candidate shows them (cands 126-129 are IDE/terminal, 130 is Pick your live demo repeat, 131 is ES6). Detection errors, per measured 0.5-2 s display.
- Page 35: no candidate shows it; not shown.
- Who is that guy: 0006 (cand 16, motorbike photos, earlier build) is extra; 0007 (cand 17, AgileTD badge) matches page 2 and is found.
- TACON agenda 0030: all three items fully visible, final state, no fade-in.
- No review errors. Pages 7, 19, 34 verified via candidates #25, #41, #136.
- Note: 0011 through 0013 etc. map by segment start time; 0012/0024/0037 files in output are now clobbered (see crop caveat).

Note: after export the judge accidentally overwrote three exported PNGs in the temp folder (0012_00-04-58.png, 0024_00-16-55.png, 0037_00-38-15.png). It judged pages 7, 19 and 34 from the identical candidates #25, #41 and #136. The files were not restored.


## Open points

- Both videos are now tuning data. A change to the skill needs a third recording to check it.
- The design's page numbers for the alternating titles were off: the alternating pair is pages 22 to 25, not 19 to 22 (see `baseline-video-1.md`).
- Short slides (under 2 s) stay a known limit of `freezedetect` d=2.
