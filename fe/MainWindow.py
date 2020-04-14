

import sys
from PyQt5.QtWidgets import QWidget, QGroupBox, QMainWindow, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton, QSlider, QFileDialog, QRadioButton, QLineEdit
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QSize
from Canvas import Canvas
import config

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

    def init_UIElements(self):

        elementWidth = 400
        elementHeight = 40
        letterColor = "cornflowerblue"
        fontSize = 20
        font = "Roboto"
        fontWeight = QFont.Bold


        self.fit_button = QPushButton(self)
        self.fit_button.setText("fit") 
        self.fit_button.clicked.connect(self.fit_clicked)
        self.fit_button.setFixedSize(QSize(elementWidth, elementHeight))
        self.fit_button.setStyleSheet("QPushButton {color: " + letterColor + "};")
        self.fit_button.setFont(QFont(font, fontSize, fontWeight))

        self.erase_button = QPushButton(self)
        self.erase_button.setText("erase") 
        self.erase_button.clicked.connect(self.erase_clicked)
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

        
        self.canvas = Canvas()

    def init_Layouts(self):
        self.w = QWidget()

        # Define containers
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


        # Add widgets to their respective grids and containers
        self.canvas_container.addWidget(self.canvas)
        self.radio_container.addWidget(self.train_Rbutton)
        self.radio_container.addWidget(self.test_Rbutton)

        self.button_container.addWidget(self.submit_button)
        self.button_container.addWidget(self.erase_button)
        self.button_container.addWidget(self.fit_button)
        self.button_container.addWidget(self.label_input)

        for i in range(10):
            self.label_container.addWidget(self.score_labels[i])


        # Combine grids and containers
        self.setCentralWidget(self.w)
        self.w.setLayout(self.main_container)

        self.main_container.addLayout(self.canvas_container)
        self.main_container.addLayout(self.radio_container)
        self.main_container.addLayout(self.button_label_container)

        self.button_label_container.addLayout(self.button_container)
        self.button_label_container.addLayout(self.label_container)

    def fit_clicked(self):
        pass

    def erase_clicked(self):
        pass

    def submit_clicked(self):
        pass

    def train_selected(self):
        pass

    def test_selected(self):
        pass


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
    #         config.mode = radioButton.mode
    #         print(config.mode)


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




