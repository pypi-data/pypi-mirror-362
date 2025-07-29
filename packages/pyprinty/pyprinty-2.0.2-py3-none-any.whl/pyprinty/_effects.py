class Spacial:
    URL = lambda url, text: f"\033]8;;{url}\033\\{text}\033]8;;\033\\"
    WINDOW_TITLE = lambda title: f"\033]0;{title}\007"
    WINDOW_COLOR = lambda r, g, b: f"\033]11;{f"#{r:02X}{g:02X}{b:02X}"}\007"
    DONG = "\a"


class Effects:
    Bold          = "\033[1m"
    Dim           = "\033[2m"
    Italic        = "\033[3m"
    Underline     = "\033[4m"
    Dubleline     = "\033[21m"
    Blink         = "\033[5m"
    Speedblink    = "\033[6m"
    Strikethrough = "\033[9m"
    Upline        = "\033[53m"
    Transparent = "\033[8m"
    CLEAR_EFFECTS = "\033[8;53;9;6;5;21;4;3;2;1m"
