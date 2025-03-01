from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QPushButton, QFileDialog, QWidget
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import sys
import os
from components.bigbuttons import ImageBtn

class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.setGeometry(100, 100, 600, 400)

        # Layout
        layout = QVBoxLayout(self)

        # Button to select an image
        self.button = QPushButton("Open Image")
        self.button.clicked.connect(self.load_image)
        layout.addWidget(self.button)

        # Label to display the image
        self.image_label = QLabel("No image selected")
        self.image_label.setStyleSheet("background-color: black;")
        self.image_label.setFixedSize(180, 320)  # Fixed size for QLabel
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center align
        layout.addWidget(self.image_label)
        layout.addWidget(ImageBtn())

        # self.setLayout(layout)

    def load_image(self):
        file, _ = QFileDialog.getOpenFileName(
            self,
            "Select an Image",
            "",
            "Images (*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.webp)"
        )
        if file:
            pixmap = QPixmap()  # Load image into QPixmap

            # ✅ Resize image while keeping aspect ratio
            scaled_pixmap = pixmap.scaled(
                self.image_label.size(),  
                Qt.AspectRatioMode.KeepAspectRatio,  
                Qt.TransformationMode.SmoothTransformation  # Smooth scaling
            )

            self.image_label.setPixmap(scaled_pixmap)
            self.image_label.setText("")  # Remove text when image loads

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageViewer()
    window.show()
    sys.exit(app.exec())
