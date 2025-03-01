from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton , QSizePolicy , QScrollArea , QFileDialog, QMessageBox
from components.bigbuttons import create_big_button, ImageButton , ImageNavButton
from PyQt6.QtGui import QIcon , QImage , QPixmap
from PyQt6.QtCore import Qt , QSize , QTimer , pyqtSignal, Qt, QThread 
import cv2
import numpy as np
from utils import resource_path , get_all_pages, retrieve_img_files, retrieve_pdf_files, open_file
import os
from components.Popups import ExportPopUp


class WatcherThread(QThread):
    file_signal = pyqtSignal(str)
    
    def __init__(self, watch_path):
        super().__init__()
        self.watch_path = watch_path
        self.running = True
    
    def run(self):
        while self.running:
            # Implement actual file-watching logic here
            self.msleep(1000)  # Simulate delay
            self.file_signal.emit("File changed")
    
    def stop(self):
        self.running = False
        self.quit()
        self.wait()

class LandingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.img_buttons = {}
        self.pdf_buttons = {}
        home_dir = os.path.expanduser("~")
        self.watch_path = os.path.join(home_dir, "Documents", "camscanner_files")
        self.init_ui()
        self.start_watcher()

    def init_ui(self):

        mainlayout = QVBoxLayout()
        mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainlayout.setSpacing(50)

        appname = QLabel("CAMSCAMMER")
        appname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        appname.setStyleSheet("QLabel { font-size: 70px; }")

        buttonsHbox = QHBoxLayout()
        buttonsHbox.addWidget(create_big_button("IMPORT IMAGE FROM LOCAL FILE" , resource_path('icons/folderdown.png') , self.handle_import_image))
        buttonsHbox.addWidget(create_big_button("CAPTURE IMAGE FROM CAMERA" , resource_path('icons/camera.png') , self.to_capture))

        filesteamLabel = QLabel("Filestream")
        filesteamLabel.setStyleSheet("QLabel { font-size: 20px; padding: 10px; }")
        mainlayout.addWidget(appname)
        mainlayout.addLayout(buttonsHbox)
        mainlayout.addWidget(filesteamLabel)

        # -------------- Kyr Works


        # Titles
        title_left = QLabel("Images")
        title_left.setStyleSheet("color: black; font-weight: bold; padding-left: 5px;")

        title_right = QLabel("PDFs")
        title_right.setStyleSheet("color: black; font-weight: bold; padding-left: 5px;")

        # Left Layout (Images)
        subleftLayout = QVBoxLayout()
        subleftLayout.addWidget(title_left)
            
        scrollAreaLeft = QScrollArea()
        scrollAreaLeft.setWidgetResizable(True)
        scrollAreaLeft.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Hide Vertical Scroll Bar
        scrollAreaLeft.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Hide Horizontal Scroll Bar
        scrollAreaWidgetLeft = QWidget()
        scrollAreaLayoutLeft = QVBoxLayout(scrollAreaWidgetLeft)
        scrollAreaLayoutLeft.setAlignment(Qt.AlignmentFlag.AlignTop)  # Keep content at the top
        scrollAreaLayoutLeft.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)  # Prevent stretching

        scrollAreaWidgetLeft.setLayout(scrollAreaLayoutLeft)
        scrollAreaLeft.setWidget(scrollAreaWidgetLeft)
        subleftLayout.addWidget(scrollAreaLeft)

        # Right Layout (PDFs)
        subrightLayout = QVBoxLayout()
        subrightLayout.addWidget(title_right)

        scrollAreaRight = QScrollArea()
        scrollAreaRight.setWidgetResizable(True)
        scrollAreaRight.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollAreaRight.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)  # Hide Horizontal Scroll Bar
        scrollAreaWidgetRight = QWidget()
        scrollAreaLayoutRight = QVBoxLayout(scrollAreaWidgetRight)
        scrollAreaLayoutRight.setAlignment(Qt.AlignmentFlag.AlignTop)  # Keep content at the top
        scrollAreaLayoutRight.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)  # Prevent stretching

        for pdf in pdfs:
            filename = os.path.basename(pdf)
            if len(filename) > 50:
                filename = filename[:47] + "..."  # Keep first 17 chars and add epsilon
            btn = QPushButton(filename)
            btn.setStyleSheet("""
            QPushButton {background-color: white; color: black; border-radius: 0px; min-height: 30px;}
""")
            btn.clicked.connect(lambda _, path=pdf: open_file(path))
            scrollAreaLayoutRight.addWidget(btn)

        scrollAreaWidgetRight.setLayout(scrollAreaLayoutRight)
        scrollAreaRight.setWidget(scrollAreaWidgetRight)

        subrightLayout.addWidget(scrollAreaRight)

        # Left Widget
        subleftWidget = QWidget()
        subleftWidget.setLayout(subleftLayout)
        subleftWidget.setStyleSheet("background-color: lightgrey;")

        # Right Widget
        subrightWidget = QWidget()
        subrightWidget.setLayout(subrightLayout)
        subrightWidget.setStyleSheet("background-color: lightgrey;")

        # Parent Layout
        parentLayout = QHBoxLayout()
        parentLayout.setSpacing(10)
        parentLayout.addWidget(subleftWidget)
        parentLayout.addWidget(subrightWidget)

        # Main Container
        subWidget = QWidget()
        subWidget.setLayout(parentLayout)
        subWidget.setStyleSheet("background-color: grey;")

        mainlayout.addWidget(subWidget)
        # --------------------------
        self.scrollAreaLayoutLeft = scrollAreaLayoutLeft  # Store layout in self
        self.scrollAreaLayoutRight = scrollAreaLayoutRight
        self.setLayout(mainlayout)

    def to_import(self):
        self.parentWidget().setCurrentIndex(1) 

    def to_capture(self):
        self.parentWidget().setCurrentIndex(1)

    def refresh_file_lists(self):
        #print(" Refreshing file lists...")
        imgs = retrieve_img_files()
        pdfs = retrieve_pdf_files()

        # Update Images List
        existing_imgs = set(self.img_buttons.keys())
        new_imgs = set(imgs)

        # Remove old buttons
        for old_img in existing_imgs - new_imgs:
            btn = self.img_buttons.pop(old_img)
            self.scrollAreaLayoutLeft.removeWidget(btn)
            btn.deleteLater()

        # Add new buttons
        for new_img in new_imgs - existing_imgs:
            filename = os.path.basename(new_img)
            filename = filename[:47] + "..." if len(filename) > 50 else filename
            btn = QPushButton(filename)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: black;
                    border-radius: 0px;
                    min-height: 30px;
                }
                QPushButton:hover {
                    background-color: grey;
                    color : white;
                }
            """)
            btn.clicked.connect(lambda _, path=new_img: open_file(path))
            self.scrollAreaLayoutLeft.addWidget(btn)
            self.img_buttons[new_img] = btn  # Store button reference

        # Update PDFs List
        existing_pdfs = set(self.pdf_buttons.keys())
        new_pdfs = set(pdfs)

        # Remove old buttons
        for old_pdf in existing_pdfs - new_pdfs:
            btn = self.pdf_buttons.pop(old_pdf)
            self.scrollAreaLayoutRight.removeWidget(btn)
            btn.deleteLater()

        # Add new buttons
        for new_pdf in new_pdfs - existing_pdfs:
            filename = os.path.basename(new_pdf)
            filename = filename[:47] + "..." if len(filename) > 50 else filename
            btn = QPushButton(filename)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    color: black;
                    border-radius: 0px;
                    min-height: 30px;
                }
                QPushButton:hover {
                    background-color: grey;
                    color : white;
                }
            """)
            btn.clicked.connect(lambda _, path=new_pdf: open_file(path))
            self.scrollAreaLayoutRight.addWidget(btn)
            self.pdf_buttons[new_pdf] = btn  # Store button reference

        self.update()

    def clear_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
    
    def start_watcher(self):
        self.watcher_thread = WatcherThread(self.watch_path)
        self.watcher_thread.file_signal.connect(self.handle_file_change, Qt.ConnectionType.QueuedConnection)
        self.watcher_thread.start()

    def handle_file_change(self, message):
        #print(f"📢 Received signal: {message}")
        QTimer.singleShot(0, self.refresh_file_lists)

    def handle_import_image(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select an Image", "", "Images (*.png *.jpg .*jpeg)")
        if file:
            print("Selected Image", file)
            img = cv2.imread(file)
            # cv2.imshow("Image" , img)
        else:
            msg = QMessageBox()
            msg.setWindowIcon(QIcon(resource_path('icons/circle-alert.png')))
            msg.setWindowTitle("Error!")
            msg.setText("An Error occurred while opening the file! Please try again...")
            msg.setIcon(QMessageBox.Icon.Warning)
            msg.setStandardButtons(QMessageBox.StandardButton.Ok)
            msg.exec()
        
             
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
        homebutton =  ImageNavButton('icons/house.png', self.to_home)

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
        capbutton.setShortcut("c")

        # Camera Status Toggle
        self.cameratogglebutton = ImageNavButton('icons/camera-off.png', self.toggle_camera)

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

        # Frame Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)

        # Layout Setup
        navVbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        navVbox.addWidget(homebutton)
        navVbox.addWidget(self.cameratogglebutton)

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
            self.cameratogglebutton.set_icon('icons/camera.png')
            self.videoStatus.setText("🔴Camera Offline")
            self.videoLabel.hide()
        else:
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            self.set_camera_resolution()
            self.timer.start(30)
            self.cameratogglebutton.set_icon('icons/camera-off.png')
            self.videoStatus.setText("🟢Camera Scanning")
            self.videoLabel.show()

    def closeEvent(self, event):
        self.cap.release()
        event.accept()

class EditImageWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.warpedPages = []

        # UI ELEMENTS

        # Home Button
        homebutton =  ImageNavButton('icons/house.png', self.to_home)

        # Export Button
        exportbutton = ImageNavButton('icons/export.png', self.export_dialog)

        # LAYOUTS

        # Navigation
        self.navLayout = QHBoxLayout()
        self.navLayout.addWidget(homebutton)
        self.navLayout.addStretch()
        self.navLayout.addWidget(exportbutton)
        self.navLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Image Layout
        self.imageVbox = QVBoxLayout()
        self.imageHbox = QHBoxLayout()
        self.imageVbox.addLayout(self.imageHbox) 
        self.image_label = QLabel(self)

        # Main Layout
        self.mainlayout = QVBoxLayout()
        self.mainlayout.addLayout(self.navLayout)
        self.mainlayout.addLayout(self.imageVbox)
        
        
       
        self.setLayout(self.mainlayout)
    
    def export_dialog(self):
        ExportPopUp().exec()
    
    def to_home(self):
        self.warpedPages = []
        self.parentWidget().setCurrentIndex(0)
    
    def update_image(self, pages, frame):
        self.warpedPages.clear()
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
        
            print(max_height, max_width, height_left, height_right)

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
        self.display_image(frame)
    
    
    def order_corners(self, corners):
        # Reshape the corners array to (4, 2)
        corners = corners.reshape(4, 2)

        # Find the centroid of the corners
        centroid = np.mean(corners, axis=0)

        # Calculate the angle of each corner relative to the centroid
        def calculate_angle(point):
            return np.arctan2(point[1] - centroid[1], point[0] - centroid[0])

        # Sort the corners based on their angles
        sorted_corners = sorted(corners, key=calculate_angle)

        # Ensure the order is consistent (top-left, top-right, bottom-right, bottom-left)
        # The sorted corners will be in clockwise or counter-clockwise order, so we need to rearrange them
        # Here, we assume the sorted corners are in clockwise order
        ordered_corners = np.zeros((4, 2), dtype=np.float32)
        ordered_corners[0] = sorted_corners[0]  # Top-left
        ordered_corners[1] = sorted_corners[1]  # Top-right
        ordered_corners[2] = sorted_corners[2]  # Bottom-right
        ordered_corners[3] = sorted_corners[3]  # Bottom-left

        return ordered_corners


    def display_image(self, frame):
        if self.warpedPages:
            for warped in self.warpedPages:
                warped_rgb = cv2.cvtColor(warped, cv2.COLOR_BGR2RGB)
                height, width, channels = warped_rgb.shape
                bytes_per_line = channels * width
                q_image = QImage(warped_rgb.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
                image_label = QLabel()
                image_label.setPixmap(QPixmap.fromImage(q_image))
                self.imageHbox.addWidget(ImageButton(image_label))
        else:
            height, width, channels = frame.shape
            bytes_per_line = channels * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
            image_label = QLabel()
            image_label.setPixmap(QPixmap.fromImage(q_image))
            self.imageHbox.addWidget(ImageButton(image_label))

