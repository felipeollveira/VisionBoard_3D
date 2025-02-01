
import numpy as np
from PyQt5.QtWidgets import QWidget
from PyQt5.QtCore import Qt


class MonitorVirtual(QWidget):
    def __init__(self, width=640, height=360):
        super().__init__()
        self.setWindowTitle("Monitor Virtual")
        self.setGeometry(0, 0, width, height)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setStyleSheet("background-color: black;")
        self.width, self.height = width, height
        self.show()
