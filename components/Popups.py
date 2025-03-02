from PyQt6.QtWidgets import QDialog , QVBoxLayout, QLabel, QPushButton

class ExportPopUp(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Custom Popup")
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        label = QLabel("This is a custom popup!", self)
        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept) 

        layout.addWidget(label)
        layout.addWidget(close_button)

        