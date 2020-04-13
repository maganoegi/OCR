
import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QSize
import cv2
import numpy as np
from scipy import ndimage
import requests
import config
import json


class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(500, 500)
        self.setPixmap(pixmap)
        self.penWidth = 15
        
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
        text= "   2   "
        if text != None:
            label = text.strip()

            if label == "":
                pass
            else:
                pixmap = self.pixmap()
                mode = "train"
                json_data = post_pixmap(pixmap, mode, label)


def post_pixmap(q_pixmap, mode, label):
    q_image = QPixmap.toImage(q_pixmap)
    width = q_image.width()
    height = q_image.height()
    depth = q_image.depth()
    img_array = QImage_2_List(q_image, width, height, depth)

    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    path = "/".join([config.host_url, mode, label])

    _, img_encoded = cv2.imencode('.jpg', img_array)
    data = img_encoded.tostring()
    response = requests.post(path, data=data, headers=headers)
    
    print(json.loads(response.text))


def QImage_2_List(img, width, height, depth):
    img = img.convertToFormat(4)

    ptr = img.bits()
    ptr.setsize(img.byteCount())

    return np.array(ptr).reshape(height, width, depth//8)
