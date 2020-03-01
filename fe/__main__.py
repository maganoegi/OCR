
import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QSlider, QFileDialog
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap, QImage, QFont
from PyQt5.QtCore import Qt, QSize

# https://app.getpocket.com/read/928938439

class Canvas(QLabel):
    def __init__(self):
        super().__init__()
        pixmap = QPixmap(500, 500)
        self.setPixmap(pixmap)
        self.penWidth = 5
        
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
        p.setColor(QColor("#000"))
        # painter.drawRect(600, 0, 1000, 600)
        # painter.fillRect(QColor=QColor('#ffffff'))
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
    
    def changePenWidth(self, width):
        self.penWidth = width

    def reset(self):
        self.pixmap().fill(QColor(Qt.white))
        self.update()

    def save_image(self):
        pixmap = self.pixmap()
        pixmap.save("Test.png", "PNG")

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("OCR")
        self.canvas = Canvas()
        self.slider = QSlider(Qt.Horizontal)
        self.submitBtn = self.add_btn("Submit")
        self.resetBtn = self.add_btn("Erase")
        self.labels = [self.add_lbl(str(i)) for i in range(10)]
        self.lbl_result = self.add_lbl("Result Test")

        w = QWidget()
        l = QVBoxLayout()
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
        l.addWidget(self.slider)
        lhv.addWidget(self.submitBtn)
        lhv.addWidget(self.resetBtn)
        for i in range(10):
            lhvv.addWidget(self.labels[i])
        lhh.addWidget(self.lbl_result)


        l.addLayout(l_container)

        palette = QHBoxLayout()

        l.addLayout(palette)
        self.setStyleSheet("background-color: #123456;")  

        self.setCentralWidget(w)

        self.submitBtn.clicked.connect(self.canvas.save_image)
        self.resetBtn.clicked.connect(self.canvas.reset)
        
        self.slider.setMinimum(5)
        self.slider.setMaximum(35)
        self.slider.valueChanged.connect(self.updateThicknessVal)
    
        for index, label in enumerate(self.labels):
            self.write_lbl_val(label, float(index + 1), index) 
        
        self.print_result_lbl(9, asPredicted=False)


    def updateThicknessVal(self):
        val = self.slider.value()
        self.canvas.changePenWidth(val)

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









# class MainWindow(QMainWindow):
    
#     def __init__(self):
#         super().__init__()

#         self.setGeometry(500, 300, 1000, 600)
#         self.setWindowTitle('OCR Application -- by Sergey Platonov')
#         self.show()
        
#         self.label = QLabel
#         canvas = QPixmap(500, 500)
#         self.label.setPixmap(canvas)
#         self.setCentralWidget(self.label)
#         self.draw()


#     def draw(self):
#         painter = QPainter(self.label.pixmap())
#         painter.drawLine(10, 10, 300, 200)
#         painter.end()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())