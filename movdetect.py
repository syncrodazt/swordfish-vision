import cv2
import numpy as np

camera = 1; # Camera number
is_save_data = True; # Save x, y coordinates of the swordfish tail to a csv file
is_use_camera = False; # Use camera or video file
# is_resize = True; # Crop image to only show the swordfish tail
is_log = False; # Print out x, y coordinates of the swordfish tail in the terminal
is_debug = False;
filename = "swordfish 01" # Video file name
extension = ".mov" # Video file extension
resize_params = {"swordfish 01" : {"r_x": 0, "r_y": 0, "r_h": 0, "r_w": 0, "is_resize": False, "rotate": 180},
                "swordfish 02" : {"r_x": 50, "r_y": 0, "r_h": 900, "r_w": 720, "is_resize": True, "rotate": 180},
                 "swordfish 03" : {"r_x": 50, "r_y": 0, "r_h": 700, "r_w": 720, "is_resize": True, "rotate": 180},
                 "camera" : {"r_x": 50, "r_y": 0, "r_h": 1700, "r_w": 1080, "is_resize": True, "rotate": 90}}

if is_use_camera:
    locals().update(resize_params["camera"]) # Extract parameters : r_x, r_y, r_h, r_w, is_resize, rotate
else:
    locals().update(resize_params[filename]) # Extract parameters : r_x, r_y, r_h, r_w, is_resize, rotate
r_x = int(r_x)
r_y = int(r_y)
r_h = int(r_h)
r_w = int(r_w)

# Read video either from camera or file
if is_use_camera:
    vid = cv2.VideoCapture(camera)
else:
    vid = cv2.VideoCapture(filename + extension)

# Show video resolution
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)  # always 0 in Linux python3
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)  # always 0 in Linux python3
print("opencv2: height:{} width:{}".format(height, width))

# Initialize opencv windows
cv2.namedWindow("Swordfish Tail Tracking", cv2.WINDOW_NORMAL)
cv2.namedWindow("Contour", cv2.WINDOW_NORMAL)
# cv2.resizeWindow("Swordfish Tail Tracking", 1080, 1920)

count = 0
pos_str = ""
while vid.isOpened():
    ret, im = vid.read() # ret: True if frame is read correctly, im: image
    if not ret:
        break
    
    # Rotate image to make the swordfish tail face down
    if rotate == 90:
        im = cv2.rotate(im, cv2.ROTATE_90_CLOCKWISE)
    elif rotate == 180:
        im = cv2.rotate(im, cv2.ROTATE_180)
        
    # Crop image so that only the swordfish tail is visible
    if is_resize:
        if is_debug:
            print(f"r_x: {r_x}, r_y: {r_y}, r_h: {r_h}, r_w: {r_w}")
        im = im[r_y: (r_y + r_h), r_x: (r_x + r_w)]
        

    im_contour = im.copy() # Copy image for contour
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    edges = cv2.Canny(imgray, 50, 200) # Detect edges using Canny
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE) # Draw contours from edges detected
    cv2.drawContours(im_contour, contours, -1, (0, 255, 0), 3)
    cv2.imshow("Contour", im_contour) # Show contour image
    
    contour_maxs = [] # Initialize array to store x, y coordinates of the swordfish tail
    for i, x in enumerate(contours):
        xnp = np.array(x)
        xnp = np.resize(xnp, (xnp.shape[0], 2))
        maxindex = np.argmax(xnp, axis=0)
        temp_endpos = xnp[maxindex[1]]
        contour_maxs.append(temp_endpos)
        if is_log:
            print(f"frame = {i}, x: {temp_endpos[0]}, y: {temp_endpos[1]}")
        # cv2.circle(im, temp_endpos, radius=1, color=(0, 0, 255), thickness=5)
        
    contour_maxs = np.array(contour_maxs)
    maxindex = np.argmax(contour_maxs, axis=0)
    endpos = contour_maxs[maxindex[1]]
    
    pos_str = pos_str+f"{endpos[0]}, {endpos[1]}"+"\n" # Append x, y coordinates to a string for csv file
    
    # Draw dot and line on the swordfish tail
    cv2.circle(im, endpos, radius=1, color=(0, 0, 255), thickness=5)
    cv2.line(im, (0, endpos[1]), (endpos[0], endpos[1]), (0, 0, 255), 1)
    cv2.line(im, (endpos[0], 0), (endpos[0], endpos[1]), (0, 0, 255), 1)
    cv2.putText(im, str(endpos), (endpos[0], endpos[1]-10),
               cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Swordfish Tail Tracking", im)
    
    # cv2.imshow('Swordfish Tail Tracking', edges)
    #cv2.imwrite("frame%d.jpg" % count, frame)
    count = count + 1
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

if is_save_data:
    with open(f'{filename}.csv', 'w') as f:
        f.write(pos_str)

vid.release()
cv2.destroyAllWindows()
