from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QSizePolicy
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt
import cv2
from components.bigbuttons import ImageNavButton
import utilities
from utilities.image_processing import get_contours_sir


class ImportImageWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Variables

        self.image = r'icons\noimage.png'

        # UI ELEMENTS

        ## Image Viewer Label

        self.image_viewer_label = QLabel("IMAGE CONTOUR INFORMATION")
        self.image_viewer_label.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        ## Image Viewer
        self.image_holder = QLabel()
        self.image_holder.setPixmap(QPixmap(self.image))
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
         self.parentWidget().setCurrentWidget(self.parentWidget().import_image_widget)
         image_orig , image , contours = get_contours_sir(imgdir)
         cv2.imshow("Drawn", image)

    
    def set_image(self, imagedir):
        self.image = imagedir
        scaled_pixmap = QPixmap(imagedir).scaled(
                    self.image_holder.width(), 
                    self.image_holder.height(), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
        self.image_holder.setPixmap(scaled_pixmap)
    
    def get_cv2_image(self):
        if self.image is not None:
            return cv2.imread(self.image)
        else:
            return None
    
    def resizeEvent(self, a0):
        self.update()
        scaled_pixmap = QPixmap(self.image).scaled(
                    self.image_holder.width(), 
                    self.image_holder.height(), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
        self.image_holder.setPixmap(scaled_pixmap)
        return super().resizeEvent(a0)
    
    def on_home_navigation_pressed(self):
        print("Import Image Widget : Returning to Landing Page")
        self.parentWidget().setCurrentWidget(self.parentWidget().landingwidget)
        

    def on_continue_navigation_pressed(self):
         print("Import Image Widget : Proceeding to Edit Image Page")
         

