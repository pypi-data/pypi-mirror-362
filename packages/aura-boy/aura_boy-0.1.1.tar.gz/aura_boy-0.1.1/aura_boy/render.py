# render.py
from colorama import init, Style, Back
init()

def hex_to_ansi_bg(hex_color):
    hex_color = hex_color.lstrip("#")
    r, g, b = [int(hex_color[i:i+2], 16) for i in (0, 2, 4)]
    return f'\x1b[48;2;{r};{g};{b}m'

def draw(grid, colorMap, scale=1):
    for row in grid:
        for _ in range(scale):  # vertical scale
            for val in row:
                color = colorMap.get(val, "#000000")
                block = hex_to_ansi_bg(color) + '  ' * scale
                print(block, end='')
            print(Style.RESET_ALL)
