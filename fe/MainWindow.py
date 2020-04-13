

import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSlider, QFileDialog, QRadioButton, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QSize
from Canvas import Canvas
import config

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR")
        self.canvas = Canvas()

        self.submitBtn = self.add_btn("Submit")
        self.resetBtn = self.add_btn("Erase")
        
        self.labels = [self.add_lbl(str(i)) for i in range(10)]
        self.lbl_result = self.add_lbl("Result Test")

        self.current_label_txtBox = QLineEdit()
        self.current_label_txtBox.resize(30, 20)

        self.trainRadioBtn = QRadioButton("Train")
        self.trainRadioBtn.setChecked(True)
        self.trainRadioBtn.mode = "train"
        self.trainRadioBtn.toggled.connect(self.modeSelect)

        self.testRadioBtn = QRadioButton("Test")
        self.testRadioBtn.mode = "test"
        self.testRadioBtn.toggled.connect(self.modeSelect)

        w = QWidget()
        l = QVBoxLayout()
        l_grid = QGridLayout()
        l_container = QHBoxLayout()
        lhv = QVBoxLayout()
        lhvv = QVBoxLayout()
        lhh = QHBoxLayout()
        lhh = QVBoxLayout()

        l_container.addLayout(lhv)
        l_container.addLayout(lhvv)
        l_container.addLayout(lhh)

        w.setLayout(l)
        l.addWidget(self.canvas)
        lhv.addWidget(self.current_label_txtBox)
        lhv.addWidget(self.submitBtn)
        lhv.addWidget(self.resetBtn)
        for i in range(10):
            lhvv.addWidget(self.labels[i])
        lhh.addWidget(self.lbl_result)

        l_grid.addWidget(self.trainRadioBtn, 0, 0)
        l_grid.addWidget(self.testRadioBtn, 0, 1)

        l.addLayout(l_grid)
        l.addLayout(l_container)

        palette = QHBoxLayout()

        l.addLayout(palette)
        self.setStyleSheet("background-color: #123456;")  

        self.setCentralWidget(w)

        self.submitBtn.clicked.connect(self.canvas.post_data)
        self.resetBtn.clicked.connect(self.canvas.reset)
        
        for index, label in enumerate(self.labels):
            self.write_lbl_val(label, float(index + 1), index) 
        
        self.print_result_lbl(9, asPredicted=False)
    
    def modeSelect(self):
        radioButton = self.sender()
        if radioButton.isChecked():
            config.mode = radioButton.mode
            print(config.mode)


    def add_lbl(self, text):
        lbl = QLabel()
        lbl.setText(text)
        return lbl

    def add_btn(self, text):
        btn = QPushButton()
        btn.setText(text) 
        return btn

    def write_lbl_val(self, label, val, index):
        spaces = lambda x: " " * x
        rounded_2_half = round(val * 2) / 2
        increments = int(rounded_2_half / 0.5)
        label.setText(spaces(6) + str(index) + spaces(2) + ("|" * int(increments)))

    def print_result_lbl(self, val, asPredicted):
        red = 255 if asPredicted else 0
        green = 0 if asPredicted else 255
        self.lbl_result.setStyleSheet(f"color: rgb({red}, {green}, 0);")
        self.lbl_result.setText(str(val))
        self.lbl_result.setFont(QFont("Arial", 70, QFont.Bold))




