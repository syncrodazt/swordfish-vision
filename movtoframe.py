import cv2
vid = cv2.VideoCapture('swordfish 01.mov')

count = 0
output_path = "./frames0102/"
t_str = ""
is_save_time = 1
is_save_image = 0
while vid.isOpened():
    ret, frame = vid.read()
    if not ret:
        continue
    # edges = cv2.Canny(frame, 50, 500)
    # cv2.namedWindow('Swordfish Tail Tracking', cv2.WINDOW_NORMAL)
    # cv2.imshow('Swordfish Tail Tracking', edges)
    if is_save_image:
        cv2.imwrite(output_path + "frame%04d.jpg" % count, frame)
    t_str = t_str + str(vid.get(cv2.CAP_PROP_POS_MSEC)) + '\n'
    count = count + 1
    if count == 100:
        break
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

if is_save_time:
    time_name = f'{output_path + "time.txt"}'
    with open(time_name, mode='w') as f:
        f.write(t_str)

vid.release()
cv2.destroyAllWindows()
