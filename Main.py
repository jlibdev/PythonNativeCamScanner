import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget , QPushButton
from PyQt6.QtGui import QFontDatabase , QFont, QIcon
import stackwidgets.ImportImageWidget
import stackwidgets.LandingWidget
from stackwidgets.Widgets import CaptureWidget, EditImageWidget
import treads.Watchers
from utils import resource_path, save_path
import treads
import stackwidgets

class CamScammerApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        # STACKABLE WIDGETS / VIEWS
        self.landingwidget = stackwidgets.LandingWidget.LandingWidget()
        self.capture_widget = CaptureWidget()
        self.edit_image_widget = EditImageWidget()
        self.import_image_widget = stackwidgets.ImportImageWidget.ImportImageWidget()

        # WIDGET INITIALIZATION
        self.addWidget(self.landingwidget)
        self.addWidget(self.capture_widget)
        self.addWidget(self.edit_image_widget)
        self.addWidget(self.import_image_widget)

        # WATCHERS

        # File Stream Watcher
        self.file_stream_watcher = treads.Watchers.WatcherThread(save_path)
        self.file_stream_watcher.start()

        # Signal Connections
        self.capture_widget.image_captured.connect(self.edit_image_widget.update_image)
        self.capture_widget.image_captured.connect(lambda: self.setCurrentWidget(self.edit_image_widget))

        self.landingwidget.switched.connect(self.capture_widget.toggle_camera)
        self.file_stream_watcher.file_signal.connect(self.landingwidget.handle_file_change)

        self.resize(1280,720)
    
    def closeEvent(self, a0):
        # Closing Threads
        self.file_stream_watcher.stop()

        return super().closeEvent(a0)

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