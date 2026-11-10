import argparse
import json
import math
import re
import sys
from pathlib import Path

from media import MediaToolError, run_ffmpeg

FRAME_OFFSET = 0.5
GRID_COLUMNS = 8
THUMBNAIL_WIDTH = 320
FRAME_TIMEOUT = 60
SHEET_TIMEOUT = 120
CROP_PATTERN = re.compile(r"(\d+):(\d+):\d+:\d+")
PSNR_TIMEOUT = 60
SAME_AS_MIN_DB = 40
PSNR_MAX_DB = 100
PSNR_AVERAGE = re.compile(r"average:(\S+)")


class CandidateError(Exception):
    pass


def build_candidates(segments, columns=GRID_COLUMNS):
    return [
        {
            "number": index + 1,
            "start": segment["start"],
            "region": segment.get("region", 0),
            "frame_time": round(max(segment["start"], segment["end"] - FRAME_OFFSET), 3),
            "file": f"candidates/{index + 1:04d}.png",
            "row": index // columns,
            "column": index % columns,
        }
        for index, segment in enumerate(segments)
    ]


def load_segments(workdir):
    path = workdir / "segments.json"
    try:
        segments = json.loads(path.read_text())
    except (OSError, ValueError) as error:
        raise CandidateError(f"cannot read {path}: {error}") from None
    if not isinstance(segments, list) or not segments:
        raise CandidateError(f"{path} has no segments")
    return segments


def validate_crops(crops, candidates):
    for crop in crops:
        if not CROP_PATTERN.fullmatch(crop):
            raise CandidateError(f"invalid --crop {crop!r}, expected W:H:X:Y")
    if len({CROP_PATTERN.fullmatch(crop).groups() for crop in crops}) > 1:
        raise CandidateError("all --crop values must have the same W:H")
    for candidate in candidates:
        region = candidate["region"]
        if not isinstance(region, int) or not 0 <= region < len(crops):
            raise CandidateError(
                f"segment region {region!r} has no --crop ({len(crops)} given)")


def extract_frames(video, workdir, crops, candidates):
    directory = workdir / "candidates"
    directory.mkdir(exist_ok=True)
    for stale in directory.glob("*.png"):
        stale.unlink()
    for candidate in candidates:
        run_ffmpeg(
            ["-ss", candidate["frame_time"], "-i", video, "-vf", f"format=rgb24,crop={crops[candidate['region']]}",
             "-frames:v", 1, workdir / candidate["file"]],
            FRAME_TIMEOUT,
        )


def measure_psnr(first, second):
    log = run_ffmpeg(["-i", first, "-i", second, "-lavfi", "psnr", "-f", "null", "-"],
                     PSNR_TIMEOUT)
    match = PSNR_AVERAGE.search(log)
    if not match:
        raise CandidateError("ffmpeg psnr printed no average")
    return min(float(match.group(1)), PSNR_MAX_DB)


def mark_same_as(candidates, measure):
    previous = {}
    for candidate in candidates:
        before = previous.get(candidate["region"])
        candidate["psnr"] = candidate["same_as"] = None
        if before:
            psnr = round(measure(before["file"], candidate["file"]), 1)
            candidate["psnr"] = psnr
            if psnr >= SAME_AS_MIN_DB:
                candidate["same_as"] = before["number"]
        previous[candidate["region"]] = candidate


def build_sheet(workdir, count, columns=GRID_COLUMNS):
    rows = math.ceil(count / columns)
    run_ffmpeg(
        ["-framerate", 1, "-i", workdir / "candidates" / "%04d.png",
         "-vf", f"scale={THUMBNAIL_WIDTH}:-2,tile={columns}x{rows}",
         "-frames:v", 1, workdir / "contact-sheet.png"],
        SHEET_TIMEOUT,
    )


def format_timestamp(seconds):
    whole = int(seconds)
    return f"{whole // 3600:02d}:{whole % 3600 // 60:02d}:{whole % 60:02d}"


def format_line(candidate, show_region):
    line = (f"row {candidate['row']} column {candidate['column']}: "
            f"#{candidate['number']} {format_timestamp(candidate['start'])}")
    if show_region:
        line += f" region {candidate['region']}"
    if candidate.get("same_as") is not None:
        line += f" same-as #{candidate['same_as']} ({candidate['psnr']:.0f} dB)"
    return line


def format_map(candidates, crop_count=1):
    show_region = crop_count > 1
    return "\n".join(format_line(c, show_region) for c in candidates)


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--crop", required=True, action="append",
                        help="W:H:X:Y, repeat once per page region, in region order")
    args = parser.parse_args(argv)
    try:
        candidates = build_candidates(load_segments(args.workdir))
        validate_crops(args.crop, candidates)
        extract_frames(args.video, args.workdir, args.crop, candidates)
        mark_same_as(candidates, lambda a, b: measure_psnr(args.workdir / a, args.workdir / b))
        build_sheet(args.workdir, len(candidates))
    except (CandidateError, MediaToolError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    (args.workdir / "candidates.json").write_text(json.dumps(candidates, indent=2))
    print(format_map(candidates, len(args.crop)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
