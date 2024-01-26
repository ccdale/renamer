import os
import sys

import ccalogging

__version__ = "0.1.0"
__appname__ = "renamer"

log = ccalogging.log


def errorNotify(exci, e, fname=None):
    lineno = exci.tb_lineno
    if fname is None:
        fname = exci.tb_frame.f_code.co_name
    ename = type(e).__name__
    msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
    log.error(msg)


def errorRaise(exci, e, fname=None):
    errorNotify(exci, e, fname)
    raise


def errorExit(exci, e, fname=None):
    errorNotify(exci, e, fname)
    sys.exit(1)


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
        ifn = os.path.join(path, fn)
        bfn, ext = os.path.splitext(fn)
        if ext == ".part":
            return None
        cn = start
        while True:
            sfn = f"{nString(cn)}{ext}"
            ofn = os.path.join(path, sfn)
            if os.path.isfile(ofn):
                cn += 1
                continue
            else:
                break
        return cn, sfn
    except Exception as e:
        errorRaise(sys.exc_info()[2], e)


def doRename(width=4, start=0):
    try:
        path = "/home/chris/dwhelper" if len(sys.argv) == 1 else sys.argv[1]
        if not os.path.isdir(path):
            print(f"{path} is not a directory")
            sys.exit(1)
        fns = fileList(path=path)
        for fn in fns:
            cn, ofn = nextNumber(path, fn, start=start, width=width)
            if cn is None:
                continue
            ifn = os.path.join(path, fn)
            print(f"renaming: {ifn} to {ofn}")
            os.rename(ifn, ofn)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
