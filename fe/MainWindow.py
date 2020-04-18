

import sys
from PyQt5.QtWidgets import QWidget, QMessageBox, QGroupBox, QMainWindow, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSlider, QFileDialog, QRadioButton, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QSize
from Canvas import Canvas
import time
import requests
import config
import numpy as np
import cv2
import json

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setStyleSheet("background-color: #123456;")  
        self.setWindowTitle("OCR - Sergey Platonov - Hepia")
        left = 300
        top = 0
        width = 800
        height = 900
        self.setGeometry(left, top, width, height)
        self.setFixedSize(width, height)

        self.init_UIElements()
        self.init_Layouts()

        self.mode = "train"

    def init_UIElements(self):

        elementWidth = 400
        elementHeight = 40
        self.letterColor = "cornflowerblue"
        fontSize = 20
        font = "Roboto"
        fontWeight = QFont.Bold

        self.canvas = Canvas()

        self.fit_button = QPushButton(self)
        self.fit_button.setText("fit") 
        self.fit_button.clicked.connect(self.fit_clicked)
        self.fit_button.setFixedSize(QSize(elementWidth, elementHeight))
        self.fit_button.setStyleSheet("QPushButton {color: " + self.letterColor + "};")
        self.fit_button.setFont(QFont(font, fontSize, fontWeight))

        self.erase_button = QPushButton(self)
        self.erase_button.setText("erase") 
        self.erase_button.clicked.connect(self.erase_canvas)
        self.erase_button.setFixedSize(QSize(elementWidth, elementHeight))
        self.erase_button.setStyleSheet("QPushButton {color: " + self.letterColor + "};")
        self.erase_button.setFont(QFont(font, fontSize, fontWeight))

        self.submit_button = QPushButton(self)
        self.submit_button.setText("submit") 
        self.submit_button.clicked.connect(self.submit_clicked)
        self.submit_button.setFixedSize(QSize(elementWidth, elementHeight))
        self.submit_button.setStyleSheet("QPushButton {color: " + self.letterColor + "};")
        self.submit_button.setFont(QFont(font, fontSize, fontWeight))

        self.label_input = QLineEdit(self)
        self.label_input.setFont(QFont(font, fontSize, fontWeight))
        self.label_input.setStyleSheet("QLineEdit {color: " + self.letterColor + "};")
        self.label_input.setFont(QFont(font, fontSize, fontWeight))
        self.label_input.setFixedSize(QSize(elementWidth, elementHeight))

        self.score_labels = []
        for i in range(10):
            label = QLabel(self)
            label.setText(str(i))
            label.setStyleSheet("QLabel {color: " + self.letterColor + "};")
            label.setFont(QFont(font, fontSize, fontWeight))
            self.score_labels.append(label)

        self.train_Rbutton = QRadioButton(self)
        self.train_Rbutton.setText("training")
        self.train_Rbutton.setChecked(True)
        self.train_Rbutton.toggled.connect(self.train_selected)
        self.train_Rbutton.setStyleSheet("QRadioButton {color: " + self.letterColor + "};")
        self.train_Rbutton.setFont(QFont(font, 15, fontWeight))

        self.test_Rbutton = QRadioButton(self)
        self.test_Rbutton.setText("testing")
        self.test_Rbutton.toggled.connect(self.test_selected)
        self.test_Rbutton.setStyleSheet("QRadioButton {color: " + self.letterColor + "};")
        self.test_Rbutton.setFont(QFont(font, 15, fontWeight))
        

    def init_Layouts(self):
        self.w = QWidget()

        # Define containers...
        self.main_container = QVBoxLayout()
        
        self.canvas_container = QHBoxLayout()
        self.canvas_container.setAlignment(Qt.AlignHCenter)

        self.radio_container = QHBoxLayout()
        self.radio_container.setAlignment(Qt.AlignHCenter)

        self.button_label_container = QHBoxLayout()
        self.button_label_container.setSpacing(30)
        self.button_label_container

        self.button_container = QVBoxLayout()
        self.label_container = QVBoxLayout()
        self.label_container.setSpacing(5)


        # ... fill them with widgets ...
        self.canvas_container.addWidget(self.canvas)
        self.radio_container.addWidget(self.train_Rbutton)
        self.radio_container.addWidget(self.test_Rbutton)

        self.button_container.addWidget(self.submit_button)
        self.button_container.addWidget(self.erase_button)
        self.button_container.addWidget(self.fit_button)
        self.button_container.addWidget(self.label_input)

        for i in range(10):
            self.label_container.addWidget(self.score_labels[i])


        # ... and combine the containers
        self.setCentralWidget(self.w)
        self.w.setLayout(self.main_container)

        self.main_container.addLayout(self.canvas_container)
        self.main_container.addLayout(self.radio_container)
        self.main_container.addLayout(self.button_label_container)

        self.button_label_container.addLayout(self.button_container)
        self.button_label_container.addLayout(self.label_container)

    def fit_clicked(self):
        """ sends a signal to the BE that triggers a training procedure """
        self.enable_UI_elements(False)

        mode = self.mode
        content_type, headers, path = get_request_resources(mode)
        data = ""
        response = requests.post(path, data=data, headers=headers)

        if response.status_code == 200:
            results = json.loads(response.text)
            self.display_animated_results(results, "train")
            self.enable_UI_elements(True)


    def erase_canvas(self):
        self.canvas.reset()

    def submit_clicked(self):
        """ extracts data from the canvas and sends appropriate information to the BE """
        mode = self.mode
        label = sanitize_input(self.label_input.text()) if mode == "train" else None
        content_type, headers, path = get_request_resources(mode, label)

        ok_to_send_img = (mode == 'train' and label != None) or mode == 'test'

        if ok_to_send_img:
            self.enable_UI_elements(False)

            pixmap = self.canvas.pixmap()
            img_array = get_image_array(pixmap)
            _, img_encoded = cv2.imencode('.jpg', img_array)
            data = img_encoded.tostring()

            response = requests.post(path, data=data, headers=headers)

            if response.status_code == 200 and mode == "test":
                results = json.loads(response.text)
                self.display_animated_results(results, mode)
            else:
                self.canvas.reset()

            self.enable_UI_elements(True)

        else:
            showErrorMsg("Please label your data with single digits (0-9)!")


    def train_selected(self):
        self.mode = "train"

        self.label_input.setVisible(True)
        self.fit_button.setVisible(True)

    def test_selected(self):
        self.mode = "test"

        self.label_input.setVisible(False)
        self.fit_button.setVisible(False)

    def enable_UI_elements(self, val) -> None:
        self.erase_button.setEnabled(val)
        self.fit_button.setEnabled(val)
        self.submit_button.setEnabled(val)
        self.label_input.setEnabled(val)
        self.canvas.setEnabled(val)

    def display_animated_results(self, results_dict, mode) -> None:
        highest_score = None if mode == 'train' else max(results_dict, key=results_dict.get)
        for i in range(10):
            self.score_labels[i].setStyleSheet("QLabel {color: " + self.letterColor + "};")
            digit = str(i)
            isHighest = digit == highest_score
            val = float(results_dict[digit]['f1-score']) if mode == "train" else float(results_dict[str(i)])
            multiplier = 15.0 if mode == "train" else 25.0
            qty_bars = int(val*multiplier)
            bars = str(i) + "   " +  "|" * qty_bars
            self.score_labels[i].setText(bars)
            if isHighest and mode != "train": self.score_labels[i].setStyleSheet("QLabel {color: green};")




def showErrorMsg(text):
    """ displays simple error window with custom text """
    error_window = QMessageBox()
    error_window.setIcon(QMessageBox.Critical)
    error_window.setText(text)
    error_window.setWindowTitle("Error")
    error_window.exec_()


def sanitize_input(text) -> str:
    """ removes whitespaces and checks whether the input is one and only one digit """
    label = text.strip() if text != None else None
    return label if label != None and label != "" and len(label) == 1 and label.isdigit() else None
    


def get_image_array(q_pixmap) -> list:
    """ extracts the pixel values from the QPixmap format and returns a numpy array """
    q_image = QPixmap.toImage(q_pixmap)
    width = q_image.width()
    height = q_image.height()
    depth = q_image.depth()
    return QImage_2_List(q_image, width, height, depth)


def get_request_resources(mode, label=None) -> (str, dict, str):
    content_type = 'image/jpeg'
    headers = {'content-type': content_type}
    path = "/".join([config.host_url, mode])
    if label != None: path = "/".join([path, label]) # append the label if needed
    
    return content_type, headers, path


def QImage_2_List(img, width, height, depth) -> list:
    """ converts QImage into a numpy array """
    img = img.convertToFormat(4)

    ptr = img.bits()
    ptr.setsize(img.byteCount())

    return np.array(ptr).reshape(height, width, depth//8)

