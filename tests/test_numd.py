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


def test_next_number_applies_prefix(tmp_path):
    cn, out_name = numd.nextNumber(
        str(tmp_path), "input.mp4", start=7, width=4, prefix="clip_"
    )

    assert cn == 7
    assert out_name == os.path.join(str(tmp_path), "clip_0007.mp4")


def test_do_rename_renames_files_and_ignores_part(tmp_path):
    (tmp_path / "one.mp4").write_text("1")
    (tmp_path / "two.mp4").write_text("2")
    (tmp_path / "three.part").write_text("3")

    numd.doRename(path=str(tmp_path), width=4, start=100)

    names = {p.name for p in tmp_path.iterdir()}
    assert names == {"0100.mp4", "0101.mp4", "three.part"}


def test_do_rename_dry_run_makes_no_changes(tmp_path):
    (tmp_path / "one.mp4").write_text("1")
    (tmp_path / "two.mp4").write_text("2")

    numd.doRename(path=str(tmp_path), width=4, start=10, dry_run=True)

    names = {p.name for p in tmp_path.iterdir()}
    assert names == {"one.mp4", "two.mp4"}


def test_do_rename_auto_expands_width_from_file_count(tmp_path):
    for i in range(12):
        (tmp_path / f"clip{i}.mp4").write_text("x")

    numd.doRename(path=str(tmp_path), width=1, start=0)

    names = sorted(p.name for p in tmp_path.iterdir())
    assert names[0] == "00.mp4"
    assert names[-1] == "11.mp4"


def test_do_rename_non_directory_exits():
    with pytest.raises(SystemExit) as ex:
        numd.doRename(path="/definitely/not/a/real/dir")

    assert ex.value.code == 1


def test_do_rename_randomise_calls_shuffle(tmp_path, monkeypatch):
    (tmp_path / "a.mp4").write_text("a")
    (tmp_path / "b.mp4").write_text("b")

    called = {"value": False}

    def fake_shuffle(items):
        called["value"] = True
        items.reverse()

    monkeypatch.setattr(numd.random, "shuffle", fake_shuffle)

    numd.doRename(path=str(tmp_path), width=4, start=0, randomise=True)

    assert called["value"] is True


def test_parse_args_defaults(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["numd"])

    args = numd.parseArgs()

    assert args.path is None
    assert args.dry_run is False
    assert args.width == 4
    assert args.start == 0
    assert args.prefix == ""
    assert args.randomise is False


def test_main_defaults_to_current_dir_and_dry_run(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["numd"])
    called = {}

    def fake_do_rename(**kwargs):
        called.update(kwargs)

    monkeypatch.setattr(numd, "doRename", fake_do_rename)

    numd.main()

    assert called["path"] == "."
    assert called["dry_run"] is True


def test_parse_args_with_all_options(monkeypatch):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            "numd",
            "~/example",
            "-D",
            "-w",
            "6",
            "-s",
            "100",
            "-p",
            "clip_",
            "-r",
        ],
    )

    args = numd.parseArgs()

    assert args.path == "~/example"
    assert args.dry_run is True
    assert args.width == 6
    assert args.start == 100
    assert args.prefix == "clip_"
    assert args.randomise is True


def test_parse_args_invalid_start_exits(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["numd", "~/example", "--start", "not-an-int"])

    with pytest.raises(SystemExit) as ex:
        numd.parseArgs()

    assert ex.value.code == 2
