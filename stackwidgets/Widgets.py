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
        self.videoStatus.setAlignment(Qt.AlignmentFlag.AlignCenter)

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

            self.captured_frame = frame.copy()

            display_frame = frame.copy()

            self.pages = []

            # Sir Function

            get_all_pages(display_frame, self.pages)

            for page in self.pages:
                cv2.drawContours(display_frame, [page], -1, (0, 255, 0), 3) 

            # Sir Function
            
            h, w , ch = display_frame.shape
            bytes_per_line = ch * w
            qimg = QImage(display_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

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
            self.videoLabel.hide()
        else:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.set_camera_resolution()
            self.timer.start(30)
            self.button.setIcon(QIcon(resource_path('icons/camera-off.png')))
            self.videoStatus.setText("🟢Camera Scanning")
            self.videoLabel.show()

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

class EditImageWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")

        self.warpedPages = []
        self.home = QPushButton("Home" ,self)
        self.home.clicked.connect(self.to_home)
        

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)

        self.mainlayout = QHBoxLayout()
        self.imageVbox = QVBoxLayout()
        self.image_label = QLabel(self)
        self.mainlayout.addLayout(self.imageVbox)
        self.mainlayout.addWidget(self.home)
        self.mainlayout.addWidget(self.scroll_area)
       
        self.setLayout(self.mainlayout)
    
    def to_home(self):
        self.warpedPages = []
        self.parentWidget().setCurrentIndex(0)
    
    def update_image(self, pages, frame):
        for page in pages:
            # Ensure the page has exactly 4 points (corners)
            if len(page) != 4:
                print("Skipping page: Expected 4 corners, found", len(page))
                continue

            # Order the corners consistently (top-left, top-right, bottom-right, bottom-left)
            page = self.order_corners(page)  # Implement this function to order the corners

            # Calculate the width and height of the ROI
            width_top = np.linalg.norm(page[0] - page[1])  # Distance between top-left and top-right
            width_bottom = np.linalg.norm(page[3] - page[2])  # Distance between bottom-left and bottom-right
            max_width = max(int(width_top), int(width_bottom))

            height_left = np.linalg.norm(page[0] - page[3])  # Distance between top-left and bottom-left
            height_right = np.linalg.norm(page[1] - page[2])  # Distance between top-right and bottom-right
            max_height = max(int(height_left), int(height_right))

            # Define input points (corners of the page)
            inputPts = np.float32(page)

            # Define output points (corners of the output image with retained aspect ratio)
            outputPts = np.float32([[0, 0],
                                    [max_width, 0],
                                    [max_width, max_height],
                                    [0, max_height]])

            # Compute the perspective transformation matrix
            M = cv2.getPerspectiveTransform(inputPts, outputPts)

            # Warp the perspective of the frame
            dst = cv2.warpPerspective(frame, M, (max_width, max_height))

            # Enhance the warped image
            dst = cv2.detailEnhance(dst, sigma_s=20, sigma_r=0.15)

            # Store the enhanced image
            self.warpedPages.append(dst)

        # Display the updated image
        self.display_image()
    
    def order_corners(self, corners):
        # Reshape the corners array to (4, 2)
        corners = corners.reshape(4, 2)

        # Initialize an array to store the ordered corners
        ordered_corners = np.zeros((4, 2), dtype=np.float32)

        # Sum the x and y coordinates to find the top-left and bottom-right corners
        sum_coords = corners.sum(axis=1)
        ordered_corners[0] = corners[np.argmin(sum_coords)]  # Top-left
        ordered_corners[2] = corners[np.argmax(sum_coords)]  # Bottom-right

        # Difference of x and y coordinates to find the top-right and bottom-left corners
        diff_coords = np.diff(corners, axis=1)
        ordered_corners[1] = corners[np.argmin(diff_coords)]  # Top-right
        ordered_corners[3] = corners[np.argmax(diff_coords)]  # Bottom-left

        return ordered_corners


    def display_image(self):
        cv2.imshow("", self.warpedPages[0])
        # for warped in self.warpedPages:
        #     warped_rgb = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
        #     height, width, channels = warped_rgb.shape
        #     bytes_per_line = channels * width
        #     q_image = QImage(warped_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
        #     image_label = QLabel()
        #     image_label.setPixmap(QPixmap.fromImage(q_image))
        #     image_label.setScaledContents(True) 
        #     self.imageVbox.addWidget(image_label)

