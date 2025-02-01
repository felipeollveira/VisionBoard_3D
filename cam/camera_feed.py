
import cv2
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer
from .update_frames import update_frame


class CameraFeed(QWidget):
    def __init__(self):
        super().__init__()

        # Configurar para mostrar a janela em tela cheia
        self.setWindowTitle("Camera Feed")
        self.showFullScreen()  # Torna a janela em tela cheia
        self.setWindowFlags(Qt.FramelessWindowHint)  # Remove as bordas da janela
        self.setStyleSheet("background-color: gray;")

        self.label = QLabel("Inicializando câmera...", self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)

        self.capture = cv2.VideoCapture(0)
        if not self.capture.isOpened():
            self.label.setText("Erro ao acessar a câmera!")
        else:
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_frame)  # Chama a função de atualização do frame
            self.timer.start(30)
    
    # Método para chamar a função update_frame do arquivo update_frames.py
    def update_frame(self):
        update_frame(self)
    
