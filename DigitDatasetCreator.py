## @package DigitDatasetCreator
#
#

import imageio
import matplotlib.pyplot
import numpy
import time
from PIL import Image, ImageDraw, ImageFont
import cv2
import os

matplotlib.pyplot.ion()

def displayFile (filename):
    print(filename)
    img=cv2.imread(filename,cv2.IMREAD_GRAYSCALE)
    img_data = 255.0 - img.reshape(28*28)
    img_data = (img_data / 255.0 * 0.99) + 0.01
    image_array = numpy.asfarray(img_data).reshape((28,28))
    matplotlib.pyplot.imshow(image_array,cmap='binary',interpolation=None)
pass


fnt = ImageFont.truetype('font.ttf', 26)
for number in range(10):
    new_img = Image.new('RGB', (28, 28), color = (255, 255, 255))
    d = ImageDraw.Draw(new_img)
    d.text((7,-2), str(number), font=fnt, fill=(0, 0, 0))
    new_img.save(str(number)+'.png')
pass

directory = os.getcwd()
for file in os.listdir(directory):
    filename = os.fsdecode(file)
    if filename.endswith(".png"):
        displayFile(filename)
pass


