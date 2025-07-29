# resize_grid.py
from PIL import Image
import numpy as np

def downscale_grid(grid, colorMap, size=(64, 48)):
    # Convert index grid to RGB array
    index_to_rgb = {
        k: tuple(int(colorMap[k].lstrip("#")[i:i+2], 16) for i in (0, 2, 4))
        for k in colorMap
    }

    rgb_array = np.array([
        [index_to_rgb.get(val, (0, 0, 0)) for val in row]
        for row in grid
    ], dtype=np.uint8)

    img = Image.fromarray(rgb_array, mode="RGB")
    img_resized = img.resize(size, resample=Image.NEAREST)
    downscaled_rgb = np.array(img_resized)

    # Convert back to new index grid and colorMap
    new_grid = []
    new_colorMap = {}
    color_to_index = {}
    index = 1

    for row in downscaled_rgb:
        new_row = []
        for rgb in row:
            hex_color = '#%02x%02x%02x' % tuple(rgb)
            if hex_color not in color_to_index:
                color_to_index[hex_color] = index
                new_colorMap[index] = hex_color
                index += 1
            new_row.append(color_to_index[hex_color])
        new_grid.append(new_row)

    return new_grid, new_colorMap
