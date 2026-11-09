import json
import subprocess
import sys
from pathlib import Path

import pytest

import export
from export import ExportError, export_slices, slice_name

SCRIPT = Path(export.__file__)
PNG = b"\x89PNG\r\n\x1a\n"


@pytest.fixture
def workdir(tmp_path):
    work = tmp_path / "work"
    (work / "candidates").mkdir(parents=True)
    starts = {1: 754.2, 3: 5.0, 7: 3723.9}
    candidates = []
    for number, start in starts.items():
        name = f"candidates/{number:04d}.png"
        (work / name).write_bytes(PNG + str(number).encode())
        candidates.append({"number": number, "start": start, "file": name})
    (work / "candidates.json").write_text(json.dumps(candidates))
    return work


def test_name_from_first_start():
    assert slice_name(1, 754.2) == "0001_00-12-34.png"


def test_name_over_one_hour():
    assert slice_name(12, 3723) == "0012_01-02-03.png"


def test_name_floors_sub_second_starts():
    assert slice_name(1, 59.999) == "0001_00-00-59.png"
    assert slice_name(1, 3599.99) == "0001_00-59-59.png"


def test_keep_order_does_not_matter(workdir, tmp_path):
    out = tmp_path / "out"
    export_slices(workdir, out, [7, 1, 3])
    assert sorted(p.name for p in out.iterdir()) == [
        "0001_00-00-05.png",
        "0002_00-12-34.png",
        "0003_01-02-03.png",
    ]
    assert (out / "0001_00-00-05.png").read_bytes() == PNG + b"3"
    assert (out / "0002_00-12-34.png").read_bytes() == PNG + b"1"
    assert (out / "0003_01-02-03.png").read_bytes() == PNG + b"7"


def test_unknown_number_names_it_and_writes_nothing(workdir, tmp_path):
    out = tmp_path / "out"
    with pytest.raises(ExportError, match="99"):
        export_slices(workdir, out, [1, 99])
    assert not out.exists()


def test_cli_unknown_number_exits_nonzero_without_traceback(workdir, tmp_path):
    out = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--workdir", str(workdir), "--output", str(out), "--keep", "1,99"],
        capture_output=True, text=True,
    )
    assert result.returncode != 0
    assert "99" in result.stderr
    assert "Traceback" not in result.stderr
    assert not out.exists()


def test_cli_exports(workdir, tmp_path):
    out = tmp_path / "out"
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--workdir", str(workdir), "--output", str(out), "--keep", "1"],
        capture_output=True, text=True,
    )
    assert result.returncode == 0
    assert [p.name for p in out.iterdir()] == ["0001_00-12-34.png"]
