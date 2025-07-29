import os
import sys


def fix_pyinstaller_workdir() -> None:
    """
    Changes the working directory to sys._MEIPASS if exists, to fix an error with pyinstaller on windows
    """
    try:
        os.chdir(sys._MEIPASS)  # type: ignore
    except AttributeError:
        pass
