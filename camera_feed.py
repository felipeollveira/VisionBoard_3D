import mss
import numpy as np
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtCore import Qt, QTimer


class CameraFeed(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Camera Feed")
        self.setGeometry(50, 50, 640, 480)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
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
            self.timer.timeout.connect(self.update_frame)
            self.timer.start(30)

        # Inicializa o mss para capturar a tela do Windows
        self.sct = mss.mss()
        self.show()

    def detect_aruco_markers(self, frame):
        """Detecta os marcadores ArUco no frame."""
        try:
            aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            aruco_params = cv2.aruco.DetectorParameters()

            # Converter a imagem para escala de cinza
            gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

            # Detectar os marcadores ArUco
            corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

            if ids is not None:
                frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

            return corners, ids
        except Exception as e:
            print(f"Erro na detecção de ArUco: {e}")
            return [], None

    def capture_screen(self):
        """Captura a tela do Windows."""
        monitor = self.sct.monitors[1]  # Usando o primeiro monitor
        screenshot = self.sct.grab(monitor)

        # Converte a captura de tela para uma imagem OpenCV
        img = np.array(screenshot)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        return img

    def update_frame(self):
        try:
            ret, frame = self.capture.read()
            if not ret:
                self.label.setText("Falha ao capturar frame da câmera!")
                return

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detecta os marcadores ArUco
            corners, ids = self.detect_aruco_markers(frame)
            if ids is not None:
                for i, corner in enumerate(corners):
                    # Determina a posição e tamanho do marcador
                    x, y, w, h = cv2.boundingRect(corner)

                    # Desenha um retângulo em torno do marcador
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                    # Captura a tela do Windows
                    screen_img = self.capture_screen()

                    # Define o fator de escala para aumentar a tela
                    scale_factor_w = 7  # 7x mais largo
                    scale_factor_h = 5  # 5x mais alto
                    new_w = w * scale_factor_w
                    new_h = h * scale_factor_h

                    # Redimensiona a captura de tela para ser maior que o marcador
                    screen_resized = cv2.resize(screen_img, (new_w, new_h))

                    # Ajusta a posição para centralizar melhor
                    x = max(0, x - (new_w - w) // 2)
                    y = max(0, y - (new_h - h) // 2)

                    # Evita ultrapassar os limites do frame da câmera
                    frame_h, frame_w, _ = frame.shape
                    new_w = min(new_w, frame_w - x)
                    new_h = min(new_h, frame_h - y)
                    screen_resized = cv2.resize(screen_img, (new_w, new_h))

                    # Sobrepõe a captura de tela do Windows na área do marcador
                    frame[y:y + new_h, x:x + new_w] = screen_resized

            # Converte o frame para o formato correto para exibição na tela
            height, width, _ = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(q_image))

        except Exception as e:
            print(f"Erro na atualização do frame: {e}")
