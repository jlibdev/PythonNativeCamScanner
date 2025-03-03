from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
from components.bigbuttons import ImageNavButton
from utilities.image_processing import get_contours
from utils import cv2_to_pixmap
from Main import CamScammerApp


class ImportImageWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent: CamScammerApp = parent

        # Variables

        self.imagedir = r'icons\noimage.png'
        self.orginal_image = None
        self.image = None
        self.contours = None

        # UI ELEMENTS

        ## Image Viewer Label

        self.image_viewer_label = QLabel("IMAGE CONTOUR INFORMATION")
        self.image_viewer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        ## Image Viewer
        self.image_holder = QLabel()
        self.image_holder.setPixmap(QPixmap(self.imagedir))
        self.image_holder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_holder.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_holder.setStyleSheet("background-color: black;") 
        self.image_holder.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        # LAYOUTS

        # Navigation Layout

        self.navigation_layout = QHBoxLayout()
        self.navigation_layout.addWidget(ImageNavButton(r"icons\house.png",self.on_home_navigation_pressed))
        self.navigation_layout.addStretch()
        self.navigation_layout.addWidget(ImageNavButton(r"icons\chev-r.png", self.on_continue_navigation_pressed , direction=Qt.LayoutDirection.RightToLeft , text = "CONTINUE", fixedsize=(150,50)))

        # Main Layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainlayout.addLayout(self.navigation_layout)
        self.mainlayout.addWidget(self.image_viewer_label)
        self.mainlayout.addWidget(self.image_holder)

        # SIGNALS

        # OTHERS

        self.setLayout(self.mainlayout)
        self.resize(1280, 720)
    
    def on_mount(self, imgdir):
        print("Import Image Widget Mounted")
        self.set_image(imgdir)
        self.parent.setCurrentWidget(self.parent.import_image_widget)
        print(len(self.contours))

    def set_image(self, imagedir):
        self.imagedir = imagedir
        self.orginal_image , self.image , self.contours = get_contours(imagedir)

        scaled_pixmap = QPixmap(cv2_to_pixmap(self.image)).scaled(
                    self.image_holder.width(), 
                    self.image_holder.height(), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
        self.image_holder.setPixmap(scaled_pixmap)
    
    def resizeEvent(self, a0):
        self.update()
        self.set_image(self.imagedir)
        return super().resizeEvent(a0)
    
    def on_home_navigation_pressed(self):
        print("Import Image Widget : Returning to Landing Page")
        self.parent.setCurrentWidget(self.parent.landingwidget)
        
    def on_continue_navigation_pressed(self):
          self.parent.edit_image_widget.update_image(self.contours, self.orginal_image)
          self.parent.setCurrentWidget(self.parent.edit_image_widget)
         

