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
CROP_PATTERN = re.compile(r"\d+:\d+:\d+:\d+")


class CandidateError(Exception):
    pass


def build_candidates(segments, columns=GRID_COLUMNS):
    return [
        {
            "number": index + 1,
            "start": segment["start"],
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


def extract_frames(video, workdir, crop, candidates):
    (workdir / "candidates").mkdir(exist_ok=True)
    for candidate in candidates:
        run_ffmpeg(
            ["-ss", candidate["frame_time"], "-i", video, "-vf", f"crop={crop}",
             "-frames:v", 1, workdir / candidate["file"]],
            FRAME_TIMEOUT,
        )


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


def format_map(candidates):
    return "\n".join(
        f"row {c['row']} column {c['column']}: #{c['number']} {format_timestamp(c['start'])}"
        for c in candidates
    )


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("video", type=Path)
    parser.add_argument("--workdir", type=Path, required=True)
    parser.add_argument("--crop", required=True, help="W:H:X:Y")
    args = parser.parse_args(argv)
    try:
        if not CROP_PATTERN.fullmatch(args.crop):
            raise CandidateError(f"invalid --crop {args.crop!r}, expected W:H:X:Y")
        candidates = build_candidates(load_segments(args.workdir))
        extract_frames(args.video, args.workdir, args.crop, candidates)
        build_sheet(args.workdir, len(candidates))
    except (CandidateError, MediaToolError, KeyError, TypeError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    (args.workdir / "candidates.json").write_text(json.dumps(candidates, indent=2))
    print(format_map(candidates))
    return 0


if __name__ == "__main__":
    sys.exit(main())
