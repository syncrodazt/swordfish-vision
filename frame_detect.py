# import cv2
# i = cv2.imread('frames0102/frame0001.jpg', cv2.IMREAD_GRAYSCALE)
# cv2.imshow('test', i)
# cv2.waitKey(0)

import numpy as np
import cv2 as cv
im = cv.imread('frames0102/frame0001.jpg')
im_contour = im.copy()
imgray = cv.cvtColor(im, cv.COLOR_BGR2GRAY)
edges = cv.Canny(imgray, 50, 200)
contours, hierarchy = cv.findContours(
    edges, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
cv.drawContours(im_contour, contours, -1, (0, 255, 0), 3)
maxs = []
for i, x in enumerate(contours):
    print(i)
    xnp = np.array(x)
    xnp = np.resize(xnp, (xnp.shape[0], 2))
    maxindex = np.argmax(xnp, axis=0)
    temp = xnp[maxindex[1]]
    print(temp)
    maxs.append(temp)
    # cv.circle(im, temp, radius=1, color=(0, 0, 255), thickness=5)
maxsnp = np.array(maxs)
maxindex = np.argmax(maxsnp, axis=0)
temp = maxsnp[maxindex[1]]
# cv.circle(im, temp, radius=1, color=(0, 0, 255), thickness=5)
cv.circle(im, temp, radius=1, color=(0, 0, 255), thickness=5)
cv.line(im, (0, temp[1]), (temp[0], temp[1]), (0, 0, 255), 1)
cv.line(im, (temp[0], 0), (temp[0], temp[1]), (0, 0, 255), 1)
cv.putText(im, str(temp), (temp[0], temp[1]-10),
           cv.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
cv.imshow('test', im)
cv.waitKey(0)

# print(contours)
