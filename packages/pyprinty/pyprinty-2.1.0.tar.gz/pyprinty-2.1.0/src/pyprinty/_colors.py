class Color:
    def __init__(self, r, g, b):
        self.red = r
        self.green = g
        self.blue = b
        self.tuple = (r, g, b)

    def string(self, text=True):
        return f"\033[{38 if text else 48};2;{self.red};{self.green};{self.blue}m"


class Colors:
    RED     = Color(255, 0, 0)
    GREEN   = Color(0, 255, 0)
    BLUE    = Color(0, 0, 255)
    YELLOW  = Color(255, 255, 0)
    CYAN    = Color(0, 255, 255)
    MAGENTA = Color(255, 0, 255)
    BLACK   = Color(0, 0, 0)
    WHITE   = Color(255, 255, 255)
    GRAY    = Color(128, 128, 128)
    ORANGE  = Color(242, 135, 5)
    Initialize_text_color = "\033[39m"
    Initialize_background_color = "\033[49m"
    Initialize_colors = "\033[39;49m"
