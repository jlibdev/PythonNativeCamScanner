import cv2
import numpy as np
from PyQt6.QtGui import QImage , QPixmap

def get_contours_cv(frame):

    valid_contours = []

    display_frame = frame.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY, 11, 2)

    kernel = np.ones((3,3), np.uint8)
    closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    MIN_AREA = 5000 

    for cnt in sorted_contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA:
            continue

        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)

        if len(approx) == 4 and cv2.isContourConvex(approx):
            x, y, w, h = cv2.boundingRect(approx)
            bounding_rect_area = w * h
            aspect_ratio = w / float(h)

            if 0.8 <= aspect_ratio <= 1.2 or bounding_rect_area * 0.8 <= area <= bounding_rect_area * 1.2:
                valid_contours.append(approx)

    print("Pages detected:", len(valid_contours))
    if not valid_contours:
        print("⚠️ No valid pages detected!")
    
    for page in valid_contours:
                    cv2.drawContours(display_frame, [page], -1, (0, 255, 0), 3) 

    return display_frame , valid_contours
    

def get_contours(imgdir):

    MIN_AREA = 5000

    valid_contours = []

    image = cv2.imread(imgdir)

    image_original = image.copy()

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, 50, 150)

    kernel = np.ones((3,3),np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
    contours, _ = cv2.findContours(closing, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)
    for cnt in sorted_contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA: 
            continue
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)

        if len(approx) == 4 and cv2.isContourConvex(approx): 
            valid_contours.append(approx)

    for page in valid_contours:
            cv2.drawContours(image, [page], -1, (0, 255, 0), 3) 

    return image_original, image, valid_contours


def cv2_to_pixmap(cv_image):
    height, width, channel = cv_image.shape
    bytes_per_line = channel * width
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
    q_image = QImage(cv_image.data, width, height, bytes_per_line, QImage.Format.Format_RGB888)
    return QPixmap.fromImage(q_image)



def cv2_to_QImage(frame, format_type=QImage.Format.Format_RGB888):
    if len(frame.shape) == 2:
        height, width = frame.shape
        bytes_per_line = width
        return QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_Grayscale8)
    else: 
        height, width, channels = frame.shape
        bytes_per_line = channels * width
        return QImage(frame.data, width, height, bytes_per_line, format_type)