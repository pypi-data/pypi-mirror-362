# run.py
from aura_boy.boy_grid import grid, colorMap
from aura_boy.resize_grid import downscale_grid
from aura_boy.render import draw

if __name__ == "__main__":
    small_grid, small_map = downscale_grid(grid, colorMap, size=(64, 48))  # or (48, 48), (32, 32)
    draw(small_grid, small_map, scale=1)  # use scale=2 if you want bigger blocks
