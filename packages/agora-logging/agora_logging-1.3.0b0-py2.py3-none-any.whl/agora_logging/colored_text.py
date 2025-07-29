from enum import Enum

'''
Color value for logging
'''

#  \x1b[        Hex 'ESC' + '['
#  integer      (Style Enum)
#  ;            Separator
#  3 + integer  integer = Foreground Color (Color Enum)
#  ;            Separator
#  4 + integer  integer = Background Color (Color Enum)
#  m            Stopper


class Style(Enum):
    Normal = 0
    Bold = 1
    Light = 2
    Italicized = 3
    Underlined = 4
    Blink = 5


class Color(Enum):
    Black = 0
    Red = 1
    Green = 2
    Yellow = 3
    Blue = 4
    Purple = 5
    Cyan = 6
    White = 7
    Default = 9


class ColoredText:
    '''
    Color value for logging
    '''
    @staticmethod
    def gray(msg):
        return ColoredText.message(msg, Style.Bold, Color.Black)

    @staticmethod
    def green(msg):
        return ColoredText.message(msg, Style.Bold, Color.Green)

    @staticmethod
    def dark_red(msg):
        return ColoredText.message(msg, Style.Bold, Color.White, Color.Red)

    @staticmethod
    def yellow(msg):
        return ColoredText.message(msg, Style.Normal, Color.Black, Color.Yellow)

    @staticmethod
    def red(msg):
        return ColoredText.message(msg, Style.Normal, Color.Black, Color.Red)

    @staticmethod
    def message(message: str, style: Style, fg_color: Color, bg_color: Color = Color.Default):
        style_str = str(style.value)
        fg_color_str = ';3' + str(fg_color.value)
        bg_color_str = ';4' + str(bg_color.value)
        return '\x1b[' + style_str + fg_color_str + bg_color_str + 'm' + message.strip() + '\x1b[0m\n'
