from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton, QScrollArea , QFileDialog, QMessageBox
from components.bigbuttons import create_big_button
from PyQt6.QtCore import Qt , QTimer , pyqtSignal, Qt
import os
from utilities import file_processing


class LandingWidget(QWidget):
    switched = pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
        from Main import CamScammerApp
        self.parent: CamScammerApp = parent
        self.img_buttons = {}
        self.pdf_buttons = {}
        self.init_ui()

    def init_ui(self):
        # UI ELEMENTS

        ## App Name Label
        appname = QLabel("CAMSCAMMER")
        appname.setAlignment(Qt.AlignmentFlag.AlignCenter)
        appname.setStyleSheet("QLabel { font-size: 70px; }")

        ## File Stream Labels
        filesteamLabel = QLabel("Filestream")
        filesteamLabel.setStyleSheet("QLabel { font-size: 20px; padding: 10px; }")

        title_left = QLabel("Images")
        title_left.setStyleSheet("color: black; font-weight: bold; padding-left: 5px;")

        title_right = QLabel("PDFs")
        title_right.setStyleSheet("color: black; font-weight: bold; padding-left: 5px;")

        ## File Stream Scrollable Area [Images]

        ### Scroll Area [Images]
        scrollAreaLeft = QScrollArea()

        scrollAreaLeft.setWidgetResizable(True)
        scrollAreaLeft.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollAreaLeft.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        ### Scroll Content [Images]
        scrollAreaWidgetLeft = QWidget()
        scrollAreaLayoutLeft = QVBoxLayout(scrollAreaWidgetLeft)
        scrollAreaLayoutLeft.setAlignment(Qt.AlignmentFlag.AlignTop) 
        scrollAreaLayoutLeft.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)

        scrollAreaWidgetLeft.setLayout(scrollAreaLayoutLeft)
        scrollAreaLeft.setWidget(scrollAreaWidgetLeft)

        ## File Stream Scrollable Area [PDFs]
        
        ### Scroll Area [PDFs]
        scrollAreaRight = QScrollArea()

        scrollAreaRight.setWidgetResizable(True)
        scrollAreaRight.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scrollAreaRight.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        ### Scroll Content [PDFs]
        scrollAreaWidgetRight = QWidget()
        scrollAreaLayoutRight = QVBoxLayout(scrollAreaWidgetRight)
        scrollAreaLayoutRight.setAlignment(Qt.AlignmentFlag.AlignTop)  # Keep content at the top
        scrollAreaLayoutRight.setSizeConstraint(QVBoxLayout.SizeConstraint.SetMinimumSize)  # Prevent stretching

        scrollAreaWidgetRight.setLayout(scrollAreaLayoutRight)
        scrollAreaRight.setWidget(scrollAreaWidgetRight)


        # LAYOUTS
        
        ## Big Button Navigation Layout
        buttonsHbox = QHBoxLayout()
        buttonsHbox.addWidget(create_big_button("IMPORT IMAGE FROM LOCAL FILE" , file_processing.resource_path('icons/folderdown.png') , self.handle_import_image))
        buttonsHbox.addWidget(create_big_button("CAPTURE IMAGE FROM CAMERA" , file_processing.resource_path('icons/camera.png') , self.to_capture))

        ## File Stream Layouts

        ### Images List Layout
        subleftLayout = QVBoxLayout()
        subleftLayout.addWidget(title_left)
        subleftLayout.addWidget(scrollAreaLeft)

        ### PDFs List Layout
        subrightLayout = QVBoxLayout()
        subrightLayout.addWidget(title_right)
        subrightLayout.addWidget(scrollAreaRight)

        ### Left Widget
        subleftWidget = QWidget()
        subleftWidget.setLayout(subleftLayout)
        subleftWidget.setStyleSheet("background-color: lightgrey;")

        ### Right Widget
        subrightWidget = QWidget()
        subrightWidget.setLayout(subrightLayout)
        subrightWidget.setStyleSheet("background-color: lightgrey;")

        ### File Stream Parent Layout
        parentLayout = QHBoxLayout()
        parentLayout.setSpacing(10)
        parentLayout.addWidget(subleftWidget)
        parentLayout.addWidget(subrightWidget)

        ### FileStream Widget Container
        subWidget = QWidget()
        subWidget.setLayout(parentLayout)
        subWidget.setStyleSheet("background-color: grey;")

        ## Main Layout
        mainlayout = QVBoxLayout()
        mainlayout.setAlignment(Qt.AlignmentFlag.AlignTop)
        mainlayout.setSpacing(50)

        mainlayout.addWidget(appname)
        mainlayout.addLayout(buttonsHbox)
        mainlayout.addWidget(filesteamLabel)
        mainlayout.addWidget(subWidget)

        # Others
        self.setLayout(mainlayout)
        self.scrollAreaLayoutLeft = scrollAreaLayoutLeft 
        self.scrollAreaLayoutRight = scrollAreaLayoutRight
        self.refresh_file_lists()
    def to_import(self):
        print("Landing Page : Switching to Import Images Widget")
        self.parent.setCurrentWidget(self.parent.import_image_widget)

    def to_capture(self):
        print("Landing Page : Switching to Capture Images Widget")
        self.parent.setCurrentWidget(self.parent.capture_widget)
        self.switched.emit()

    def refresh_file_lists(self):
        print("Landing Page : Refreshing Files List")
        imgs = file_processing.retrieve_img_files()
        pdfs = file_processing.retrieve_pdf_files()

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
            btn.clicked.connect(lambda _, path=new_img: file_processing.open_file(path))
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
            btn.clicked.connect(lambda _, path=new_pdf: file_processing.open_file(path))
            self.scrollAreaLayoutRight.addWidget(btn)
            self.pdf_buttons[new_pdf] = btn  # Store button reference

    def handle_file_change(self, message):
        print(message)
        QTimer.singleShot(0, self.refresh_file_lists)

    def handle_import_image(self):
        file,_ = QFileDialog.getOpenFileName(self,"Select an Image", "", "Images (*.png *.jpg .*jpeg)")
        if file:
            if not os.path.exists(file):  # Check if file exists
                QMessageBox.critical(self, "Error", "The selected file does not exist!")
                return
            else:
                print("Selected Image : ", file)
                self.parent.import_image_widget.on_mount(file)