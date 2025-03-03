from PyQt6.QtWidgets import QPushButton, QVBoxLayout, QWidget , QLabel, QScrollArea, QHBoxLayout, QSizePolicy
from PyQt6.QtGui import QIcon, QPixmap , QImage
from PyQt6.QtCore import QSize, Qt, pyqtSignal
from utils import resource_path, cv2_to_QImage
import cv2



def create_big_button(label, icon , action):
    button = QPushButton()
    button.setIcon(QIcon(icon))
    button.setText(label)
    button.setIconSize(QSize(30,30))
    button.clicked.connect(action)
    button.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

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

prev_click = None

class ImageBtn(QWidget):
    on_image_changed = pyqtSignal()
    on_self_delete = pyqtSignal()
    def __init__(self , cv_img, btn_action ):
        super().__init__()
        self.setFixedSize(50,76)
        self.cv_image = cv_img

        self.cv_img_orig = cv_img.copy()

        self.q_image = cv2_to_QImage(self.cv_image)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.imglabel = QLabel()
        self.imglabel.setStyleSheet("background-color: black;border-radius: 0px;")
        self.imglabel.setFixedSize(self.size())
        self.imglabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        pixmap = QPixmap.fromImage(self.q_image)
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)

        self.imglabel.setPixmap(pixmap)

        self.button = QPushButton(self)
        self.button.setStyleSheet("background-color: black; border-radius: 0px;")
        self.button.clicked.connect(lambda: self.on_click(btn_action))
        self.button.setFixedSize(self.imglabel.size())


        button_layout = QVBoxLayout(self.button)
        button_layout.addWidget(self.imglabel)
        button_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        button_layout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        button_layout.setSpacing(0)  # Remove spacing
        
        layout.addWidget(self.button)
    
    def on_click(self, btn):
        global prev_click  # Access global variable
        
        if prev_click and prev_click != self and not prev_click.isHidden():  
            prev_click.setStyleSheet("border: none;")  # Remove border safely

        self.setStyleSheet("border: 3px solid white;")  # Apply border to new selection
        prev_click = self  # Update previous selection

        btn(self)  # Execute the action


    def apply_filter(self, filter):
        to_delete = False
        match filter:
            case "Gray":
                self.cv_image = cv2.cvtColor(self.cv_img_orig , cv2.COLOR_RGB2GRAY)
            case "Orig":
                self.cv_image = self.cv_img_orig
            case "B&W":
                self.cv_image = self.cv_img_orig[:,:,2]
                _, self.cv_image = cv2.threshold(self.cv_image, 100, 255, cv2.THRESH_BINARY)
            case "Nega":
                blur = cv2.bilateralFilter(self.cv_img_orig, 9, 75, 75)
                gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)
                _,self.cv_image = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY_INV)
            case "Otsu":
                gray = cv2.cvtColor(self.cv_img_orig, cv2.COLOR_RGB2GRAY)
                blur = cv2.GaussianBlur(gray , (5,5), 0)
                _, self.cv_image = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            case "AMT":
                gray = cv2.cvtColor(self.cv_img_orig, cv2.COLOR_RGB2GRAY)
                self.cv_image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 3, 5)
            case "Rotate-CCW":
                self.cv_img_orig = cv2.rotate(self.cv_img_orig, cv2.ROTATE_90_COUNTERCLOCKWISE)
                self.cv_image = cv2.rotate(self.cv_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            case "Rotate": # from Rotate-CW
                self.cv_img_orig = cv2.rotate(self.cv_img_orig, cv2.ROTATE_90_CLOCKWISE)
                self.cv_image = cv2.rotate(self.cv_image, cv2.ROTATE_90_CLOCKWISE)
            case "Delete":
                to_delete = True
                self.deleteSelf()
            case _:
                print("Filter Does Not Exist")

        self.q_image = cv2_to_QImage(self.cv_image)
        pixmap = QPixmap.fromImage(self.q_image)
        pixmap = pixmap.scaled(self.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.imglabel.setPixmap(pixmap)
        if not to_delete:
            self.on_image_changed.emit()

    def deleteSelf(self):
        global prev_click  # Ensure it doesn't reference a deleted widget

        if prev_click == self:
            prev_click = None  # Reset to avoid crashes

        self.on_self_delete.emit()
        self.deleteLater()
        self.hide()

        if self.parentWidget():
            self.parentWidget().removed_item()  # Ensure parent exists before calling


class ActionsBtn(QWidget):
    def __init__(self, action_name):
        super().__init__()
        self.action_name = action_name
        self.selected = None
        self.setFixedSize(100, 50)
        layout = QHBoxLayout(self)
        self.btn = QPushButton(action_name, self)  # Set text on button
        self.btn.setFixedSize(self.size())
        layout.addWidget(self.btn)
        self.btn.clicked.connect(self.action)

    def action(self):
        if self.selected:
            self.selected.apply_filter(self.action_name)

    def set_selected(self , selected):
        self.selected = selected

    def disable_btn(self, is_disabled):
        self.btn.setDisabled(is_disabled)





