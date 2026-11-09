import argparse
import json
import shutil
import sys
from pathlib import Path

SECONDS_PER_MINUTE = 60
SECONDS_PER_HOUR = 3600


class ExportError(Exception):
    pass


def slice_name(sequence, start):
    seconds = int(start)
    hours, rest = divmod(seconds, SECONDS_PER_HOUR)
    minutes, seconds = divmod(rest, SECONDS_PER_MINUTE)
    return f"{sequence:04d}_{hours:02d}-{minutes:02d}-{seconds:02d}.png"


def parse_keep(text):
    try:
        return [int(part) for part in text.split(",")]
    except ValueError:
        raise ExportError(f"--keep must be comma-separated numbers: {text!r}") from None


def select_kept(candidates, keep):
    by_number = {candidate["number"]: candidate for candidate in candidates}
    for number in keep:
        if number not in by_number:
            raise ExportError(f"candidate {number} is not in candidates.json")
    kept = [by_number[number] for number in dict.fromkeys(keep)]
    return sorted(kept, key=lambda candidate: candidate["start"])


def export_slices(workdir, output, keep):
    workdir, output = Path(workdir), Path(output)
    try:
        candidates = json.loads((workdir / "candidates.json").read_text())
    except (OSError, ValueError) as error:
        raise ExportError(f"cannot read candidates.json: {error}") from None
    kept = select_kept(candidates, keep)
    for candidate in kept:
        if not (workdir / candidate["file"]).is_file():
            raise ExportError(f"file of candidate {candidate['number']} is missing")
    output.mkdir(parents=True, exist_ok=True)
    written = []
    for sequence, candidate in enumerate(kept, start=1):
        target = output / slice_name(sequence, candidate["start"])
        shutil.copyfile(workdir / candidate["file"], target)
        written.append(target)
    return written


def main(argv=None):
    parser = argparse.ArgumentParser(description="Export kept candidates as named PNGs.")
    parser.add_argument("--workdir", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--keep", required=True, help="e.g. 1,3,7")
    args = parser.parse_args(argv)
    try:
        written = export_slices(args.workdir, args.output, parse_keep(args.keep))
    except ExportError as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    for path in written:
        print(path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
