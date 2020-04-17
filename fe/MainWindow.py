

import sys
from PyQt5.QtWidgets import QWidget, QGroupBox, QMainWindow, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSlider, QFileDialog, QRadioButton, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QSize
from Canvas import Canvas
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
        letterColor = "cornflowerblue"
        fontSize = 20
        font = "Roboto"
        fontWeight = QFont.Bold

        self.canvas = Canvas()

        self.fit_button = QPushButton(self)
        self.fit_button.setText("fit") 
        self.fit_button.clicked.connect(self.fit_clicked)
        self.fit_button.setFixedSize(QSize(elementWidth, elementHeight))
        self.fit_button.setStyleSheet("QPushButton {color: " + letterColor + "};")
        self.fit_button.setFont(QFont(font, fontSize, fontWeight))

        self.erase_button = QPushButton(self)
        self.erase_button.setText("erase") 
        self.erase_button.clicked.connect(self.erase_canvas)
        self.erase_button.setFixedSize(QSize(elementWidth, elementHeight))
        self.erase_button.setStyleSheet("QPushButton {color: " + letterColor + "};")
        self.erase_button.setFont(QFont(font, fontSize, fontWeight))

        self.submit_button = QPushButton(self)
        self.submit_button.setText("submit") 
        self.submit_button.clicked.connect(self.submit_clicked)
        self.submit_button.setFixedSize(QSize(elementWidth, elementHeight))
        self.submit_button.setStyleSheet("QPushButton {color: " + letterColor + "};")
        self.submit_button.setFont(QFont(font, fontSize, fontWeight))

        self.label_input = QLineEdit(self)
        self.label_input.setFont(QFont(font, fontSize, fontWeight))
        self.label_input.setStyleSheet("QLineEdit {color: " + letterColor + "};")
        self.label_input.setFont(QFont(font, fontSize, fontWeight))
        self.label_input.setFixedSize(QSize(elementWidth, elementHeight))

        self.score_labels = []
        for i in range(10):
            label = QLabel(self)
            label.setText(str(i))
            label.setStyleSheet("QLabel {color: " + letterColor + "};")
            label.setFont(QFont(font, fontSize, fontWeight))
            self.score_labels.append(label)

        self.train_Rbutton = QRadioButton(self)
        self.train_Rbutton.setText("training")
        self.train_Rbutton.setChecked(True)
        self.train_Rbutton.toggled.connect(self.train_selected)
        self.train_Rbutton.setStyleSheet("QRadioButton {color: " + letterColor + "};")
        self.train_Rbutton.setFont(QFont(font, 15, fontWeight))

        self.test_Rbutton = QRadioButton(self)
        self.test_Rbutton.setText("testing")
        self.test_Rbutton.toggled.connect(self.test_selected)
        self.test_Rbutton.setStyleSheet("QRadioButton {color: " + letterColor + "};")
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
        mode = self.mode
        content_type, headers, path = get_request_resources(mode)
        data = ""
        response = requests.post(path, data=data, headers=headers)

        if response.status_code == 200:
            print(json.loads(response.text))

    def erase_canvas(self):
        self.canvas.reset()

    def submit_clicked(self):
        """ extracts data from the canvas and sends appropriate information to the BE """
        mode = self.mode
        label = sanitize_input(self.label_input.text())
        content_type, headers, path = get_request_resources(mode, label)

        ok_to_send_img = (mode == 'train' and label != None) or mode == 'test'

        if ok_to_send_img:
            pixmap = self.canvas.pixmap()
            img_array = get_image_array(pixmap)
            _, img_encoded = cv2.imencode('.jpg', img_array)
            data = img_encoded.tostring()

            response = requests.post(path, data=data, headers=headers)

            if response.status_code == 200:
                self.erase_canvas()
                print(json.loads(response.text))
        else:
            pass
            # missing label input error


    def train_selected(self):
        self.mode = "train"

        self.label_input.setEnabled(True)
        self.fit_button.setEnabled(True)

    def test_selected(self):
        self.mode = "test"

        self.label_input.setEnabled(False)
        self.fit_button.setEnabled(False)



def sanitize_input(text) -> str:
    """ removes whitespaces and checks whether the input is one and only one digit """
    label = text.strip() if text != None else None
    return label if label != None and label != "" and len(label) == 1 and label.isdigit() else None
    


def get_image_array(q_pixmap) -> list:
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


def QImage_2_List(img, width, height, depth):
    img = img.convertToFormat(4)

    ptr = img.bits()
    ptr.setsize(img.byteCount())

    return np.array(ptr).reshape(height, width, depth//8)








# def post_img(mode, label=None):

#     content_type = 'image/jpeg'
#     headers = {'content-type': content_type}
#     path = "/".join([config.host_url, mode, label])

#     _, img_encoded = cv2.imencode('.jpg', img_array)
#     data = img_encoded.tostring()
#     response = requests.post(path, data=data, headers=headers)
    
#     print(json.loads(response.text))


    # def post_train_data(self):
    # text= "   9   "
    # if text != None:
    #     label = text.strip()

    #     if label == "":
    #         pass
    #     else:
    #         pixmap = self.pixmap()
    #         mode = "train"
    #         json_data = post_pixmap(pixmap, mode, label)











    # def __init__(self):

    #     w = QWidget()
    #     l = QVBoxLayout()
    #     l_grid = QGridLayout()
    #     l_container = QHBoxLayout()
    #     lhv = QVBoxLayout()
    #     lhvv = QVBoxLayout()
    #     lhh = QHBoxLayout()
    #     lhh = QVBoxLayout()

    #     l_container.addLayout(lhv)
    #     l_container.addLayout(lhvv)
    #     l_container.addLayout(lhh)

    #     w.setLayout(l)
    #     l.addWidget(self.canvas)
    #     lhv.addWidget(self.current_label_txtBox)
    #     lhv.addWidget(self.submitBtn)
    #     lhv.addWidget(self.resetBtn)
    #     for i in range(10):
    #         lhvv.addWidget(self.labels[i])
    #     lhh.addWidget(self.lbl_result)

    #     l_grid.addWidget(self.trainRadioBtn, 0, 0)
    #     l_grid.addWidget(self.testRadioBtn, 0, 1)

    #     l.addLayout(l_grid)
    #     l.addLayout(l_container)

    #     palette = QHBoxLayout()

    #     l.addLayout(palette)
    #     self.setStyleSheet("background-color: #123456;")  

    #     self.setCentralWidget(w)

    #     self.submitBtn.clicked.connect(self.canvas.post_data)
    #     self.resetBtn.clicked.connect(self.canvas.reset)
        
    #     for index, label in enumerate(self.labels):
    #         self.write_lbl_val(label, float(index + 1), index) 
        
    #     self.print_result_lbl(9, asPredicted=False)
    
    # def modeSelect(self):
    #     radioButton = self.sender()
    #     if radioButton.isChecked():
    #         self.mode = radioButton.mode
    #         print(self.mode)


    # def add_lbl(self, text):
    #     lbl = QLabel()
    #     lbl.setText(text)
    #     return lbl

    # def add_btn(self, text):
    #     btn = QPushButton()
    #     btn.setText(text) 
    #     return btn

    # def write_lbl_val(self, label, val, index):
    #     spaces = lambda x: " " * x
    #     rounded_2_half = round(val * 2) / 2
    #     increments = int(rounded_2_half / 0.5)
    #     label.setText(spaces(6) + str(index) + spaces(2) + ("|" * int(increments)))

    # def print_result_lbl(self, val, asPredicted):
    #     red = 255 if asPredicted else 0
    #     green = 0 if asPredicted else 255
    #     self.lbl_result.setStyleSheet(f"color: rgb({red}, {green}, 0);")
    #     self.lbl_result.setText(str(val))
    #     self.lbl_result.setFont(QFont("Arial", 70, QFont.Bold))




