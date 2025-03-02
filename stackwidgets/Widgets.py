from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton , QSizePolicy , QScrollArea , QFileDialog, QMessageBox
from components.bigbuttons import create_big_button, ImageNavButton, ImageBtn , ActionsBtn
from PyQt6.QtGui import QIcon , QImage , QPixmap
from PyQt6.QtCore import Qt , QSize , QTimer , pyqtSignal, Qt, QThread 
import cv2
import numpy as np
from utils import resource_path , get_all_pages, retrieve_img_files, retrieve_pdf_files, open_file , clear_widget , export_to_pdf, export_to_img
import os
from components.Popups import ExportPopUp
from components.Scrollers import imageSrollerV


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

    switched = pyqtSignal()
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
        self.switched.emit()

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
        QTimer.singleShot(0, self.refresh_file_lists)

    def handle_import_image(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select an Image", "", "Images (*.png *.jpg .*jpeg)")
        if file:
            if not os.path.exists(file):  # Check if file exists
                QMessageBox.critical(self, "Error", "The selected file does not exist!")
                return
            else:
                print("Selected Image", file)
                img = cv2.imread(file)
                # cv2.imshow("Image" , img)
            
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
        self.cap = None

        # Frame Update Timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

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
        self.cap.release()
        event.accept()

class EditImageWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.warpedPages = []

        self.selected = None

        # UI ELEMENTS

        # Home Button
        homebutton =  ImageNavButton('icons/house.png', self.to_home)

        # Export Button
        exportbutton = ImageNavButton(icon = 'icons/export.png',action = self.export_dialog, direction=Qt.LayoutDirection.RightToLeft , text = "EXPORT", fixedsize=(100,50))

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
        export_to_pdf(valid_list)
        export_to_img(valid_list)
        
        ExportPopUp().exec()
    
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
        if self.warpedPages:
            for warped in self.warpedPages:
                imageBtn = ImageBtn(warped,self.set_preview)
                self.imageScroller.add_item(imageBtn)
                imageBtn.on_image_changed.connect(self.preview_updated)
        else:
            imageBtn = ImageBtn(frame,self.set_preview)
            self.imageScroller.add_item(imageBtn)
            imageBtn.on_image_changed.connect(self.preview_updated)

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



    def resizeEvent(self, event):
        """Trigger image resize when the window resizes."""
        if self.q_imaage:
            self.q_imaage = self.q_imaage.scaled(self.previewImage.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            self.previewImage.setPixmap(QPixmap.fromImage(self.q_imaage))
        super().resizeEvent(event)

class FiltersLayout(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedHeight(200)
        layout = QVBoxLayout(self)
        self.selected = None
        # Filters Container
        self.filtersWidget = QWidget() 
        self.filtersWidget.setStyleSheet("background-color: black; border-radius: 10px")
        self.filtersContainer = QVBoxLayout(self.filtersWidget)

        filtersLabel = QLabel("FILTERS")
        filtersLabel.setStyleSheet("font-size: 24px")
        filtersLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.filtersContainer.addWidget(filtersLabel)
        self.filtersSelection = QHBoxLayout()

        self.filters = [ActionsBtn("Orig") , ActionsBtn("Gray") , ActionsBtn("B&W") , ActionsBtn("Nega") ,ActionsBtn("Otsu") , ActionsBtn("AMT") ]

        for filter in self.filters:
            self.filtersSelection.addWidget(filter)
            filter.disable_btn(True)
        
        self.filtersContainer.addLayout(self.filtersSelection)
        
        # IMG Actions Container
        self.imgActionsWidget = QWidget()  # Wrap in a QWidget
        self.imgactionsContainer = QVBoxLayout(self.imgActionsWidget)  
        self.imgActionsWidget.setStyleSheet("background-color: black;  border-radius: 10px")

        actionsLabel = QLabel("IMG")
        actionsLabel.setStyleSheet("font-size: 24px")
        actionsLabel.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        self.actions = [ActionsBtn("Rotate-CCW") , ActionsBtn("Rotate-CW") , ActionsBtn("Delete")]

        self.imgactionsContainer.addWidget(actionsLabel)
        self.actionsSelection = QHBoxLayout()

        
        for action in self.actions:
            self.actionsSelection.addWidget(action)
            action.disable_btn(True)

        self.imgactionsContainer.addLayout(self.actionsSelection)

        self.mainlayout = QHBoxLayout()
        self.mainlayout.addWidget(self.filtersWidget, 1)  
        self.mainlayout.addWidget(self.imgActionsWidget, 1)  
        layout.addLayout(self.mainlayout)

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
    
    


        


