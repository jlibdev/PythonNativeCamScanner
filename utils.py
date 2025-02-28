import os
import sys
import cv2
import numpy as np

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

    # edges = cv2.Canny(th2, 50, 150)
    # kernel = np.ones((3,3),np.uint8)
    # dilate = cv2.dilate(edges, kernel, iterations=1)
    # closing = cv2.morphologyEx(dilate, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    MIN_AREA = 5000  

    for cnt in sorted_contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA: 
            continue

        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.05 * perimeter, True)

        if len(approx) == 4 and cv2.isContourConvex(approx):  # Ensure it's convex
            x, y, w, h = cv2.boundingRect(approx)
            aspect_ratio = max(w, h) / min(w, h)  # Ensures portrait & landscape work

            # Acceptable aspect ratio range (allows squares & rectangles)
            if 0.8 <= aspect_ratio <= 2.0:  
                pages.append(approx)