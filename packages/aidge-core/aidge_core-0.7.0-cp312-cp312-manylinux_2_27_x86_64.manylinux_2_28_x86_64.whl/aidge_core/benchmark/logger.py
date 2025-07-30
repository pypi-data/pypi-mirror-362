from enum import Enum

COLOR_ON = True

class Color(Enum):
    RED = '31'
    GREEN = '32'
    YELLOW = '33'
    BLUE = '34'
    MAGENTA = '35'
    CYAN = '36'
    WHITE = '37'

class Logger:
    def __init__(self, color_on: bool = True):
        self.color_on = color_on

    def to_color(self, msg: str, color: Color, bold: bool = False) -> str:
        if self.color_on:
            return f"\033[{int(bold)};{color.value}m{msg}\033[0m"
        else:
            return msg
