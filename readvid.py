import cv2
vid = cv2.VideoCapture('swordfish 01.mov')
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)  # always 0 in Linux python3
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)  # always 0 in Linux python3
print("opencv: height:{} width:{}".format(height, width))

count = 0
while vid.isOpened():
    ret, frame = vid.read()
    if not ret:
        continue
    edges = cv2.Canny(frame, 50, 500)
    cv2.namedWindow('Swordfish Tail Tracking', cv2.WINDOW_NORMAL)
    cv2.imshow('Swordfish Tail Tracking', edges)
    #cv2.imwrite("frame%d.jpg" % count, frame)
    count = count + 1
    if count == 10:
        break
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

vid.release()
cv2.destroyAllWindows()
