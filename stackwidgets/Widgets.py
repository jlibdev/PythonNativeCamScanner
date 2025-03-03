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
    
    


        


