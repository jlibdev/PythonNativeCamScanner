from PyQt6.QtWidgets import QDialog , QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon
from utils import resource_path

class ExportPopUp(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Export")
        self.setWindowIcon(QIcon(resource_path(r'icons\export.png')))
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        label = QLabel("This is a custom popup!", self)
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept) 

        layout.addWidget(label)
        layout.addWidget(close_button)

        