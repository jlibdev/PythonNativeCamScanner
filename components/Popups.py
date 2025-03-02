from PyQt6.QtWidgets import QDialog , QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon
from utils import resource_path, export_to_pdf, export_to_img

class ExportPopUp(QDialog):
    def __init__(self, image_list):
        super().__init__()

        self.setWindowTitle("Export")
        self.setWindowIcon(QIcon(resource_path(r'icons\export.png')))
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        label = QLabel("This is a custom popup!", self)
        exportImgBtn = QPushButton("EXPORT AS PNG")
        exportPdfBtn = QPushButton("Export As PDF")

        exportImgBtn.clicked.connect(self.export_png)
        exportPdfBtn.clicked.connect(self.export_pdf)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept) 

        layout.addWidget(label)
        layout.addWidget(close_button)
    
    def export_png(self):
        export_to_img()
        self.close()
    
    def export_pdf(self):
        export_to_pdf()
        self.close()
    
    

        