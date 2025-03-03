# import cv2
# import numpy as np


# def preprocess_image(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5,5), 0)
#     thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11 , 2)

#     return thresh

# def get_edges(thresh):
#     edges = cv2.Canny(thresh, 50 ,150)
#     return edges

# def find_contour(edges):
#     cnt, _ = cv2.findContours(edges , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     cnt = sorted(cnt, key=cv2.contourArea, reverse=True)

#     for c in cnt:
#         epsilon = 0.02 * cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, epsilon, True)

#         if len(approx) == 4:
#             return approx
#     return None


# def warp(image , contour):
#     pts = np.array(contour, dtype="float32")
#     rect = np.array(sorted(pts, key=lambda x: x[0][0] + x[0][1]))
#     (tl,tr,br,bl) = rect[:,0]

#     w = max(np.linalg.norm(br-bl), np.linalg.norm(tr-tl))
#     h = max(np.linalg.norm(tr-br), np.linalg.norm(tl-bl))

#     dst = np.array([[0,0], [w-1,0], [w-1, h-1], [0, h-1]], dtype="float32")

#     M =  cv2.getPerspectiveTransform(pts, dst)

#     warp = cv2.warpPerspective(image, M , (int(w), int(h)))

#     return warp

# image = cv2.imread(r"C:\Users\Joshua Libando\Dropbox\PC\Documents\IMG20240314170018.jpg")

# t = preprocess_image(image)

# e = get_edges(t)

# c = find_contour(e)

# cv2.drawContours(image, [c], -1, (0, 255, 0), 3)

# cv2.imshow("" , image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton , QSizePolicy , QScrollArea , QFileDialog, QMessageBox, QApplication
import sys
from PyQt6.QtGui import QIcon , QImage , QPixmap
from PyQt6.QtCore import Qt , QSize , QTimer , pyqtSignal, Qt, QThread 
import cv2
import numpy as np
from components.bigbuttons import ImageNavButton

import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget , QPushButton
from PyQt6.QtGui import QFontDatabase , QFont, QIcon
import stackwidgets.LandingWidget
from stackwidgets.Widgets import LandingWidget , CaptureWidget, EditImageWidget
import treads.Watchers
from utils import resource_path, save_path
import treads
import stackwidgets



class ImportImageWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Variables

        self.image = r'icons\noimage.png'

        # UI ELEMENTS

        ## Image Viewer Label

        self.image_viewer_label = QLabel("Image Contour Information")
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
         self.parentWidget().setCurrentWidget(self.parentWidget().import_image_widget())
    
    def set_image(self, imagedir):
        self.image = imagedir
        self.image_holder.setPixmap(QPixmap(self.image))
    
    def get_cv2_image(self):
        if self.image is not None:
            return cv2.imread(self.image)
        else:
            return None
    
    def resizeEvent(self, a0):
        self.update()
        return super().resizeEvent(a0)
    
    def on_home_navigation_pressed(self):
        print("Import Image Widget : Returning to Landing Page")
        

    def on_continue_navigation_pressed(self):
         print("Import Image Widget : Proceeding to Edit Image Page")
         
        
app = QApplication(sys.argv)

font_id = QFontDatabase.addApplicationFont(resource_path("fonts/Jura-VariableFont_wght.ttf"))

if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family, 12)) 

window = ImportImageWidget()


window.show()
sys.exit(app.exec())

