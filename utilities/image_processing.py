import cv2
import numpy as np

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




