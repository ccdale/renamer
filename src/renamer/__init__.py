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


def doRename():
    try:
        path = "/home/chris/dwhelper" if len(sys.argv) == 1 else sys.argv[1]
        fns = fileList(path=path)
        for cn, fn in enumerate(fns):
            ifn = os.path.join("/home/chris/dwhelper", fn)
            bfn, ext = os.path.splitext(fn)
            if ext == ".part":
                continue
            ofn = os.path.join("/home/chris/dwhelper", f"{cn}{ext}")
            print(f"renaming: {ifn} to {ofn}")
            os.rename(ifn, ofn)
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
