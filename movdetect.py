import cv2 as cv
import numpy as np
vid = cv.VideoCapture('swordfish 01.mov')
height = vid.get(cv.CAP_PROP_FRAME_HEIGHT)  # always 0 in Linux python3
width = vid.get(cv.CAP_PROP_FRAME_WIDTH)  # always 0 in Linux python3
print("opencv: height:{} width:{}".format(height, width))

cv.namedWindow('Swordfish Tail Tracking', cv.WINDOW_NORMAL)
# cv.resizeWindow("Swordfish Tail Tracking", 1080, 1920)
count = 0
while vid.isOpened():
    ret, im = vid.read()
    if not ret:
        continue
    # edges = cv.Canny(frame, 50, 500)

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
    cv.imshow('Swordfish Tail Tracking', im)
    # cv.imshow('Swordfish Tail Tracking', edges)
    #cv.imwrite("frame%d.jpg" % count, frame)
    count = count + 1
    if cv.waitKey(10) & 0xFF == ord('q'):
        break

vid.release()
cv.destroyAllWindows()
