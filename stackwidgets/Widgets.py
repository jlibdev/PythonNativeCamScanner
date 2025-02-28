from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton , QSizePolicy , QScrollArea
from components.bigbuttons import create_big_button
from PyQt6.QtGui import QIcon , QImage , QPixmap
from PyQt6.QtCore import Qt , QSize , QTimer , pyqtSignal
import cv2
import numpy as np
from utils import resource_path , get_all_pages

class LandingWidget(QWidget):
    def __init__(self):
        super().__init__()

        mainlayout = QVBoxLayout()
        mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainlayout.setSpacing(50)

        appname = QLabel("CAMSCAMMER")
        appname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        appname.setStyleSheet("QLabel { font-size: 70px; }")

        buttonsHbox = QHBoxLayout()
        buttonsHbox.addWidget(create_big_button("IMPORT IMAGE FROM LOCAL FILE" , resource_path('icons/folderdown.png') , self.to_import))
        buttonsHbox.addWidget(create_big_button("CAPTURE IMAGE FROM CAMERA" , resource_path('icons/camera.png') , self.to_capture))

        filesteamLabel = QLabel("Filestream")
        filesteamLabel.setStyleSheet("QLabel { font-size: 20px; padding: 10px; }")

        mainlayout.addWidget(appname)
        mainlayout.addLayout(buttonsHbox)
        mainlayout.addWidget(filesteamLabel)
        self.setLayout(mainlayout)
    
    def to_import(self):
        self.parentWidget().setCurrentIndex(1) 
    def to_capture(self):
        self.parentWidget().setCurrentIndex(1)

class CaptureWidget(QWidget):

    image_captured = pyqtSignal(object , object)
    def __init__(self):
        super().__init__()

        self.captured_frame = None
        self.captured_pages = None

        self.pages = []
        mainlayout = QHBoxLayout()
        mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        navVbox = QVBoxLayout()
        videoSteamVbox = QVBoxLayout()
        actionsVbox = QVBoxLayout()

        # Home Button
        homebutton = QPushButton()
        homebutton.setIcon(QIcon(resource_path('icons/house.png')))
        homebutton.setIconSize(QSize(30, 30))
        homebutton.setFixedSize(50, 50)
        homebutton.setStyleSheet("""
            QPushButton {
                border-radius: 25px;  
                border: none;
            }
            QPushButton:hover {background-color: #ACACAC}
        """)
        homebutton.clicked.connect(self.to_home)

        # Capture Button
        capbutton = QPushButton()
        capbutton.setIcon(QIcon(resource_path('icons/aperture.png')))
        capbutton.setIconSize(QSize(50, 50))
        capbutton.setFixedSize(70, 70)
        capbutton.setStyleSheet("""
            QPushButton {
                border-radius: 35px;
                border: none;
            }
            QPushButton:hover {background-color: #ACACAC}
        """)
        capbutton.clicked.connect(self.capture_image)

        #  Video Stream Label

        self.videoStatus = QLabel("🟢Camera Scanning")

        # Video Stream
        self.videoLabel = QLabel(self)
        self.videoLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.videoLabel.setStyleSheet("background-color: black;") 
        self.videoLabel.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        # OpenCV Camera Setup
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.set_camera_resolution()

        # Control Button
        self.button = QPushButton(self)
        self.button.setIcon(QIcon(resource_path('icons/camera-off.png')))
        self.button.setIconSize(QSize(24, 24))
        self.button.setFixedSize(50, 50)
        self.button.setStyleSheet("""
            QPushButton {
                border-radius: 25px;
                border: none;
            }
            QPushButton:hover {background-color: #ACACAC}
        """)
        self.button.clicked.connect(self.toggle_camera)

        # Frame Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Layout Setup
        navVbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        navVbox.addWidget(homebutton)
        navVbox.addWidget(self.button)

        videoSteamVbox.addWidget(self.videoStatus)
        videoSteamVbox.addWidget(self.videoLabel, 1)

        actionsVbox.setAlignment(Qt.AlignmentFlag.AlignVCenter)
        actionsVbox.addWidget(capbutton)

        mainlayout.addLayout(navVbox)
        mainlayout.addLayout(videoSteamVbox, 1)  
        mainlayout.addLayout(actionsVbox)

        self.setLayout(mainlayout)
        self.setWindowTitle("Cam Scammer App")

    def capture_image(self):
        if self.timer.isActive():
            self.toggle_camera()
            self.image_captured.emit(self.pages , self.captured_frame)
            
            self.parentWidget().setCurrentIndex(2)

    def to_home(self):
        self.parentWidget().setCurrentIndex(0)
        if self.timer.isActive():
            self.toggle_camera()

    def set_camera_resolution(self):
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def update_frame(self):
        success, frame = self.cap.read()
        if success:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            self.captured_frame = frame

            self.pages = []

            # Sir Function

            get_all_pages(frame, self.pages)

            self.captured_pages = self.pages
            
            for page in self.pages:
                cv2.drawContours(frame, [page], -1, (0, 255, 0), 3) 

            # Sir Function
            
            h, w, ch = frame.shape
            bytes_per_line = ch * w
            qimg = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

            # Resize frame to QLabel's current size
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
            self.timer.stop()
            self.cap.release()
            self.button.setIcon(QIcon(resource_path('icons/camera.png')))
            self.videoStatus.setText("🔴Camera Offline")
        else:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.set_camera_resolution()
            self.timer.start(30)
            self.button.setIcon(QIcon(resource_path('icons/camera-off.png')))
            self.videoStatus.setText("🟢Camera Scanning")

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

class EditImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")

        self.warpedPages = []

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True) 

        mainlayout = QHBoxLayout()
        self.imageVbox = QVBoxLayout()
        self.image_label = QLabel(self)
        mainlayout.addLayout(self.imageVbox)
        mainlayout.addWidget(self.scroll_area)
       
        self.setLayout(mainlayout)

    def update_image(self, pages , frame):
    
        for page in pages:
            inputPts = np.float32(page)

            outputPts = np.float32([[0,0],
                        [0,800],
                        [500,800],
                        [500,0]])
            M = cv2.getPerspectiveTransform(inputPts,outputPts)

            dst = cv2.warpPerspective(frame, M, (500,800))

            self.warpedPages.append(dst)

        self.display_image()


    def display_image(self):
        for warped in self.warpedPages:
            warped_rgb = cv2.cvtColor(self.warpedPages[0], cv2.COLOR_BGR2RGB)
            height, width, channels = warped_rgb.shape
            bytes_per_line = channels * width
            q_image = QImage(warped_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            image_label = QLabel()
            image_label.setPixmap(QPixmap.fromImage(q_image))
            image_label.setScaledContents(True) 
            self.imageVbox(image_label)

        
