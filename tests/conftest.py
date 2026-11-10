import pytest

from media import run_ffmpeg

WIDTH, HEIGHT = 1280, 720
DURATION = 30
SLIDE_COLORS = ("0x203040", "0x202080", "0x204020")
SLIDE_CHANGES = (10, 20)
BULLET_TIME = 5
BULLET_BOX = "x=100:y=300:w=300:h=40"
BACKGROUND_COLOR = "0x303030"
SPEAKER_COLOR = "0xd2b48c"
SPEAKER_SIZE = "120x240"
SPEAKER_Y = 200
SPEAKER_X = "980+t*8"
NOISE_STRENGTH = 4
GENERATION_TIMEOUT = 120


def _slide_filter():
    parts = []
    for index, color in enumerate(SLIDE_COLORS):
        start = SLIDE_CHANGES[index - 1] if index else 0
        end = SLIDE_CHANGES[index] if index < len(SLIDE_CHANGES) else DURATION
        parts.append(f"drawbox=x=0:y=0:w=960:h={HEIGHT}:color={color}:t=fill"
                     f":enable='between(t,{start},{end})'")
    return parts


@pytest.fixture(scope="session")
def synthetic_talk(tmp_path_factory):
    path = tmp_path_factory.mktemp("talk") / "talk.mp4"
    slides = ",".join([
        *_slide_filter(),
        f"drawbox={BULLET_BOX}:color=white:t=fill:enable='gte(t,{BULLET_TIME})'",
    ])
    graph = (
        f"[0:v]{slides}[slides];"
        f"[slides][1:v]overlay=x='{SPEAKER_X}':y={SPEAKER_Y},"
        f"noise=alls={NOISE_STRENGTH}:allf=t+u"
    )
    run_ffmpeg(
        ["-f", "lavfi", "-i",
         f"color=c={BACKGROUND_COLOR}:s={WIDTH}x{HEIGHT}:r=10:d={DURATION}",
         "-f", "lavfi", "-i",
         f"color=c={SPEAKER_COLOR}:s={SPEAKER_SIZE}:r=10:d={DURATION}",
         "-filter_complex", graph, "-pix_fmt", "yuv420p", path],
        GENERATION_TIMEOUT,
    )
    return path


PAGE_SIZE = (600, 700)
PAGE_Y = 10
PAGE_X = {"left": 20, "right": 660}
SCORE_DURATION = 50
PAGE_COLORS = {
    "left": (("0x203040", 0), ("0x202080", 10), ("0x204020", 30), ("0x802020", 40)),
    "right": (("0x406040", 0), ("0x604060", 20), ("0x806020", 40)),
}


def _page_filter(side):
    width, height = PAGE_SIZE
    return [f"drawbox=x={PAGE_X[side]}:y={PAGE_Y}:w={width}:h={height}:color={color}:t=fill"
            f":enable='gte(t,{start})'" for color, start in PAGE_COLORS[side]]


@pytest.fixture(scope="session")
def synthetic_score(tmp_path_factory):
    path = tmp_path_factory.mktemp("score") / "score.mp4"
    pages = ",".join([*_page_filter("left"), *_page_filter("right"),
                      f"noise=alls={NOISE_STRENGTH}:allf=t+u"])
    run_ffmpeg(
        ["-f", "lavfi", "-i",
         f"color=c={BACKGROUND_COLOR}:s={WIDTH}x{HEIGHT}:r=10:d={SCORE_DURATION}",
         "-vf", pages, "-pix_fmt", "yuv420p", path],
        GENERATION_TIMEOUT,
    )
    return path
