from PyQt6.QtWidgets import QDialog , QVBoxLayout, QLabel, QPushButton, QMessageBox 
from PyQt6.QtGui import QIcon
from utilities import file_processing

class ExportPopUp(QDialog):
    def __init__(self, image_list):
        super().__init__()

        self.image_list = image_list

        self.setWindowTitle("Export")
        self.setWindowIcon(QIcon(file_processing.resource_path(r'icons\export.png')))
        self.setFixedSize(300, 150)
        self.msg = QMessageBox()
        self.msg.setWindowIcon(QIcon(file_processing.resource_path(r'icons\camera.png')))

        layout = QVBoxLayout(self)

        label = QLabel("EXPORT FILES", self)
        exportImgBtn = QPushButton("EXPORT AS PNG")
        exportImgBtn.setIcon(QIcon(file_processing.resource_path(r'icons\image.png')))
        exportPdfBtn = QPushButton("Export As PDF")
        exportPdfBtn.setIcon(QIcon(file_processing.resource_path(r'icons\file-text.png')))

        exportImgBtn.clicked.connect(self.export_png)
        exportPdfBtn.clicked.connect(self.export_pdf)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.accept) 

        layout.addWidget(label)
        layout.addWidget(exportImgBtn)
        layout.addWidget(exportPdfBtn)
        layout.addWidget(close_button)
    
    def export_png(self):
        
        if file_processing.export_to_img(self.image_list):
            self.msg.setWindowTitle("Exported Successfully!")
            self.msg.setText("Images has been exported as PDFs")
            self.msg.setIcon(QMessageBox.Icon.Information)
            self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        else:
            self.msg.setWindowTitle("Export Failed!")
            self.msg.setText("There are no images to export")
            self.msg.setIcon(QMessageBox.Icon.Warning)
            self.msg.setStandardButtons(QMessageBox.StandardButton.Close)
        self.msg.exec()
        self.close()
    
    def export_pdf(self):
        if file_processing.export_to_pdf(self.image_list):
            self.msg.setWindowTitle("Exported Successfully!")
            self.msg.setText("Images has been exported as PDFs")
            self.msg.setIcon(QMessageBox.Icon.Information)
            self.msg.setStandardButtons(QMessageBox.StandardButton.Ok)
        else:
            self.msg.setWindowTitle("Export Failed!")
            self.msg.setText("There are no images to export")
            self.msg.setIcon(QMessageBox.Icon.Warning)
            self.msg.setStandardButtons(QMessageBox.StandardButton.Close)
        self.msg.exec()
        self.close()
    

    

        