from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton , QSizePolicy
from components.bigbuttons import ImageNavButton
from PyQt6.QtGui import QIcon , QImage , QPixmap
from PyQt6.QtCore import Qt , QSize , QTimer , pyqtSignal, Qt
import cv2
from utilities import image_processing , file_processing


class CaptureWidget(QWidget):

    # SIGNALS INIT
    image_captured = pyqtSignal(object , object)

    def __init__(self , parent=None):
        from Main import CamScammerApp
        super().__init__(parent)

        self.parent : CamScammerApp = parent

        # VARIABLES
        self.frame = None
        self.cap = None
        self.valid_contours = None
        self.timer = QTimer()

        # UI ELEMENTS

        ## Home Button
        homebutton =  ImageNavButton('icons/house.png', self.to_home)

        ## Camera Capture Frame Button
        capbutton = QPushButton()
        capbutton.setIcon(QIcon(file_processing.resource_path('icons/aperture.png')))
        capbutton.setIconSize(QSize(50, 50))
        capbutton.setFixedSize(70, 70)
        capbutton.setStyleSheet("""
            QPushButton {
                border-radius: 35px;
                border: none;
            }
            QPushButton:hover {background-color: #ACACAC}
        """)
        capbutton.setShortcut("c")

        ## Camera Toggle Button
        self.cameratogglebutton = ImageNavButton('icons/camera-off.png', self.toggle_camera)

        ## Video Stream Status
        self.videoStatus = QLabel("🟢Camera Scanning")
        self.videoStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)

        ## Video Stream View 
        self.videoLabel = QLabel(self)
        self.videoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.videoLabel.setStyleSheet("background-color: black;") 
        self.videoLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))


        # LAYOUTS

        ## Navigation Layout
        navVbox = QVBoxLayout()
        navVbox.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        navVbox.addWidget(homebutton)
        navVbox.addWidget(self.cameratogglebutton)

        ## VideoStream Layout
        videoSteamVbox = QVBoxLayout()
        videoSteamVbox.addWidget(self.videoStatus)
        videoSteamVbox.addWidget(self.videoLabel, 1)


        ## Actions Layout
        actionsVbox = QVBoxLayout()
        actionsVbox.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        actionsVbox.addWidget(capbutton)

        ## Main Layout
        mainlayout = QHBoxLayout()
        mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainlayout.addLayout(navVbox)
        mainlayout.addLayout(videoSteamVbox, 1)  
        mainlayout.addLayout(actionsVbox)

        # SIGNALS CONNECT

        capbutton.clicked.connect(self.capture_image)
        self.timer.timeout.connect(self.update_frame)

        # OTHERS
        self.setLayout(mainlayout)

    def capture_image(self):
        if self.timer.isActive():
            if self.frame is None:
                print("No frame captured yet.")
                return 
            


            self.toggle_camera()
 
            self.image_captured.emit(self.valid_contours, self.frame)

            if self.parent is not None:
                self.parent.setCurrentWidget(self.parent.edit_image_widget)

    def to_home(self):
        if self.parent is not None:
                self.parent.setCurrentWidget(self.parent.landingwidget)
        if self.timer.isActive():
            self.toggle_camera()

    def update_frame(self):
        if self.cap:
            success, self.frame = self.cap.read()

            if success:
                self.frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)

                display_frame, self.valid_contours = image_processing.get_contours_cv(self.frame)

                h, w , ch = display_frame.shape
                bytes_per_line = ch * w
                qimg = QImage(display_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

                scaled_pixmap = QPixmap.fromImage(qimg).scaled(
                    self.videoLabel.width(), 
                    self.videoLabel.height(), 
                    Qt.AspectRatioMode.KeepAspectRatio, 
                    Qt.TransformationMode.SmoothTransformation
                )
                self.videoLabel.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        self.update_frame()
        super().resizeEvent(event)

    def toggle_camera(self):
        if self.timer.isActive():
            print("Camera Toggled Off")
            self.timer.stop()
            self.cap.release()
            self.cameratogglebutton.set_icon('icons/camera.png')
            self.videoStatus.setText("🔴Camera Offline")
            self.videoLabel.hide()
        else:
            print("Camera Toggled On")
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.timer.start(30)
            self.cameratogglebutton.set_icon('icons/camera-off.png')
            self.videoStatus.setText("🟢Camera Scanning")
            self.videoLabel.show()