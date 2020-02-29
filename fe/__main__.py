
import sys
from PyQt5.QtWidgets import QWidget, QMainWindow, QLabel, QApplication
from PyQt5.QtGui import QPainter, QColor, QPen, QPixmap
from PyQt5.QtCore import Qt

# https://app.getpocket.com/read/928938439
class MainWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.setGeometry(500, 300, 1000, 600)
        self.setWindowTitle('OCR Application -- by Sergey Platonov')
        self.show()
        
        self.label = QLabel
        canvas = QPixmap(500, 500)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        self.draw()


    def draw(self):
        painter = QPainter(self.label.pixmap())
        painter.drawLine(10, 10, 300, 200)
        painter.end()
        


if __name__ == "__main__":
    app = QApplication(sys.argv)
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())