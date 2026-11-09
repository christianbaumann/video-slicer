import argparse
import math
import sys
from pathlib import Path

from media import MediaToolError, probe_duration, run_ffmpeg

DEFAULT_COUNT = 12
MONTAGE_COLUMNS = 4
THUMBNAIL_WIDTH = 480
FFMPEG_TIMEOUT = 120


def sample_times(duration, count):
    return [duration * index / (count + 1) for index in range(1, count + 1)]


def extract_samples(video, samples_dir, times):
    samples_dir.mkdir(parents=True, exist_ok=True)
    for number, time in enumerate(times, start=1):
        target = samples_dir / f"s{number:02d}.png"
        run_ffmpeg(["-ss", f"{time:.3f}", "-i", video, "-frames:v", 1, target],
                   FFMPEG_TIMEOUT)


def build_montage(samples_dir, count, target):
    rows = math.ceil(count / MONTAGE_COLUMNS)
    run_ffmpeg(
        ["-framerate", 1, "-i", samples_dir / "s%02d.png",
         "-vf", f"scale={THUMBNAIL_WIDTH}:-1,tile={MONTAGE_COLUMNS}x{rows}",
         "-frames:v", 1, target],
        FFMPEG_TIMEOUT,
    )


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write sample frames and a montage.")
    parser.add_argument("video")
    parser.add_argument("--workdir", required=True, type=Path)
    parser.add_argument("--count", type=int, default=DEFAULT_COUNT)
    args = parser.parse_args(argv)
    if args.count < 1:
        parser.error("--count must be at least 1")
    try:
        times = sample_times(probe_duration(args.video), args.count)
        samples_dir = args.workdir / "samples"
        extract_samples(args.video, samples_dir, times)
        build_montage(samples_dir, args.count, args.workdir / "montage.png")
    except MediaToolError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
