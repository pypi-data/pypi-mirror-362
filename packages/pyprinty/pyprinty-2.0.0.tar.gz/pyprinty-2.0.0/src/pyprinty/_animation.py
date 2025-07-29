class Animation:
    def __init__(self, load=None):
        self.fonts = load or {}
        self.list_freeze = []

    def __call__(self, name):
        return self.fonts[name]["font"] if name in self.fonts else None

    def add_font(self, name, font, mode="print"):
        self.fonts[name] = {"font": font, "mode": mode}

    def freeze(self, name):
        if not name in self.list_freeze and name in self.fonts:
            self.list_freeze.append(name)

    def thaw(self, name):
        if name in self.list_freeze:
            self.list_freeze.remove(name)

    def send(self, font_name, *text, file=None, end="\n", sep=" "):
        if not font_name in self.list_freeze:
            font = self.fonts[font_name]["font"]
            mode = self.fonts[font_name]["mode"]
            if mode == "print":
                from sys import __stdout__ as st
                print(font(*text, file=file or st, sep=sep), end=end, flush=True)
            elif mode == "sun":
                font.sun(*text, file=file, sep=sep, end=end)
            elif mode == "rank":
                font.slow(*text, file=file, sep=sep, end=end)
