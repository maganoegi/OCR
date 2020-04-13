import cv2
import numpy as np
from scipy import ndimage
import os
import lib.config as config


def getFileNumberName(path):
    _root, _dirs, files = next(os.walk(path))
    return len(files)


def append_to_dataset(img_array, label):
    file_format = ".png"
    # TODO: CREATE FOLDERS IF NOT PRESENT!!!
    this_dir = os.path.dirname(os.path.abspath(__file__))
    base_path = os.path.dirname(this_dir)
    labeled_path = os.path.join(base_path, "digits", label)
    file_name = f"{getFileNumberName(labeled_path)}{file_format}"

    path = os.path.join(labeled_path, file_name)

    cv2.imwrite(path, img_array)


def preprocess(img_array):

    inversed = 255 - img_array

    centered = center_image(inversed) 

    stretched = stretch_image(inversed)

    resized = cv2.resize(src = stretched, dsize = (config.SIZE, config.SIZE))

    blurred = cv2.blur(resized, config.KSIZE)

    _ret, thresh = cv2.threshold(blurred, config.THRESHOLD, 255, cv2.THRESH_BINARY)
    
    # reverting for display purposes, for some reason it does not save correctly when inverted
    cv2.imwrite('processed_img.png', 255 - thresh) 

    return thresh

def stretch_image(img):
    top, right, bottom, left = find_edges(img)
    tl = [left, top]
    tr = [right, top]
    bl = [left, bottom]
    br = [right, bottom]

    src = np.array([tl, tr, br, bl], 'float32')

    dst = np.array([[0,0], [config.DIMENSION-1,0], [config.DIMENSION-1,config.DIMENSION-1], [0,config.DIMENSION-1]], 'float32')

    M = cv2.getPerspectiveTransform(src, dst)

    return cv2.warpPerspective(img, M, (config.DIMENSION, config.DIMENSION))


def find_edges(img):
    left, right = scan_horizontal(img)
    top, bottom = scan_vertical(img)

    return top, right, bottom, left


def scan_horizontal(img):
    min_index = config.DIMENSION
    left = 0
    for y in img:
        for index, x in enumerate(y):
            
            if x[0] > 0 and index < min_index:
                min_index = index
                left = index
                break

    max_index = 0
    right = 0
    for y in img:
        for index in reversed(range(len(y))):
            x = y[index]
            if x[0] > 0 and index > max_index:
                max_index = index
                right = index
                break

    return left, right

def scan_vertical(img):
    min_index = config.DIMENSION
    top = 0
    for i in range(config.DIMENSION):
        column = img[:, i]
        for j in range(config.DIMENSION):
            if column[j][0] > 0 and j < min_index:
                min_index = j
                top = j
                break

    max_index = 0
    bottom = 0
    for i in range(config.DIMENSION):
        column = img[:, i]
        for j in range(config.DIMENSION):
            if column[j][0] > 0 and j > max_index:
                max_index = j
                bottom = j
                break

    return top, bottom


def center_image(img):
    cm = ndimage.measurements.center_of_mass(img)
    delta_y = config.DIMENSION/2 - cm[0]
    delta_x = config.DIMENSION/2 - cm[1]
    translation_matrix = np.float32([[1, 0, delta_x], [0, 1, delta_y]])
    return cv2.warpAffine(img, translation_matrix, (config.DIMENSION, config.DIMENSION)) 