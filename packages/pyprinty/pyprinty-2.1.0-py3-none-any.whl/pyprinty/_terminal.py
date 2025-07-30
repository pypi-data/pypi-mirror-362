import sys
import os


def good():
    return sys.stdout.isatty()


def size():
    x = os.get_terminal_size()
    return (x.columns, x.lines) if good() else None
