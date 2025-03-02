from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget , QLabel, QScrollArea
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize, Qt
from utils import resource_path, cv2_to_QImage
import cv2



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
    def __init__(self , cv_img, btn_action ):
        super().__init__()
        self.setFixedSize(50,76)

        self.cv_image = cv_img

        self.cv_img_orig = cv_img

        self.q_image = cv2_to_QImage(self.cv_image)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imglabel = QLabel()
        self.imglabel.setStyleSheet("background-color: black;border-radius: 10px;")
        self.imglabel.setFixedSize(self.size())
        self.imglabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap.fromImage(self.q_image)
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.imglabel.setPixmap(pixmap)

        self.button = QPushButton(self)
        self.button.setStyleSheet("background-color: black; border-radius: 10px;")
        self.button.clicked.connect(lambda: self.on_click(btn_action))
        self.button.setFixedSize(self.imglabel.size())


        button_layout = QVBoxLayout(self.button)
        button_layout.addWidget(self.imglabel)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        button_layout.setSpacing(0)  # Remove spacing
        
        layout.addWidget(self.button)
    
    def on_click(self, btn):
        btn(self)

    def apply_filter(self, filter):
        match filter:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case _:
                pass
    
    def apply_imgActn(self , type):
        match type:
            case 1:
                pass
            case 2:
                pass
            case 3:
                pass
            case 4:
                pass
            case _:
                pass

    def update_image(self , newImg):
        pass

        
class ActionsBtn(QWidget):
    def __init__(self, action_name):
        super().__init__()
        self.setFixedSize(80, 80)
        self.setStyleSheet("background-color: gray;")

        layout = QVBoxLayout(self)

        # Create a button
        self.btn = QPushButton(action_name, self)  # Set text on button
        self.btn.setFixedSize(self.size())

        # Add the button to the layout
        layout.addWidget(self.btn)

        # Connect button click to an action
        self.btn.clicked.connect(self.action)

    def action(self):
        print("Action triggered")





