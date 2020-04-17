
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

