
import sys
import cv2
import threading
import numpy as np
from PyQt6.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import QTimer, Qt

class CameraApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Camera Toggle Example")
        self.setGeometry(100, 100, 640, 480)

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.toggle_button = QPushButton("Turn On Camera", self)
        self.toggle_button.clicked.connect(self.toggle_camera)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.toggle_button)
        self.setLayout(layout)

        self.capture = cv2.VideoCapture(0)  # Initialize camera
        self.running = False
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

    def toggle_camera(self):
        if self.running:
            self.running = False
            self.timer.stop()
            self.toggle_button.setText("Turn On Camera")
            self.image_label.clear()
        else:
            self.running = True
            self.timer.start(30)  # Adjust frame rate
            self.toggle_button.setText("Turn Off Camera")

    def update_frame(self):
        if self.running:
            ret, frame = self.capture.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = frame.shape
                bytes_per_line = ch * w
                q_image = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
                self.image_label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        self.capture.release()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CameraApp()
    window.show()
    sys.exit(app.exec())
