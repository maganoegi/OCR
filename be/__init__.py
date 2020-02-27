
import cv2
# import keras
import numpy as np
from matplotlib import pyplot as plt
import os
import random
import math

from mnist import MNIST

def extract(data_root, Testing=False):
    mndata = MNIST(data_root)
    images, labels = mndata.load_training() if not Testing else mndata.load_testing()
    return mndata, images, labels

def print_mndata_digit(index):
    print(mndata.display(images[index]))
    size = math.sqrt(len(images[index]))
    print(f"Label = {labels[index]}\tSize = {int(size)} x {int(size)}")

def train(images, labels):
    pass

if __name__ == '__main__':

    # Path to Data Directory
    parentDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_root = parentDir + "/data/"
    
    # Extract images and labels
    mndata, images, labels = extract(data_root)

    # Display in terminal
    index = random.randrange(0, len(images))
    print_mndata_digit(index)