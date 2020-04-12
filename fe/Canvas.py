
import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QSize
import cv2
from PIL import Image, ImageFilter
import numpy as np
from scipy import ndimage
import subprocess

SIZE = 20
THRESHOLD = 5
PENWIDTH = 15
KERNELVAL = 2
KSIZE = (KERNELVAL, KERNELVAL)
DIMENSION = 500


class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(500, 500)
        self.setPixmap(pixmap)
        self.penWidth = PENWIDTH
        
        self.last_x, self.last_y = None, None

        self.pixmap().fill(QColor(Qt.white))

    def set_pen_color(self, c):
        self.pen_color = QColor(c)

    def mouseMoveEvent(self, e):
        if self.last_x is None: # First event.
            self.last_x = e.x()
            self.last_y = e.y()
            return # Ignore the first time.

        painter = QPainter(self.pixmap())
        p = painter.pen()
        p.setWidth(self.penWidth)
        p.setColor(QColor(Qt.black))
        painter.setPen(p)
        painter.drawLine(self.last_x, self.last_y, e.x(), e.y())
        painter.end()
        self.update()

        # Update the origin for next time.
        self.last_x = e.x()
        self.last_y = e.y()

    def mouseReleaseEvent(self, e):
        self.last_x = None
        self.last_y = None
    
    def reset(self):
        self.pixmap().fill(QColor(Qt.white))
        self.update()

    def post_data(self):
        pixmap = self.pixmap()

        treated_image = preprocess(pixmap)


def preprocess(q_pixmap):
    q_image = QPixmap.toImage(q_pixmap)

    depth = q_image.depth()

    img_array = QImage_2_List(q_image, DIMENSION, DIMENSION, depth)

    inversed = 255 - img_array

    centered = center_image(inversed) 

    print(find_scaling_factor(centered))

    resized = cv2.resize(src = centered, dsize = (SIZE, SIZE))

    blurred = cv2.blur(resized, KSIZE)

    _ret, thresh = cv2.threshold(blurred, THRESHOLD, 255, cv2.THRESH_BINARY)
    
    # inverting for display purposes, for some reason it does not save correctly
    cv2.imwrite('processed_img.png', 255 - thresh) 

    return thresh

def find_scaling_factor(img):
    return scan_vertical(img)

def scan_horizontal(img):
    min_index = DIMENSION
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

# def scan_vertical(img):
#     min_index = DIMENSION
#     left = 0
#     for y in img:
#         for index, x in enumerate(y):
            
#             if x[0] > 0 and index < min_index:
#                 min_index = index
#                 left = index
#                 break

#     max_index = 0
#     right = 0
#     for y in img:
#         for index in reversed(range(len(y))):
#             x = y[index]
#             if x[0] > 0 and index > max_index:
#                 max_index = index
#                 right = index
#                 break

#     return left, right



def center_image(img):
    cm = ndimage.measurements.center_of_mass(img)
    delta_y = DIMENSION/2 - cm[0]
    delta_x = DIMENSION/2 - cm[1]
    translation_matrix = np.float32([[1, 0, delta_x], [0, 1, delta_y]])
    return cv2.warpAffine(img, translation_matrix, (DIMENSION, DIMENSION)) 

def QImage_2_List(img, width, height, depth):
    img = img.convertToFormat(4)

    ptr = img.bits()
    ptr.setsize(img.byteCount())

    return np.array(ptr).reshape(height, width, depth//8)
