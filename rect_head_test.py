import os
import sys

import numpy as np
from PIL import Image, ImageDraw


# draw a rectangle in a image via given coordinates (xmin, ymin, xmax, ymax)
def draw_rectangle(image, coordinates, color=(255, 0, 0)):
    draw = ImageDraw.Draw(image)
    # * 512
    coordinates = [int(i * 512) for i in coordinates]
    draw.rectangle(coordinates, outline=color)
    return image


if __name__ == "__main__":
    given_coordinates = "0.721695 0.216333 1.0 0.692503"
    # split coordinates
    given_coordinates = given_coordinates.split(" ")
    # convert to float
    given_coordinates = [float(i) for i in given_coordinates]
    # convert to numpy array
    given_coordinates = np.array(given_coordinates)

    # get image path
    image_path = "untitled.png"
    # load image
    image = Image.open(image_path)
    # draw a rectangle in image
    image = draw_rectangle(image, given_coordinates)
    image.show()
