# import cv2
# import numpy as np


# def preprocess_image(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     blurred = cv2.GaussianBlur(gray, (5,5), 0)
#     thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11 , 2)

#     return thresh

# def get_edges(thresh):
#     edges = cv2.Canny(thresh, 50 ,150)
#     return edges

# def find_contour(edges):
#     cnt, _ = cv2.findContours(edges , cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#     cnt = sorted(cnt, key=cv2.contourArea, reverse=True)

#     for c in cnt:
#         epsilon = 0.02 * cv2.arcLength(c, True)
#         approx = cv2.approxPolyDP(c, epsilon, True)

#         if len(approx) == 4:
#             return approx
#     return None


# def warp(image , contour):
#     pts = np.array(contour, dtype="float32")
#     rect = np.array(sorted(pts, key=lambda x: x[0][0] + x[0][1]))
#     (tl,tr,br,bl) = rect[:,0]

#     w = max(np.linalg.norm(br-bl), np.linalg.norm(tr-tl))
#     h = max(np.linalg.norm(tr-br), np.linalg.norm(tl-bl))

#     dst = np.array([[0,0], [w-1,0], [w-1, h-1], [0, h-1]], dtype="float32")

#     M =  cv2.getPerspectiveTransform(pts, dst)

#     warp = cv2.warpPerspective(image, M , (int(w), int(h)))

#     return warp

# image = cv2.imread(r"C:\Users\Joshua Libando\Dropbox\PC\Documents\IMG20240314170018.jpg")

# t = preprocess_image(image)

# e = get_edges(t)

# c = find_contour(e)

# cv2.drawContours(image, [c], -1, (0, 255, 0), 3)

# cv2.imshow("" , image)
# cv2.waitKey(0)
# cv2.destroyAllWindows()




from PyQt6.QtWidgets import QWidget, QHBoxLayout , QVBoxLayout, QLabel, QPushButton , QSizePolicy , QScrollArea , QFileDialog, QMessageBox, QApplication
import sys
from PyQt6.QtGui import QIcon , QImage , QPixmap
from PyQt6.QtCore import Qt , QSize , QTimer , pyqtSignal, Qt, QThread 
import cv2
import numpy as np
from components.bigbuttons import ImageNavButton

import sys
from PyQt6.QtWidgets import QApplication, QStackedWidget , QPushButton
from PyQt6.QtGui import QFontDatabase , QFont, QIcon
import stackwidgets.LandingWidget
from stackwidgets.Widgets import  CaptureWidget, EditImageWidget
import treads.Watchers
from utils import resource_path, save_path
import treads
import stackwidgets

        
# app = QApplication(sys.argv)

# font_id = QFontDatabase.addApplicationFont(resource_path("fonts/Jura-VariableFont_wght.ttf"))

# if font_id != -1:
#         font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
#         app.setFont(QFont(font_family, 12)) 

# window = ImportImageWidget()


# window.show()
# sys.exit(app.exec())



import cv2
import numpy as np
from skimage.filters import threshold_local

# Load image
image = cv2.imread(r"C:\Users\Joshua Libando\Dropbox\PC\Documents\IMG20240314140042.jpg")

# Convert to HSV and extract the Value (V) channel
V = cv2.split(cv2.cvtColor(image, cv2.COLOR_BGR2HSV))[2]

# Apply adaptive thresholding using skimage
T = threshold_local(V, 25, offset=15, method="gaussian")
thresh = (V > T).astype("uint8") * 255  # Convert to binary image

# Find contours
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Ensure at least one contour is found
if contours:
    # Get the largest contour by area
    largest_contour = max(contours, key=cv2.contourArea)

    # Draw the largest contour on the original image
    contour_img = image.copy()
    cv2.drawContours(contour_img, [largest_contour], -1, (0, 255, 0), 2)  # Green contour

    # Display results
    cv2.imshow("Thresholded", thresh)
    cv2.imshow("Largest Contour", contour_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:
    print("No contours found!")
