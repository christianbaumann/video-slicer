---
id: 03
dependencies: []
status: done
owner: s-9c2e
branch: task/2026-11-09-second-video-evaluation-03
---

# Task 03: Demo frame rule

The review step drops live demo frames, and it keeps slides that contain screenshots or code.

## References

* `design.md#live-demo-frames`
* `design.md#findings-in-video-2`
* Touches: `.claude/skills/video-slicer/SKILL.md` (step 5)
* Reads only: `../music-transcriber/testdata/` (both videos)

## Work

* [x] Add live demo frames (IDE, terminal, browser) to the drop list in `SKILL.md` step 5
* [x] State the difference in the rule: a live demo fills the shared screen, and a slide shows a screenshot or code with slide layout, such as a slide title or footer

## Verification

* [x] A fresh agent that follows step 5 on the candidates of video 2 from minutes 25 to 35 drops all IDE, terminal and browser frames, and keeps the slides in this range, for example "Pick your live demo" and "Takeaways" **Note:** Verified via fresh agent on run 1 candidates: #60 to #129 (IDE, terminal, diff views, browser docs page) dropped, #59 "Pick your live demo" kept. "Takeaways" (#135, 00:37:31) is outside minutes 25 to 35 and was kept in a separate check by the verifier.
* [x] A fresh agent that follows step 5 on the candidates of video 1 keeps the slides with GitHub screenshots, for example "Elements - Navigation" and the full-slide screenshot at PDF page 6 **Note:** Verified via fresh agent on run 1 candidates: #12 (full GitHub screenshot in slide layout) and #13 "Elements - Navigation" kept. Run 1 judge maps page 6 for the mapping check in `results/baseline-video-1.md`.
* [x] Slides with code in video 2 stay kept, for example "Legacy JUnit 4" if it is shown in the recording **Note:** Code slides that are candidates stayed kept (#22, #32, #34, #35, #39, #131, #132). "Legacy JUnit 4" is shown for under 2 s and never became a candidate, so the rule cannot apply to it. See the detection errors in `results/baseline-video-2.md`.
* [x] Candidates for this check are in a temp folder, and no new file is in `../music-transcriber/` **Note:** Candidates are under the session temp folder. `find -newer` on the claim timestamp found no new file in `music-transcriber`.
