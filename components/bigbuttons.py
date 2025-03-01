from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import QSize
from utils import resource_path


def create_big_button(label, icon , action):
    button = QPushButton()
    button.setIcon(QIcon(icon))
    button.setText(label)
    button.setIconSize(QSize(30,30))
    button.clicked.connect(action)

    # Use margin instead of padding
    button.setStyleSheet("""
        QPushButton {
            padding: 50px;
        }
    """)

    return button

class ImageNavButton(QWidget):
    def __init__(self,icon, action):
        super().__init__()
        layout = QVBoxLayout(self)
        self.button = QPushButton(self)
        self.button.setIcon(QIcon(resource_path(icon)))
        self.button.setIconSize(QSize(30, 30))
        self.button.setFixedSize(50, 50)
        self.button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;  
                border: none;
            }
            QPushButton:hover {background-color: #ACACAC}
        """)

        layout.addWidget(self.button)
        self.button.clicked.connect(action)

    def set_icon(self, icon):
        self.button.setIcon(QIcon(resource_path(icon)))

class ImageButton(QWidget):
    def __init__(self, cv_label):
        super().__init__()
        self.setFixedSize(180, 320)

        layout = QVBoxLayout(self)

        # QLabel with OpenCV image
        self.label = cv_label
        self.label.setScaledContents(True)  # Ensure the image scales properly

        # QPushButton with QLabel inside
        self.button = QPushButton(self)
        button_layout = QVBoxLayout(self.button)
        button_layout.addWidget(self.label)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        button_layout.setSpacing(0)  # Remove spacing

        # Set button size to match the QLabel size
        self.button.setFixedSize(self.label.sizeHint())

        layout.addWidget(self.button)

        # Connect button click
        self.button.clicked.connect(self.on_click)

        

    def on_click(self):
        print("Button Clicked!")


