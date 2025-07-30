from time import sleep as sl
from sys import __stdout__ as st

from ._colorsgenerator import levels_generator as lg
from ._colors import Color


def slow(font, *text, file=None, sep=" ", end="\n", time=None):
    file = file or st
    steps = max(font.steps, 2)
    delay = (font.time_slow if time is None else time) / steps
    txt = sep.join(text)
    R = "\b" * len(txt)

    for color, num_step in lg(font.shine_color.tuple, (font.text_color.tuple if font.text else font.base_color.tuple), steps):
        print(font(Color(*color).string(text=font.text) + txt, location=False), flush=True, file=file, end=R if num_step != steps-1 else "")
        sl(delay)

    print("".join(font.location_end), file=file, flush=True, end=font(end, location=False))


def glare(font, *text, file=None, sep=" ", end="\n", time=None):
    file = file or st
    shine_width = max(font.shine_width, 0)
    text = sep.join(text)
    colors = ((font.text_color.tuple  if font.text else font.base_color.tuple), font.shine_color.tuple)
    R = "\b" * len(text)

    def build_shiny_frame(pos):
        interpolate = lambda start, end, factor: int(start + (end - start) * factor)
        compute_color = lambda: tuple(interpolate(b, s, factor) for b, s in zip(*colors))
        colorize_char = lambda: color.string(text=font.text) + char
        result = ""
        for i, char in enumerate(text):
            factor = max(0, 1 - abs(i - pos) / (shine_width + 1))
            color = Color(*compute_color())
            result += colorize_char()
        return result + "\033[0m"

    i = 0
    delay = (font.time_glare if time is None else time) / len(range(-shine_width, len(text) + shine_width + 1))
    pos = 0
    for pos in range(-shine_width, len(text) + shine_width + 1):
        i += 1
        print(font(build_shiny_frame(pos), location=False), end=R, flush=True, file=file)
        sl(delay)

    print(font(build_shiny_frame(pos), location=False), end="", flush=True, file=file)
    print("".join(font.location_end), end=font(end, location=False), file=file, flush=True)


def typewriter(font, *text, file=None, sep=" ", end="\n", time=None):
    file = file or st
    text = sep.join(text)

    delay = (font.time_typewriter if time is None else time) / len(text)
    for char in text:
        print(font(char, location=False), end="", flush=True, file=file)
        sl(delay)

    print("".join(font.location_end), end=font(end, location=False), file=file, flush=True)
