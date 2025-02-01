import cv2
import numpy as np

# Verifica se o módulo ArUco está disponível
if not hasattr(cv2.aruco, 'drawMarker'):
    print("Erro: Seu OpenCV pode estar sem suporte ao ArUco. Atualize para a versão mais recente!")

# Criar um dicionário ArUco
aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
marker_size = 400  

# Gerar o marcador ArUco
marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)
cv2.aruco.generateImageMarker(aruco_dict, 1, marker_size, marker_image)

# Salvar a imagem do marcador
cv2.imwrite("marker_aruco.png", marker_image)

print(" Marcador gerado! Verifique o arquivo 'marker_aruco.png'.")
