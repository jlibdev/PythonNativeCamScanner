import sys
import mimetypes, os
from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtGui import QFontDatabase , QFont, QIcon
from PyQt6.QtCore import Qt
from stackwidgets.Widgets import LandingWidget , CaptureWidget, EditImageWidget
from utils import resource_path

class CamScammerApp(QStackedWidget):
    def __init__(self):
        super().__init__()


        self.landingwidget = LandingWidget()
        self.capture_widget = CaptureWidget()
        self.edit_image_widget = EditImageWidget()

        self.addWidget(self.landingwidget)
        self.addWidget(self.capture_widget)
        self.addWidget(self.edit_image_widget)


        self.capture_widget.image_captured.connect(self.edit_image_widget.update_image)
        self.capture_widget.image_captured.connect(lambda: self.setCurrentWidget(self.edit_image_widget))

        self.resize(1280,720)


def main():

    app = QApplication(sys.argv)

    font_id = QFontDatabase.addApplicationFont(resource_path("fonts/Jura-VariableFont_wght.ttf"))

    if font_id != -1:
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        app.setFont(QFont(font_family, 12))  

    window = CamScammerApp()
    window.setWindowTitle("CamScammer")
    window.setWindowIcon(QIcon(resource_path("icons/camera.png")))
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()