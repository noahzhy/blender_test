import os
import sys
import glob

# from mathutils import Vector
from PIL import Image, ImageDraw

import numpy as np
import matplotlib
import matplotlib.pyplot as plt


# from pip._internal import main
# main(['install', 'pillow'])
# main(['install', '-r', 'requirements.txt'])

# function to rectangle the numpy array via given value
def rectangle(arr, value):
    target_arr = np.where(arr == value)
    # get the min and max of x and y
    min_x, max_x = np.min(target_arr[0]), np.max(target_arr[0])
    min_y, max_y = np.min(target_arr[1]), np.max(target_arr[1])
    return min_x, max_x, min_y, max_y


# load image as numpy array
def load_image(path):
    img = np.array(Image.open(path).convert('RGBA'))
    # divide rgb and alpha
    rgb, alpha = img[:, :, 0:3], img[:, :, 3]
    # convert to hsv
    hsv = matplotlib.colors.rgb_to_hsv(rgb)[:,:,0]
    # # covert to 0-16
    hsv = (hsv * 16).astype(np.uint8) + 1
    # where alpha is 0, set hsv to 0
    hsv[alpha == 0] = 0
    return hsv


if __name__ == "__main__":
    # path = "body_20230304172018_581351150011.png"
    path = "0001.png"
    img = load_image(path)

    min_x, max_x, min_y, max_y = rectangle(img, 1)
    # draw box via PIL
    img = Image.open(path).convert('RGBA')
    draw = ImageDraw.Draw(img)
    draw.rectangle((min_y, min_x, max_y, max_x), outline=(0, 255, 0, 255))

    # img.show()
    
    # show image
    plt.imshow(img, cmap='jet')
    plt.show()
