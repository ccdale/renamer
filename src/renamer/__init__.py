import subprocess
import sys
from pathlib import Path

import ccalogging
import tomllib

__version__ = "0.1.11"
__appname__ = "numd"

ccalogging.setConsoleOut()
ccalogging.setInfo()
log = ccalogging.log


def errorNotify(exci, e, fname=None):
    lineno = exci.tb_lineno
    if fname is None:
        fname = exci.tb_frame.f_code.co_name
    ename = type(e).__name__
    msg = f"{ename} Exception at line {lineno} in function {fname}: {e}"
    print(msg)


def errorRaise(exci, e, fname=None):
    errorNotify(exci, e, fname)
    raise


def errorExit(exci, e, fname=None):
    errorNotify(exci, e, fname)
    sys.exit(1)


def gitroot() -> str:
    try:
        return (
            subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True)
            .splitlines()
            .pop()
        )
    except Exception as e:
        errorExit(sys.exc_info()[2], e)
        return ""


def getVersion() -> str:
    try:
        git_root = gitroot()
        if not git_root:
            return "0.0.0"
        pyproject_path = Path(git_root) / "pyproject.toml"
        if not pyproject_path.exists():
            return "0.0.0"
        with open(pyproject_path, "rb") as f:
            pyproject_data = tomllib.load(f)
        return pyproject_data.get("project", {}).get("version", "0.0.0")
    except Exception as e:
        errorExit(sys.exc_info()[2], e)
        return "0.0.0"


class colours:
    reset = "\033[0m"
    bold = "\033[01m"
    disable = "\033[02m"
    underline = "\033[04m"
    reverse = "\033[07m"
    strikethrough = "\033[09m"
    invisible = "\033[08m"

    class fg:
        black = "\033[30m"
        red = "\033[31m"
        green = "\033[32m"
        orange = "\033[33m"
        blue = "\033[34m"
        purple = "\033[35m"
        cyan = "\033[36m"
        lightgray = "\033[37m"
        darkgray = "\033[90m"
        lightred = "\033[91m"
        lightgreen = "\033[92m"
        yellow = "\033[93m"
        lightblue = "\033[94m"
        pink = "\033[95m"
        lightcyan = "\033[96m"

    class bg:
        black = "\033[40m"
        red = "\033[41m"
        green = "\033[42m"
        orange = "\033[43m"
        blue = "\033[44m"
        purple = "\033[45m"
        cyan = "\033[46m"
        lightgray = "\033[47m"


def progressBar(
    progress,
    total,
    showValues=False,
    remove=False,
    newline=False,
    colour=colours.fg.green,
    bgcolour=colours.fg.darkgray,
):
    try:
        percent = 100 * (progress / float(total))
        fill = chr(9609)
        blank = chr(9617)
        blanks = blank * (100 - int(percent))
        fills = fill * int(percent)
        bar = f"{colour}{fills}{bgcolour}{blanks}"
        if showValues:
            msg = f"\r|{bar}| {progress} / {total}"
        else:
            msg = f"\r|{bar}| {percent:.2f}"
        print(msg, end="\r")
        if remove:
            splat = " " * len(msg)
            if newline:
                print(f"{colours.reset}{splat}")
            else:
                print(f"{colours.reset}{splat}", end="\r")
    except Exception as e:
        errorNotify(sys.exc_info()[2], e)
