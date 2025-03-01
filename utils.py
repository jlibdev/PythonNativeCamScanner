import os, mimetypes
import sys
import cv2
import numpy as np
from PyQt6.QtGui import QPixmap, QImage
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
from PyQt6.QtCore import QThread, pyqtSignal, QObject

def resource_path(relative_path):
    """ Get the absolute path to a resource, compatible with PyInstaller. """
    if getattr(sys, 'frozen', False):  # Check if running as an executable
        base_path = sys._MEIPASS  # Temporary folder for PyInstaller
    else:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_all_pages(frame, pages):

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    _, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    edges = cv2.Canny(th2, 50, 150)
    kernel = np.ones((3,3),np.uint8)
    dilate = cv2.dilate(edges, kernel, iterations=1)
    closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)

    # frame = cv2.resize(frame, (widthImg, heightImg))  # RESIZE IMAGE
    # imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # CONVERT IMAGE TO GRAY SCALE
    # imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 1)  # ADD GAUSSIAN BLUR
    # imgThreshold = cv2.Canny(imgBlur, 255, 255)  # APPLY CANNY BLUR
    # kernel = np.ones((5, 5), np.uint8)
    # imgDial = cv2.dilate(imgThreshold, kernel, iterations=1)  # APPLY DILATION
    # imgThreshold = cv2.erode(imgDial, kernel, iterations=1)  # APPLY EROSION
    # closing = cv2.morphologyEx(imgThreshold, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    MIN_AREA = 5000  

    for cnt in sorted_contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA: 
            continue

        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.05 * perimeter, True)

        if len(approx) == 4 and cv2.isContourConvex(approx):  # Ensure it's convex
            # x, y, w, h = cv2.boundingRect(approx)
            pages.append(approx)


def cv2_to_pixmap(cv_image):
    """Convert OpenCV image (BGR NumPy array) to QPixmap."""
    height, width, channel = cv_image.shape
    bytes_per_line = channel * width
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(q_image)







# Function to open a file
def open_file(file_path):
    if os.path.exists(file_path):
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(["xdg-open", file_path], check=True)
    else:
        print("File not found:", file_path)


def retrieve_img_files():
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Construct paths
    image_camscanner_path = os.path.join(home_dir, "Documents", "camscanner_files", "images")

    # Create folder if it doesn’t exist
    os.makedirs(image_camscanner_path, exist_ok=True)

    # Function to check if a file is a JPEG or PNG
    def is_image(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type in ["image/jpeg", "image/png"]

    # Retrieve all JPEG and PNG files
    img_files = [
        os.path.join(image_camscanner_path, f)
        for f in os.listdir(image_camscanner_path)
        if is_image(os.path.join(image_camscanner_path, f))
    ]

    return img_files 

def retrieve_pdf_files():
    # Get the user's home directory
    home_dir = os.path.expanduser("~")

    # Construct paths
    pdf_camscanner_path = os.path.join(home_dir, "Documents", "camscanner_files", "pdf")
    
    # Create folder if it doesn’t exist
    os.makedirs(pdf_camscanner_path, exist_ok=True)

    def is_pdf(file_path):
        mime_type, _ = mimetypes.guess_type(file_path)
        return mime_type == "application/pdf"

    pdf_files = [
        os.path.join(pdf_camscanner_path, f)
        for f in os.listdir(pdf_camscanner_path)
        if is_pdf(os.path.join(pdf_camscanner_path, f))
    ]

    return pdf_files

# Function to open a file
def open_file(file_path):
    if os.path.exists(file_path):
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS/Linux
            subprocess.run(["xdg-open", file_path], check=True)
    else:
        print("File not found:", file_path)



