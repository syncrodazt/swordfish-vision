# import cv2
# i = cv2.imread('frames0102/frame0001.jpg', cv2.IMREAD_GRAYSCALE)
# cv2.imshow('test', i)
# cv2.waitKey(0)

import numpy as np
import cv2
import os
from fn_detect import fn_detect

is_log = False

input_folder = "input"
output_folder = "output"
filename = "swordfish 01" # Video file name
extension = ".png" # Video file extension
save_param = {"is_save": True,
              "filename": filename,
              "extension": extension,
              "output_folder": output_folder}

# im = cv2.imread("frames/frames0102/frame0001.jpg")
im = cv2.imread(os.path.join(input_folder, filename + extension))
height, width, _ = im.shape

params = {"swordfish 01" : {"rotate": 180, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": height, "r_w": width},
        "swordfish 02" : {"rotate": 180, "is_resize": True, "r_x": 50, "r_y": 0, "r_h": 900, "r_w": 720},
        "swordfish 03" : {"rotate": 180, "is_resize": True, "r_x": 50, "r_y": 0, "r_h": 700, "r_w": 720},
        "swordfish 04" : {"rotate": 0, "is_resize": True, "r_x": 0, "r_y": 0, "r_h": 1850, "r_w": 900},
        "swordfish 05" : {"rotate": 180, "is_resize": True, "r_x": 0, "r_y": 0, "r_h": 1850, "r_w": 900},
        "camera" : {"rotate": 90, "is_resize": True, "r_x": 50, "r_y": 0, "r_h": 1700, "r_w": 1080}}


locals().update(params[filename]) # Extract parameters : r_x, r_y, r_h, r_w, is_resize, rotate
r_x = int(r_x)
r_y = int(r_y)
r_h = int(r_h)
r_w = int(r_w)


WINDOW_SCALE = 0.7
print(height, width)

im_contour = im.copy()

# Convert to grayscale
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
_, imgray = cv2.threshold(imgray, 128, 192, cv2.THRESH_OTSU)
cv2.namedWindow("Imgray", cv2.WINDOW_NORMAL)
cv2.imshow("Imgray", imgray)
cv2.resizeWindow("Imgray", int(width*WINDOW_SCALE), int(height*WINDOW_SCALE))

# Canny edge detection
edges = cv2.Canny(imgray, 5, 200)
cv2.namedWindow("Canny", cv2.WINDOW_NORMAL)
cv2.imshow("Canny", edges)
cv2.resizeWindow("Canny", int(width*WINDOW_SCALE), int(height*WINDOW_SCALE))
cv2.imwrite(os.path.join(output_folder, filename + "_edges" + extension), edges)

contours, hierarchy = cv2.findContours(
    edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
print(f"contours: {len(contours)}")
# for contour_idx, contour in enumerate(contours):
#     cv2.drawContours(im_contour, contour, -1, (0, 255, 0), 3)
#     cv2.imshow(f"Contour {contour_idx}", im_contour)
#     cv2.resizeWindow(f"Contour {contour_idx}", int(width*WINDOW_SCALE), int(height*WINDOW_SCALE))


endpos = fn_detect(im, is_log=False, param=params[filename], save_param=save_param)


cv2.waitKey(0)
cv2.destroyAllWindows()