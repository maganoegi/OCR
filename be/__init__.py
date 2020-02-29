
import cv2
# import keras
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import image as pltImage
import os
import random
import math
import numpy as np 
from PIL import Image, ImageFilter
from mnist import MNIST

THRESHOLD = 100 # grey
SIZE = 28


def MNIST_extract(data_root, Testing=False):
    mndata = MNIST(data_root)
    images, labels = mndata.load_training() if not Testing else mndata.load_testing()
    return mndata, images, labels


def clean_MNIST(line_img):
    return [x if x > THRESHOLD else 0 for x in line_img]

def print_MNIST_digit(line_img):

    print(mndata.display(line_img))
    for i in range(SIZE):
        line = ""
        for j in range(SIZE):
            line += "\033[31m█\033[0m" if line_img[i*SIZE + j] > 100 else "█"
        print(line)

def train(images, labels):
    print("\n------------------- TRAINING -------------------\n")



def MNIST_convert():

    path = './test_input.png'
    im = Image.open(path).convert('L')
    width = float(im.size[0])
    height = float(im.size[1])
    newImage = Image.new('L', (SIZE, SIZE), (255))  # creates white canvas of SIZExSIZE pixels

    if width > height:  # check which dimension is bigger
        # Width is bigger. Width becomes 20 pixels.
        nheight = int(round((20.0 / width * height), 0))  # resize height according to ratio width
        if (nheight == 0):  # rare case but minimum is 1 pixel
            nheight = 1
            # resize and sharpen
        img = im.resize((20, nheight), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wtop = int(round(((SIZE - nheight) / 2), 0))  # calculate horizontal position
        newImage.paste(img, (4, wtop))  # paste resized image on white canvas
    else:
        # Height is bigger. Heigth becomes 20 pixels.
        nwidth = int(round((20.0 / height * width), 0))  # resize width according to ratio height
        if (nwidth == 0):  # rare case but minimum is 1 pixel
            nwidth = 1
            # resize and sharpen
        img = im.resize((nwidth, 20), Image.ANTIALIAS).filter(ImageFilter.SHARPEN)
        wleft = int(round(((SIZE - nwidth) / 2), 0))  # caculate vertical pozition
        newImage.paste(img, (wleft, 4))  # paste resized image on white canvas


    imgArray = np.array(newImage.getdata())  # get pixel values
    
    imgArrayInv = 255 - imgArray

    imgArrayInv = clean_MNIST(imgArrayInv)

    return imgArrayInv


if __name__ == '__main__':

    # Path to Data Directory
    parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_root = parentDir + "/data/"
    
    # Extract images and labels
    mndata, images, labels = MNIST_extract(data_root)

    # Display individual digit in terminal
    index = random.randrange(0, len(images))
    img = images[index]

    print_MNIST_digit(img)

    # Test MNIST conversion
    custom = MNIST_convert()
    print_MNIST_digit(custom)