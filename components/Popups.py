from PyQt6.QtWidgets import QDialog , QVBoxLayout, QLabel, QPushButton
from PyQt6.QtGui import QIcon
from utils import resource_path, export_to_pdf, export_to_img


class ExportPopUp(QDialog):
    def __init__(self, image_list):
        super().__init__()

        self.image_list = image_list

        self.setWindowTitle("Export")
        self.setWindowIcon(QIcon(resource_path(r'icons\export.png')))
        self.setFixedSize(300, 150)

        layout = QVBoxLayout(self)

        label = QLabel("EXPORT FILES", self)
        exportImgBtn = QPushButton("EXPORT AS PNG")
        exportImgBtn.setIcon(QIcon(resource_path(r'icons\image.png')))
        exportPdfBtn = QPushButton("Export As PDF")
        exportPdfBtn.setIcon(QIcon(resource_path(r'icons\file-text.png')))

        exportImgBtn.clicked.connect(self.export_png)
        exportPdfBtn.clicked.connect(self.export_pdf)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept) 

        layout.addWidget(label)
        layout.addWidget(exportImgBtn)
        layout.addWidget(exportPdfBtn)
        layout.addWidget(close_button)
    
    def export_png(self):
        export_to_img(self.image_list)
        self.close()
    
    def export_pdf(self):
        export_to_pdf(self.image_list)
        self.close()
    
    

        