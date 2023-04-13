import os
from PIL import Image, ImageDraw
import glob
import numpy as np

import matplotlib
import matplotlib.pyplot as plt


# list 16 hsv colors using np.linspace
def gen_palette(n=16):
    # generate 16 colors in order of hue with PIL
    img = Image.new('HSV', (1, n), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    for i in range(n):
        draw.point((0, i), (int(i * (256/n)), 255, 255))
    del draw
    # convert to rgb
    img = img.convert('RGB')
    # convert to numpy array
    colors = np.array(img)
    return colors


colors = gen_palette()
# remove repeated colors
colors = np.unique(colors, axis=0)
# to single list
colors = colors.reshape(-1).tolist()
# every 3 elements is a color
colors = [tuple(colors[i:i+3]) for i in range(0, len(colors), 3)]
# to numpy array
colors = np.array(colors)



# from PIL import Image
# import numpy as np

# # 给定的16种颜色
# colors = [(255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), 
#           (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255),
#           (128, 128, 128), (128, 0, 0), (128, 128, 0), (0, 128, 0),
#           (128, 0, 128), (0, 128, 128), (0, 0, 128), (0, 0, 0)]

# # 加载图片


import cv2
import numpy as np

# # 给定的16种颜色
# colors = np.array([(0, 0, 255), (0, 128, 255), (0, 255, 255), (0, 255, 128), 
#           (0, 255, 0), (128, 255, 0), (255, 255, 0), (255, 128, 0),
#           (255, 0, 0), (255, 0, 128), (255, 0, 255), (128, 0, 255),
#           (0, 0, 255), (0, 255, 255), (255, 255, 255), (0, 0, 0)])


def gen_pure_color(path):
    f_name = os.path.basename(path)

    # 加载图片
    img = cv2.imread(path)
    # 将图片转换为RGB模式
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 将每个像素点替换为与其最近的给定颜色
    distances = np.sqrt(((img - colors[:, np.newaxis, np.newaxis])**2).sum(axis=3))
    labels = np.argmin(distances, axis=0)
    img_array = colors[labels]

    img_array = np.uint8(img_array)


    # using PIL to save image
    img = Image.fromarray(img_array, 'RGB')
    img.save(f_name, 'PNG', quality=100)

    # # 将数组转换回图片格式
    # new_img = cv2.cvtColor(np.uint8(img_array), cv2.COLOR_RGB2BGR)

    # # resize to 512x512
    # new_img = cv2.resize(new_img, (512, 512), interpolation=cv2.INTER_NEAREST)
    # # 去除孤立的像素点，用旁边的像素点填充
    # new_img = cv2.medianBlur(new_img, 3)


    # # 100% 保存图片
    # cv2.imwrite(f_name, new_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
    # load it in matplotlib
    # plt.imshow(new_img)
    # plt.show()

for f in glob.glob('texture/*.png'):
    gen_pure_color(f)


