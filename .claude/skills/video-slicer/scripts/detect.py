import argparse
import json
import re
import sys
from pathlib import Path

from media import MediaToolError, probe_duration, run_ffmpeg

DEFAULT_NOISE_DB = -50
DEFAULT_MIN_SECONDS = 2
DETECT_TIMEOUT = 3600
CROP_PATTERN = re.compile(r"\d+:\d+:\d+:\d+")
FREEZE_PATTERN = re.compile(r"lavfi\.freezedetect\.freeze_(start|end)=(\d+(?:\.\d+)?)")


def parse_segments(output, duration):
    segments = []
    for kind, value in FREEZE_PATTERN.findall(output):
        if kind == "start":
            segments.append({"start": float(value), "end": None})
        elif segments and segments[-1]["end"] is None:
            segments[-1]["end"] = float(value)
    for segment in segments:
        if segment["end"] is None:
            segment["end"] = duration
    return segments


def tag_and_sort(regions):
    tagged = [{**segment, "region": region}
              for region, segments in enumerate(regions) for segment in segments]
    return sorted(tagged, key=lambda segment: (segment["start"], segment["region"]))


def detect_segments(video, crop, noise_db, min_seconds):
    filters = f"crop={crop},freezedetect=n={noise_db}dB:d={min_seconds},metadata=print"
    output = run_ffmpeg(["-i", video, "-vf", filters, "-an", "-f", "null", "-"], DETECT_TIMEOUT)
    return parse_segments(output, probe_duration(video))


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("video")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--crop", required=True, action="append",
                        help="W:H:X:Y, repeat for several page regions")
    parser.add_argument("--noise-db", type=float, default=DEFAULT_NOISE_DB)
    parser.add_argument("--min-seconds", type=float, default=DEFAULT_MIN_SECONDS)
    args = parser.parse_args(argv)
    if not all(CROP_PATTERN.fullmatch(crop) for crop in args.crop):
        parser.error("--crop must look like W:H:X:Y with integers")
    try:
        segments = tag_and_sort(
            [detect_segments(args.video, crop, args.noise_db, args.min_seconds)
             for crop in args.crop])
    except MediaToolError as error:
        sys.exit(f"error: {error}")
    workdir = Path(args.workdir)
    workdir.mkdir(parents=True, exist_ok=True)
    (workdir / "segments.json").write_text(json.dumps(segments, indent=2))
    print(f"{len(segments)} segments written to {workdir / 'segments.json'}")


if __name__ == "__main__":
    main()
