import cv2
import numpy as np
import os
from fn_detect import fn_detect

camera = 1; # Camera number
is_save_data = False; # Save x, y coordinates of the swordfish tail to a csv file
is_use_camera = False; # Uase camera or video file
# is_resize = True; # Crop image to only show the swordfish tail
is_log = False; # Print out x, y coordinates of the swordfish tail in the terminal
is_debug = False;
input_folder = "input"
filename = "swordfish 08" # Video file name
extension = ".mov" # Video file extension
output_folder = "output"
save_param = {"is_save": False,
              "filename": filename,
              "extension": ".png",
              "output_folder": output_folder}

# Read video either from camera or file
if is_use_camera:
    vid = cv2.VideoCapture(camera)
else:
    vid = cv2.VideoCapture(os.path.join(input_folder, filename + extension))
    
# Show video resolution
height = vid.get(cv2.CAP_PROP_FRAME_HEIGHT)  # always 0 in Linux python3
width = vid.get(cv2.CAP_PROP_FRAME_WIDTH)  # always 0 in Linux python3
print("opencv2: height:{} width:{}".format(height, width))

# Rotate and crop parameters
# r_x: x coordinate of the top left corner of the cropped image
# r_y: y coordinate of the top left corner of the cropped image
# r_h: height of the cropped image
# r_w: width of the cropped image
params = {"swordfish 01" : {"rotate": 180, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": height, "r_w": width},
        "swordfish 02" : {"rotate": 180, "is_resize": True, "r_x": 50, "r_y": 0, "r_h": 900, "r_w": 720},
        "swordfish 03" : {"rotate": 180, "is_resize": True, "r_x": 50, "r_y": 0, "r_h": 700, "r_w": 720},
        "swordfish 04" : {"rotate": 0, "is_resize": True, "r_x": 0, "r_y": 0, "r_h": 1850, "r_w": 900},
        "swordfish 05" : {"rotate": 180, "is_resize": True, "r_x": 0, "r_y": 0, "r_h": 1850, "r_w": 900},
        "swordfish 06" : {"rotate": 180, "is_resize": True, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080},
        "swordfish 07" : {"rotate": 180, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080},
        "swordfish 08" : {"rotate": 180, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080},
        "camera" : {"rotate": 270, "is_resize": True, "r_x": 100, "r_y": 0, "r_h": 1920, "r_w": 1080}}
        # "camera" : {"rotate": 270, "is_resize": True, "r_x": 100, "r_y": 0, "r_h": 1080, "r_w": 1920}}

if is_use_camera:
    locals().update(params["camera"]) # Extract parameters : r_x, r_y, r_h, r_w, is_resize, rotate
else:
    locals().update(params[filename]) # Extract parameters : r_x, r_y, r_h, r_w, is_resize, rotate
r_x = int(r_x)
r_y = int(r_y)
r_h = int(r_h)
r_w = int(r_w)

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
    elif rotate == 270:
        im = cv2.rotate(im, cv2.ROTATE_90_COUNTERCLOCKWISE)
        
    # Crop image so that only the swordfish tail is visible
    if is_resize:
        if is_debug:
            print(f"r_x: {r_x}, r_y: {r_y}, r_h: {r_h}, r_w: {r_w}")
        im = im[r_y: (r_y + r_h), r_x: (r_x + r_w)]
        

    endpos = fn_detect(im, is_log=False, param=params[filename], save_param=save_param)
    pos_str = pos_str+f"{endpos[0]}, {endpos[1]}"+"\n" # Append x, y coordinates to a string for csv file
    
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
