from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton , QSizePolicy , QScrollArea , QFileDialog, QMessageBox, QApplication
import sys
from PyQt6.QtGui import QIcon , QImage , QPixmap
from PyQt6.QtCore import Qt , QSize , QTimer , pyqtSignal, Qt, QThread 
import cv2
import numpy as np

class ImportImageWidget(QWidget):
    def __init__(self):
        super().__init__()

        # Variables

        self.image = None

        # UI ELEMENTS

        # LAYOUTS

        # Main Layout
        self.mainlayout = QVBoxLayout()

        # SIGNALS

        # OTHERS

        self.setLayout(self.mainlayout)
    
    def set_image(self, imagedir):
        self.image = imagedir
    
    def get_cv2_image(self):
        if self.image is not None:
            return cv2.imread(self.image)
        else:
            return None
        
app = QApplication(sys.argv)
window = ImportImageWidget()
window.show()
sys.exit(app.exec())

