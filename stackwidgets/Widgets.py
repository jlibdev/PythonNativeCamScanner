from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton , QSizePolicy , QScrollArea , QFileDialog, QMessageBox, QDialog
from components.bigbuttons import create_big_button, ImageNavButton, ImageBtn , ActionsBtn
from PyQt6.QtGui import QIcon , QImage , QPixmap
from PyQt6.QtCore import Qt , QSize , QTimer , pyqtSignal, Qt, QThread
import cv2
import numpy as np
from utils import resource_path , get_all_pages, retrieve_img_files, retrieve_pdf_files, open_file , clear_widget 
import os
from components.Popups import ExportPopUp
from components.Scrollers import imageSrollerV

class ContoursDialog(QDialog):
    def __init__(self, img, contours, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Confirm Contours")
        self.setFixedSize(600, 400)
        self.contours = contours

        # Make a copy of the image and draw only the current contour
        img_with_contour = img.copy()
        cv2.drawContours(img_with_contour, contours, -1, (0, 255, 0), 2)  # Green outline

        # Convert OpenCV image to QPixmap for display
        height, width, ch = img_with_contour.shape
        bytes_per_line = ch * width
        q_image = QImage(img_with_contour.data, width, height, bytes_per_line, QImage.Format.Format_RGB888).rgbSwapped()
        pixmap = QPixmap.fromImage(q_image)

        # Create UI elements
        layout = QVBoxLayout()
        label = QLabel()

        # Get the available size within the layout
        available_width = self.width() - 20  # Adjust padding if necessary
        available_height = self.height() - 100  # Leave space for buttons

        # Scale image to fit inside the available space while keeping the aspect ratio
        scaled_pixmap = pixmap.scaled(available_width, available_height, Qt.AspectRatioMode.KeepAspectRatio)
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)

        # Buttons
        button_layout = QHBoxLayout()
        accept_btn = QPushButton("Accept")
        reject_btn = QPushButton("Reject")

        button_layout.addWidget(accept_btn)
        button_layout.addWidget(reject_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect button signals
        accept_btn.clicked.connect(self.accept)
        reject_btn.clicked.connect(self.reject)

        

# ------------------------------------------------------------------------------------------------    
            
class CaptureWidget(QWidget):
    image_captured = pyqtSignal(object , object)
    def __init__(self):
        super().__init__()
        self.captured_frame = None

        self.pages = []
        self.pages.clear()
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
        self.cap = None

        # Frame Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        # Layout Setup
        navVbox.setAlignment(Qt.AlignmentFlag.AlignVCenter)
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
            if self.captured_frame is None:
                print("No frame captured yet.")  # Debugging output
                return  # Prevent crash if no frame is available

            self.toggle_camera()

            if self.captured_frame is None:
                print("No frame captured yet.")  # Debugging output
                return
            
            self.image_captured.emit(self.pages, self.captured_frame)

            parent = self.parentWidget()
            if parent is not None:
                parent.setCurrentIndex(2)

    def to_home(self):
        self.parentWidget().setCurrentIndex(0)
        if self.timer.isActive():
            self.toggle_camera()

    def set_camera_resolution(self):
        if self.cap.isOpened():
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

    def update_frame(self):
        if self.cap:
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
            self.set_camera_resolution()
            self.timer.start(30)
            self.cameratogglebutton.set_icon('icons/camera-off.png')
            self.videoStatus.setText("🟢Camera Scanning")
            self.videoLabel.show()

    def closeEvent(self, event):
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
        event.accept()

class EditImageWidget(QWidget):

    contours_received = pyqtSignal(list, np.ndarray) #------------------------------ 

    def __init__(self):
        super().__init__()

        self.warpedPages = []

        # Connect the signal to a method
        self.contours_received.connect(self.update_image) #------------------------------ 


        self.selected = None

        # UI ELEMENTS

        # Home Button
        homebutton =  ImageNavButton('icons/house.png', self.to_home)

        # Export Button
        exportbutton = ImageNavButton(icon = 'icons/export.png',action = self.export_dialog, direction=Qt.LayoutDirection.RightToLeft , text = "EXPORT", fixedsize=(100,50))

        # Capture Button

        capturebutton = ImageNavButton('icons/camera.png' , self.to_capture)
        self.q_imaage = None

        # LAYOUTS
        self.mainlayout = QVBoxLayout()
        self.navLayout = QHBoxLayout()
        self.imagePreviewContainer = QHBoxLayout()
        self.imageListContainer = QScrollArea()
        self.imageScroller = imageSrollerV()
        self.imageListContainer.setWidget(self.imageScroller)

        # Styles

        #  Image List Container
        self.imageListContainer.setFixedWidth(70)
        self.imageListContainer.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.imageListContainer.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.imageListContainer.horizontalScrollBar().setFixedSize(0,0)
        self.imageListContainer.verticalScrollBar().setFixedSize(0,0)


        # Navigation
        self.navLayout.addWidget(homebutton)
        self.navLayout.addWidget(capturebutton)
        self.navLayout.addStretch()
        self.navLayout.addWidget(exportbutton)
        self.navLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Image Preview Container
        self.imagePreviewContainer.addWidget(self.imageListContainer)
        self.previewImage = QLabel()
        self.previewImage.setPixmap(QPixmap(resource_path('icons/noimage.png')))
        self.previewImage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.previewImage.setStyleSheet("background-color: black ; border-radius: 10px")
        self.previewImage.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.imagePreviewContainer.addWidget(self.previewImage)

        
        # Filters Container
        self.filtersContainer = FiltersLayout()
        
        # Main Layout
        self.mainlayout.addLayout(self.navLayout)
        self.mainlayout.addLayout(self.imagePreviewContainer)
        self.mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.mainlayout.addWidget(self.filtersContainer)

        self.setLayout(self.mainlayout)
    
    def export_dialog(self):
        valid_list = self.imageScroller.children()[1:]
        ExportPopUp(valid_list).exec()
    
    def to_capture(self):
        parent = self.parentWidget()
        if parent is not None and hasattr(parent, "capture_widget"):
            parent.setCurrentIndex(1)
            parent.capture_widget.toggle_camera()
        else:
            print("Error: capture_widget not found in parentWidget()")
    
    def to_home(self):
        self.warpedPages.clear()
        self.parentWidget().setCurrentIndex(0)
        self.previewImage.setPixmap(QPixmap(resource_path('icons/noimage.png')))
        clear_widget(self.imageListContainer)
        self.filtersContainer.clear_selected()
        
    def update_image(self, pages, frame):
        self.warpedPages.clear()
        for page in pages:
            if len(page) != 4:
                print("Skipping page: Expected 4 corners, found", len(page))
                continue

            page = self.order_corners(page) 
            width_top = np.linalg.norm(page[0] - page[1])  
            width_bottom = np.linalg.norm(page[3] - page[2])  
            max_width = max(int(width_top), int(width_bottom))

            height_left = np.linalg.norm(page[0] - page[3]) 
            height_right = np.linalg.norm(page[1] - page[2])  
            max_height = max(int(height_left), int(height_right))

            inputPts = np.float32(page)
            outputPts = np.float32([[0, 0],
                                    [max_width, 0],
                                    [max_width, max_height],
                                    [0, max_height]])

            M = cv2.getPerspectiveTransform(inputPts, outputPts)

            dst = cv2.warpPerspective(frame, M, (max_width, max_height))

            dst = cv2.detailEnhance(dst, sigma_s=20, sigma_r=0.15)

            self.warpedPages.append(dst)

        self.display_image(frame)
    

    def order_corners(self, corners):
        corners = corners.reshape(4, 2)

        centroid = np.mean(corners, axis=0)

        def calculate_angle(point):
            return np.arctan2(point[1] - centroid[1], point[0] - centroid[0])

        sorted_corners = sorted(corners, key=calculate_angle)

        ordered_corners = np.zeros((4, 2), dtype=np.float32)
        ordered_corners[0] = sorted_corners[0]  
        ordered_corners[1] = sorted_corners[1]  
        ordered_corners[2] = sorted_corners[2] 
        ordered_corners[3] = sorted_corners[3] 

        return ordered_corners

    def display_image(self, frame):

        if frame is None:
            print("Error: Frame is None, cannot display image.")
            return
        
        if self.warpedPages:
            for warped in self.warpedPages:
                imageBtn = ImageBtn(warped,self.set_preview)
                self.imageScroller.add_item(imageBtn)
                imageBtn.on_image_changed.connect(self.preview_updated)
                imageBtn.on_self_delete.connect(self.filtersContainer.clear_selected)
                imageBtn.on_self_delete.connect(self.on_image_deleted)
        else:
            imageBtn = ImageBtn(frame,self.set_preview)
            self.imageScroller.add_item(imageBtn)
            imageBtn.on_image_changed.connect(self.preview_updated)
            imageBtn.on_self_delete.connect(self.filtersContainer.clear_selected)
            imageBtn.on_self_delete.connect(self.on_image_deleted)

    def set_preview(self, selected):
        self.selected = selected
        self.mainlayout.itemAt(2).widget().set_selected(selected)
        q_image = self.selected.q_image
        self.q_imaage = q_image.scaled(self.previewImage.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.previewImage.setPixmap(QPixmap.fromImage(self.q_imaage))

    def preview_updated(self):
        image = self.selected.q_image
        q_image = image
        self.q_imaage = q_image.scaled(self.previewImage.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.previewImage.setPixmap(QPixmap.fromImage(self.q_imaage))

    def on_image_deleted(self):
        self.previewImage.setPixmap(QPixmap(resource_path('icons/noimage.png')))

    def resizeEvent(self, event):
        """Trigger image resize when the window resizes."""
        if self.q_imaage:
            self.q_imaage = self.q_imaage.scaled(self.previewImage.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.previewImage.setPixmap(QPixmap.fromImage(self.q_imaage))
        super().resizeEvent(event)

class FiltersLayout(QWidget):
    def __init__(self):
        super().__init__()

        # Main Layout
        layout = QHBoxLayout(self)
        self.selected = None

        # Filters Container (Black Background)
        self.filtersWidget = QWidget()
        self.filtersWidget.setFixedHeight(100)
        self.filtersWidget.setFixedWidth(1200)
        self.filtersWidget.setStyleSheet("background-color: black; border-radius: 10px;")

        # Layouts for Filters and Actions
        self.filtersContainer = QHBoxLayout(self.filtersWidget)


        # Define Filter Buttons
        self.filters = [ActionsBtn("Orig"), ActionsBtn("Gray"), ActionsBtn("B&W"),
                        ActionsBtn("Nega"), ActionsBtn("Otsu"), ActionsBtn("AMT")]

        # Define Action Buttons
        self.actions = [ActionsBtn("Rotate"), ActionsBtn("Delete")]

        # Apply Styles & Add Buttons to Layouts
        self.setup_buttons(self.filters, self.filtersContainer)
        self.setup_buttons(self.actions, self.filtersContainer)


        # Main Layout
        self.mainlayout = QHBoxLayout()
        self.mainlayout.addWidget(self.filtersWidget, 1)
        layout.addLayout(self.mainlayout)
    
    def setup_buttons(self, buttons, layout):
        for button in buttons:
            button.setStyleSheet("""QPushButton {
                background-color: #f0f0f0;
                color: black;
                border: 2px solid #ccc;
                border-radius: 0px;
                font-size: 12px;
                font-weight: bold;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: grey;
                color: white;
            }
            QPushButton:pressed {
                background-color: lightgrey;
            }
            QPushButton:disabled {
                background-color: #d3d3d3;
                color: #888;
            }""")
            layout.addWidget(button)
           

    def set_selected(self, selected):
        self.selected = selected
        for filter in self.filters:
            filter.set_selected(selected)
            filter.disable_btn(False)
        
        for action in self.actions:
            action.set_selected(selected)
            action.disable_btn(False)

    def clear_selected(self):
        for filter in self.filters:
            filter.set_selected(None)
            filter.disable_btn(True)

        for action in self.actions:
            action.set_selected(None)
            action.disable_btn(True)
    
    


        


