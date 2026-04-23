import os
import sys

import pytest

from renamer import numd


def test_file_list_returns_only_files(tmp_path):
    (tmp_path / "a.txt").write_text("a")
    (tmp_path / "b.mp4").write_text("b")
    (tmp_path / "subdir").mkdir()

    files = numd.fileList(str(tmp_path))

    assert set(files) == {"a.txt", "b.mp4"}


def test_nstring_zero_pads_to_width():
    assert numd.nString(7) == "0007"
    assert numd.nString(42, width=6) == "000042"


def test_next_number_skips_part_extension(tmp_path):
    result = numd.nextNumber(str(tmp_path), "video.part", start=0, width=4)
    assert result is None


def test_next_number_finds_first_available_slot(tmp_path):
    (tmp_path / "0000.mp4").write_text("x")
    (tmp_path / "0001.mp4").write_text("x")

    cn, out_name = numd.nextNumber(str(tmp_path), "input.mp4", start=0, width=4)

    assert cn == 2
    assert out_name == os.path.join(str(tmp_path), "0002.mp4")


def test_do_rename_renames_files_and_ignores_part(tmp_path, monkeypatch):
    (tmp_path / "one.mp4").write_text("1")
    (tmp_path / "two.mp4").write_text("2")
    (tmp_path / "three.part").write_text("3")

    monkeypatch.setattr(sys, "argv", ["numd", str(tmp_path), "100"])

    numd.doRename(width=4, start=0)

    names = {p.name for p in tmp_path.iterdir()}
    assert names == {"0100.mp4", "0101.mp4", "three.part"}


def test_do_rename_invalid_start_exits(tmp_path, monkeypatch):
    monkeypatch.setattr(sys, "argv", ["numd", str(tmp_path), "not-an-int"])

    with pytest.raises(SystemExit) as ex:
        numd.doRename(width=4, start=0)

    assert ex.value.code == 1


def test_do_rename_non_directory_exits(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["numd", "/definitely/not/a/real/dir"])

    with pytest.raises(SystemExit) as ex:
        numd.doRename(width=4, start=0)

    assert ex.value.code == 1
