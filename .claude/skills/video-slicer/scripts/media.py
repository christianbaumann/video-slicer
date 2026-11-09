import subprocess


class MediaToolError(Exception):
    pass


def _run(command, timeout):
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=timeout
        )
    except subprocess.TimeoutExpired:
        raise MediaToolError(f"{command[0]} timed out after {timeout} s") from None
    except OSError as error:
        raise MediaToolError(f"{command[0]} could not be started: {error}") from None
    if result.returncode != 0:
        detail = result.stderr.strip().splitlines()[-1:] or ["no error output"]
        raise MediaToolError(f"{command[0]} failed: {detail[0]}")
    return result


def run_ffmpeg(args, timeout):
    """Run ffmpeg and return its stderr, where filters such as freezedetect log."""
    return _run(["ffmpeg", "-hide_banner", "-nostdin", "-y", *map(str, args)], timeout).stderr


def probe_duration(video, timeout=30):
    command = [
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1", str(video),
    ]
    output = _run(command, timeout).stdout.strip()
    try:
        return float(output)
    except ValueError:
        raise MediaToolError(f"ffprobe returned no duration for {video}") from None
