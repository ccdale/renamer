import argparse
import os
import sys

from renamer import errorExit, errorNotify, errorRaise, log


def fileList(path):
    try:
        return [x for x in os.listdir(path) if os.path.isfile(os.path.join(path, x))]
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)


def nString(cn, width=4):
    try:
        return f"{cn:>0{width}}"
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def nextNumber(path, fn, start=0, width=4, prefix=""):
    try:
        _, ext = os.path.splitext(fn)
        if ext == ".part":
            return None
        cn = start
        while True:
            sfn = f"{prefix}{nString(cn, width=width)}{ext}"
            ofn = os.path.join(path, sfn)
            if os.path.exists(ofn):
                cn += 1
                continue
            else:
                break
        return cn, ofn
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def doRename(path="~/dwhelper", width=4, start=0, prefix="", dry_run=False):
    try:
        path = os.path.expanduser(path)
        if not os.path.isdir(path):
            log.error(f"{path} is not a directory")
            sys.exit(1)
        fns = fileList(path=path)
        if fns:
            max_index = start + len(fns) - 1
            required_width = len(str(max_index))
            if required_width > width:
                width = required_width
        tcn = 0
        for fn in fns:
            result = nextNumber(path, fn, start=start, width=width, prefix=prefix)
            if result is None:
                continue
            cn, ofn = result
            start = cn + 1
            ifn = os.path.join(path, fn)
            action = "would rename" if dry_run else "renaming"
            log.info(f"{action}: {ifn} to {ofn}")
            if not dry_run:
                os.rename(ifn, ofn)
            tcn += 1
        summary = "would rename" if dry_run else "renamed"
        log.info(f"{summary} {tcn} files")
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def parseArgs(argv=None):
    parser = argparse.ArgumentParser(
        prog="numd",
        description="Rename files in a directory with incrementing numeric filenames.",
    )
    parser.add_argument("path", nargs="?", default="~/dwhelper")
    parser.add_argument("-D", "--dry-run", action="store_true")
    parser.add_argument("-w", "--width", type=int, default=4)
    parser.add_argument("-s", "--start", type=int, default=0)
    parser.add_argument("-p", "--prefix", default="")
    return parser.parse_args(argv)


def main():
    try:
        args = parseArgs()
        doRename(
            path=args.path,
            width=args.width,
            start=args.start,
            prefix=args.prefix,
            dry_run=args.dry_run,
        )
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


if __name__ == "__main__":
    main()
