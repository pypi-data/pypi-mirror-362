from ._colors import Colors
from ._effects import Effects
from ._show import slow, glare, typewriter
from ._cursor import Cursor


class Font:
    def __init__(
            self, base_color=None, text_color=None, shine_color=None,
            text=True, shine_width=2, effects=None,steps=255, time_glare=1,
            location_start=None, location_end=None, time_slow=1,
            time_typewriter=1, load=None
    ):
        self.base_color = base_color or Colors.BLACK
        self.text_color = text_color or Colors.WHITE
        self.shine_color = shine_color or Colors.BLACK
        self.location_start = location_start or []
        self.location_end = location_end or []
        self.effects = effects or []
        self.text = text
        self.shine_width = shine_width
        self.steps = steps
        self.time_glare = time_glare
        self.time_slow = time_slow
        self.time_typewriter = time_typewriter

        if load:
            for i in load.items():
                setattr(self, i[0], i[1])

    def __call__(self, *text, location=True, sep=" "):
        return Cursor.CLEAR_TEXT + ("".join(self.location_start) if location else "") +\
            self.text_color.string() + self.base_color.string(text=False) +\
            "".join(self.effects) + sep.join(text) + ("".join(self.location_end) if location else "")

    def glare(self, *text, file=None, sep=" ", end="\n", time=None):
        print(Cursor.CLEAR_TEXT + "".join(self.location_start), end="", flush=True)
        glare(self, *text, file=file, sep=sep, end=end, time=time)

    def slow(self, *text, file=None, sep=" ", end="\n", time=None):
        print(Cursor.CLEAR_TEXT + "".join(self.location_start), end="", flush=True)
        slow(self, *text, file=file, sep=sep, end=end, time=time)

    def typewriter(self, *text, file=None, sep=" ", end="\n", time=None):
        print(Cursor.CLEAR_TEXT + "".join(self.location_start), end="", flush=True)
        typewriter(self, *text, file=file, sep=sep, end=end, time=time)

    def json(self):
        return {
            "base_color": self.base_color,
            "text_color": self.text_color,
            "shine_color": self.shine_color,
            "location_start": self.location_start,
            "location_end": self.location_end,
            "effects": self.effects,
            "text": self.text,
            "shine_width": self.shine_width,
            "steps": self.steps,
            "time_glare": self.time_glare,
            "time_slow": self.time_slow,
            "time_typewriter": self.time_typewriter
        }


class Fonts:
    ERROR = {
        "base_color": Colors.RED, "text_color": Colors.WHITE, "effects": [Effects.Bold, Effects.Speedblink]
    }
    ERROR2 = {
        "base_color": Colors.BLACK, "text_color": Colors.RED, "effects": [Effects.Bold, Effects.Dubleline]
    }
    TITLE = {
        "base_color": Colors.BLACK, "text_color": Colors.YELLOW, "effects": [Effects.Bold, Effects.Upline, Effects.Italic]
    }
    HANDWRITING = {
        "base_color": Colors.BLACK, "text_color": Colors.GRAY, "effects": [Effects.Italic, Effects.Dim]
    }
    LOW = {
        "base_color": Colors.BLACK, "text_color": Colors.MAGENTA, "effects": [Effects.Dim]
    }
    HIGH = {
        "base_color": Colors.BLACK, "text_color": Colors.GREEN, "effects": [Effects.Bold]
    }
    CLASSIC = {
        "base_color": Colors.BLACK, "text_color": Colors.CYAN, "effects": []
    }
    CANCELED = {
        "base_color": Colors.BLACK, "text_color": Colors.BLUE, "effects": [Effects.Strikethrough]
    }
    MESSAGE = {
        "base_color": Colors.WHITE, "text_color": Colors.BLUE, "effects": []
    }
    IMPORTANT_MESSAGE = {
        "base_color": Colors.WHITE, "text_color": Colors.ORANGE, "effects": [Effects.Blink]
    }
    IMPORTANT_MESSAGE2 = {
        "base_color": Colors.RED, "text_color": Colors.GREEN, "effects": [Effects.Underline]
    }
