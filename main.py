import sys
from monitor.monitor_virtual import MonitorVirtual
from camera_feed import CameraFeed
from PyQt5.QtWidgets import QApplication



if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication

    app = QApplication(sys.argv)
    camera = CameraFeed()
    sys.exit(app.exec_())
