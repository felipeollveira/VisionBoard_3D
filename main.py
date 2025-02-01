import sys
from cam.camera_feed import CameraFeed
from PyQt5.QtWidgets import QApplication



# Main
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraFeed()
    window.show()
    sys.exit(app.exec_())
