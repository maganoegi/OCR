
import cv2
# import keras
import numpy as np
from matplotlib import pyplot as plt
import os
import random
import math
import numpy as np 

from mnist import MNIST


def MNIST_extract(data_root, Testing=False):
    mndata = MNIST(data_root)
    images, labels = mndata.load_training() if not Testing else mndata.load_testing()
    return mndata, images, labels


def print_MNIST_digit(index):
    img = images[index]
    print(mndata.display(img))
    size = int(math.sqrt(len(img)))
    print(f"Label = {labels[index]}\tSize = {size} x {size}")


    for i in range(size):
        line = ""
        for j in range(size):
            line += "\033[31m█\033[0m" if img[i*size + j] != 0 else "█" 
        print(line)

def train(images, labels):
    print("\n------------------- TRAINING -------------------\n")


if __name__ == '__main__':

    # Path to Data Directory
    parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_root = parentDir + "/data/"
    
    # Extract images and labels
    mndata, images, labels = MNIST_extract(data_root)

    # Display individual digit in terminal
    index = random.randrange(0, len(images))
    print_MNIST_digit(index)