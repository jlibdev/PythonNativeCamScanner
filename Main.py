import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget
from PyQt6.QtGui import QFontDatabase , QFont, QIcon
from stackwidgets.Widgets import LandingWidget , CaptureWidget, EditImageWidget
import treads.Watchers
from utils import resource_path
import treads

class CamScammerApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        # STACKABLE WIDGETS / VIEWS
        self.landingwidget = LandingWidget()
        self.capture_widget = CaptureWidget()
        self.edit_image_widget = EditImageWidget()

        # WATCHERS

        # File Stream Watcher
        self.file_stream_watcher = treads.Watchers.WatcherThread(r'C:\Users\Joshua Libando\Dropbox\PC\Documents\camscanner_files')
        self.file_stream_watcher.start()
        self.file_stream_watcher.file_signal.connect(self.handle_file_event)


        self.addWidget(self.landingwidget)
        self.addWidget(self.capture_widget)
        self.addWidget(self.edit_image_widget)
        
        # Signal Connections
        self.capture_widget.image_captured.connect(self.edit_image_widget.update_image)
        self.capture_widget.image_captured.connect(lambda: self.setCurrentWidget(self.edit_image_widget))
        self.landingwidget.switched.connect(self.capture_widget.toggle_camera)
        self.resize(1280,720)

    def handle_file_event(self , message):
        print(message)
    
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