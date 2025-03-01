from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget , QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from utils import resource_path
import os



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
    def __init__(self,icon, action, direction = Qt.LayoutDirection.LeftToRight , text = "" , stylesheet = """
            QPushButton {
                border-radius: 25px;  
                border: none;
            }
            QPushButton:hover {background-color: #ACACAC}""" , iconsize = QSize(30, 30) , fixedsize = (50,50)):
        super().__init__()
        layout = QVBoxLayout(self)
        self.button = QPushButton(text)
        self.button.setIcon(QIcon(resource_path(icon)))
        self.button.setIconSize(iconsize)
        self.button.setFixedSize(fixedsize[0] , fixedsize[1])
        self.button.setStyleSheet(stylesheet)
        self.button.setLayoutDirection(direction)
        layout.addWidget(self.button)
        self.button.clicked.connect(action)

    def set_icon(self, icon):
        self.button.setIcon(QIcon(resource_path(icon)))

class ImageBtn(QWidget):
    def __init__(self , q_image):
        super().__init__()
        self.setFixedSize(180,320)
        # self.setStyleSheet("background-color: black")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.imglabel = QLabel()
        self.imglabel.setStyleSheet("background-color: black;border-radius: 10px;")
        self.imglabel.setFixedSize(self.size())
        self.imglabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.imglabel.setPixmap(pixmap)

        self.button = QPushButton(self)
        self.button.setStyleSheet("background-color: black; border-radius: 10px;")
        button_layout = QVBoxLayout(self.button)
        button_layout.addWidget(self.imglabel)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        button_layout.setSpacing(0)  # Remove spacing
        self.button.clicked.connect(self.on_click) 

        self.button.setFixedSize(self.imglabel.size())

        layout.addWidget(self.button)
    
    def on_click(self):
        print("Clicked")

