import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw

import os
import sys
import glob
import random

# generate 24 color palette in hsv
def gen_palette(n=16):
    # generate 24 colors in order of hue with PIL
    img = Image.new('HSV', (1, n), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i in range(n):
        draw.point((0, i), (int(i * (256/n)), 255, 255))
    del draw
    # convert to rgb
    img = img.convert('RGB')
    # convert to numpy array
    colors = np.array(img)
    # resize to 2 columns
    colors = colors.reshape((2, 8, -1))
    return colors



if __name__ == "__main__":
    colors = gen_palette()
    # show it in PIL
    # img = Image.fromarray(colors, 'RGB')
    # img.show()

    # 放大到 32 倍
    colors = colors.repeat(64, axis=0).repeat(64, axis=1)


    # show it in matplotlib
    plt.imshow(colors, cmap='jet')
    plt.show()
    # save it withou white background
    plt.imsave('palette.png', colors, cmap='jet', format='png')
