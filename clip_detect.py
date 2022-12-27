import cv2
import numpy as np
import os
from fn_detect import fn_detect

camera = 1; # Camera number
is_save_data = True; # Save x, y coordinates of the swordfish tail to a csv file
is_save_vid = True; # Save video with the swordfish tail detected
is_use_camera = False; # Uase camera or video file
# is_resize = True; # Crop image to only show the swordfish tail
is_log_fn = False; # Print out x, y coordinates of the swordfish tail in the terminal
is_debug = False;
is_show = True;
input_folder = "input"
filenames = ["testing 01", "testing 02", "testing 03", "testing 04", "testing 05"]
# filenames = ["testing 01 cut"]
for filename in filenames:
    # filename = "testing 01 cut" # Video file name
    print(f"filename: {filename}")
    extension = ".mov" # Video file extension
    output_folder = filename
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

    # Initialize video writer
    if is_save_vid:
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out_contour = cv2.VideoWriter(f'{filename}_contour.mp4', fourcc, 30.0, (int(width), int(height)))
        out_cm = cv2.VideoWriter(f'{filename}_cm.mp4', fourcc, 30.0, (int(width), int(height)))

    # Rotate and crop parameters
    # r_x: x coordinate of the top left corner of the cropped image
    # r_y: y coordinate of the top left corner of the cropped image
    # r_h: height of the cropped image
    # r_w: width of the cropped image
    params = {"swordfish 01" : {"rotate": 180, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": height, "r_w": width, "rotation_center" : [560, 89], "cm_px": [9.8, 900]},
            "swordfish 02" : {"rotate": 180, "is_resize": True, "r_x": 50, "r_y": 0, "r_h": 900, "r_w": 720, "rotation_center" : [560, 89], "cm_px": [9.8, 900]},
            "swordfish 03" : {"rotate": 180, "is_resize": True, "r_x": 50, "r_y": 0, "r_h": 700, "r_w": 720, "rotation_center" : [560, 89], "cm_px": [9.8, 900]},
            "swordfish 04" : {"rotate": 0, "is_resize": True, "r_x": 0, "r_y": 0, "r_h": 1850, "r_w": 900, "rotation_center" : [560, 89], "cm_px": [9.8, 900]},
            "swordfish 05" : {"rotate": 180, "is_resize": True, "r_x": 0, "r_y": 0, "r_h": 1850, "r_w": 900, "rotation_center" : [560, 89], "cm_px": [9.8, 900]},
            "swordfish 06" : {"rotate": 180, "is_resize": True, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [560, 89], "cm_px": [9.8, 900]},
            "swordfish 07" : {"rotate": 180, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [560, 89], "cm_px": [9.8, 900]},
            "swordfish 08" : {"rotate": 0, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [560, 250], "cm_px": [9.8, 696]},
            "testing 01" : {"rotate": 0, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [542, 358], "cm_px": [9.8, 1075]},
            "testing 01 cut" : {"rotate": 0, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [542, 358], "cm_px": [9.8, 1075]},
            "testing 02" : {"rotate": 0, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [542, 358], "cm_px": [9.8, 1075]},
            "testing 03" : {"rotate": 0, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [542, 358], "cm_px": [9.8, 1075]},
            "testing 04" : {"rotate": 0, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [542, 358], "cm_px": [9.8, 1075]},
            "testing 05" : {"rotate": 0, "is_resize": False, "r_x": 0, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [542, 358], "cm_px": [9.8, 1075]},
            "camera" : {"rotate": 270, "is_resize": True, "r_x": 100, "r_y": 0, "r_h": 1920, "r_w": 1080, "rotation_center" : [560, 89], "cm_px": [9.8, 900]}}
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
    endpos_px_str = ""
    origin_cm_str = ""

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
            
        # Detect the swordfish tail position
        im_contour, im, endpos_px, origin_cm = fn_detect(im, count=count, is_log_fn=is_log_fn, is_show=is_show, param=params[filename], save_param=save_param)
        
        # Save images to a video
        # print(f"im_contour.shape = {im_contour.shape}")
        # print(f"im_cm.shape = {im.shape}")
        if is_save_vid:
            out_contour.write(im_contour)
            out_cm.write(im)
        
        # Append x, y coordinates to a string for csv file
        endpos_px_str = endpos_px_str+f"{endpos_px[0]}, {endpos_px[1]}"+"\n" # Append x, y coordinates to a string for csv file
        origin_cm_str = origin_cm_str+f"{origin_cm[0]}, {origin_cm[1]}"+"\n" # Append x, y coordinates to a string for csv file
        
        # if count == 0:
        #     # cv2.waitKey(100)
        #     cv2.waitKey(10000)
            
        count = count + 1
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    if is_save_data:
        with open(f'{filename}_endpos_px.csv', 'w') as f:
            f.write(endpos_px_str)
        with open(f'{filename}_origin_cm.csv', 'w') as f:
            f.write(origin_cm_str)

    vid.release()
    out_contour.release()
    out_cm.release()
    cv2.destroyAllWindows()
