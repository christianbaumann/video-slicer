---
id: 03
dependencies: []
status: in-progress
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

* [ ] Add live demo frames (IDE, terminal, browser) to the drop list in `SKILL.md` step 5
* [ ] State the difference in the rule: a live demo fills the shared screen, and a slide shows a screenshot or code with slide layout, such as a slide title or footer

## Verification

* [ ] A fresh agent that follows step 5 on the candidates of video 2 from minutes 25 to 35 drops all IDE, terminal and browser frames, and keeps the slides in this range, for example "Pick your live demo" and "Takeaways"
* [ ] A fresh agent that follows step 5 on the candidates of video 1 keeps the slides with GitHub screenshots, for example "Elements - Navigation" and the full-slide screenshot at PDF page 6
* [ ] Slides with code in video 2 stay kept, for example "Legacy JUnit 4" if it is shown in the recording
* [ ] Candidates for this check are in a temp folder, and no new file is in `../music-transcriber/`
