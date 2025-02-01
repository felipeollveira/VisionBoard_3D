# update_frames.py

from PyQt5.QtGui import QImage, QPixmap
import cv2
import numpy as np
from .detect_markers import detect_aruco_markers

def update_frame(self):
    try:
        ret, frame = self.capture.read()
        if not ret:
            self.label.setText("Falha ao capturar frame da câmera!")
            return

        # Converte o frame da câmera de BGR para RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Chama a função detect_aruco_markers passando o frame capturado
        corners, ids = detect_aruco_markers(frame)

        # Se os marcadores foram detectados, continua com a lógica de sobreposição
        if ids is not None:
            for i, corner in enumerate(corners):
                x, y, w, h = cv2.boundingRect(corner)

                # Aqui você pode fazer a sobreposição de um conteúdo virtual na posição do marcador
                # Exemplo:
                # virtual_screen = self.generate_virtual_screen(w, h)
                # frame[y:y + h, x:x + w] = virtual_screen

        # Converte a imagem de volta para o formato adequado para exibição
        height, width, _ = frame.shape
        bytes_per_line = 3 * width
        q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(q_image))

    except Exception as e:
        print(f"Erro na atualização do frame: {e}")
