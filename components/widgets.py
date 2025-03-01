from PyQt6.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

class ImageWidget(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)

        self.img_label = QLabel("No Image")  # Default text when no image
        self.img_label.setFixedSize(150, 150)
        self.img_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.img_label.setStyleSheet("background-color: gray; border-radius: 10px; font-size: 14px; color: white;")

        # Buttons to add and remove pixmap
        self.add_btn = QPushButton("Add Image")
        self.add_btn.clicked.connect(self.add_pixmap)

        self.remove_btn = QPushButton("Remove Image")
        self.remove_btn.clicked.connect(self.remove_pixmap)

        layout.addWidget(self.img_label)
        layout.addWidget(self.add_btn)
        layout.addWidget(self.remove_btn)

        self.setLayout(layout)

    def add_pixmap(self):
        """ Set a pixmap and remove text """
        if not self.img_label.pixmap():  # If no image is set
            pixmap = QPixmap()
            self.img_label.setPixmap(pixmap)
            self.img_label.setText("")  # Remove text

    def remove_pixmap(self):
        """ Remove the pixmap and show text """
        self.img_label.clear()  # Clears the QLabel
        self.img_label.setText("No Image")  # Show text

# Run Application
app = QApplication([])

widget = ImageWidget()
widget.show()

app.exec()