import cv2
import numpy as np

def get_contours(imgdir):

    MIN_AREA = 5000

    valid_contours = []

    image = cv2.imread(imgdir)

    image_original = image.copy()

    # Convert to Grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # blur = 

    _, th2 = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(th2, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    sorted_contours = sorted(contours, key=cv2.contourArea, reverse=True)

    for cnt in sorted_contours:
        area = cv2.contourArea(cnt)
        if area < MIN_AREA: 
            continue
        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.05 * perimeter, True)

        if len(approx) == 4 and cv2.isContourConvex(approx): 
            valid_contours.append(approx)

    for page in valid_contours:
            cv2.drawContours(image, [page], -1, (0, 255, 0), 3) 

    return image_original, image , contours




