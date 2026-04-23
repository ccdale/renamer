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


def nextNumber(path, fn, start=0, width=4):
    try:
        # ifn = os.path.join(path, fn)
        bfn, ext = os.path.splitext(fn)
        if ext == ".part":
            return None
        cn = start
        while True:
            sfn = f"{nString(cn)}{ext}"
            ofn = os.path.join(path, sfn)
            if os.path.exists(ofn):
                cn += 1
                continue
            else:
                break
        return cn, ofn
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def doRename(width=4, start=0):
    try:
        path = "~/dwhelper"
        path = path if len(sys.argv) == 1 else sys.argv[1]
        if len(sys.argv) > 2:
            try:
                start = int(sys.argv[2])
            except ValueError:
                log.error(f"start value '{sys.argv[2]}' is not a valid integer")
                sys.exit(1)
        path = os.path.expanduser(path)
        if not os.path.isdir(path):
            log.error(f"{path} is not a directory")
            sys.exit(1)
        fns = fileList(path=path)
        tcn = 0
        for fn in fns:
            result = nextNumber(path, fn, start=start, width=width)
            if result is None:
                continue
            cn, ofn = result
            start = cn + 1
            ifn = os.path.join(path, fn)
            log.info(f"renaming: {ifn} to {ofn}")
            os.rename(ifn, ofn)
            tcn += 1
        log.info(f"renamed {tcn} files")
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def main():
    try:
        doRename(width=4, start=0)
    except Exception as e:
        errorExit(sys.exc_info()[2], e)


if __name__ == "__main__":
    if any(arg in ("-h", "--help") for arg in sys.argv[1:]):
        print(f"\nusage: {sys.argv[0]} [path] [start]\n")
        sys.exit(0)
    if len(sys.argv) > 3:
        log.error(f"usage: {sys.argv[0]} [path] [start]")
        sys.exit(1)
    main()
