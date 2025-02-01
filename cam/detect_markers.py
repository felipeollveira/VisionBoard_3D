import cv2

def detect_aruco_markers(frame):
    """Detecta os marcadores ArUco no frame."""
    try:
        aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
        aruco_params = cv2.aruco.DetectorParameters()

        # Converte a imagem para escala de cinza
        gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)

        # Detecta os marcadores ArUco no frame
        corners, ids, _ = cv2.aruco.detectMarkers(gray, aruco_dict, parameters=aruco_params)

        # Se houver marcadores, desenha as bordas
        if ids is not None:
            frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)

        return corners, ids
    except Exception as e:
        print(f"Erro na detecção de ArUco: {e}")
        return [], None
