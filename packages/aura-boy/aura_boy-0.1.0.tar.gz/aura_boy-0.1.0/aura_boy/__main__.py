# aura_boy/__main__.py
from .boy_grid import grid, colorMap
from .resize_grid import downscale_grid
from .render import draw

def main():
    small_grid, small_map = downscale_grid(grid, colorMap, size=(64, 48))
    draw(small_grid, small_map, scale=1)

if __name__ == "__main__":
    main()
