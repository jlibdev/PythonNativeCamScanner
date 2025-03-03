import cv2
import numpy as np

def get_contours_sir(imgdir):

    image = cv2.imread(imgdir)

    image_original = image.copy()

    # Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Use a copy of your image e.g. edged.copy(), since findContours alters the image
    contours, hierarchy = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Draw all contours, note this overwrites the input image (inplace operation)
    # Use '-1' as the 3rd parameter to draw all
    cv2.drawContours(image, contours, -1, (0,255,0), thickness = 2)

    return image_original, image , contours

# def get_contours(imgdir):
