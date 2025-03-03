from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton, QScrollArea , QFileDialog, QMessageBox
from components.bigbuttons import create_big_button
from PyQt6.QtCore import Qt , QTimer , pyqtSignal, Qt
import cv2
from utils import resource_path , get_all_pages, retrieve_img_files, retrieve_pdf_files, open_file , clear_widget 
import os

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
        self.scrollAreaLayoutLeft = scrollAreaLayoutLeft 
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