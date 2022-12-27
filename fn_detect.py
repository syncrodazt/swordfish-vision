import cv2
import numpy as np
import os

def fn_detect(im, count, is_log_fn, is_show, param, save_param):
    rotation_center = param["rotation_center"]
    # known_cm = 9.8 # cm
    # # known_pixel = 639 # pixel
    # known_pixel = 900 # pixel
    cm_px = param["cm_px"]
    px2cm = cm_px[0]/cm_px[1]
    r_x = param["r_x"]
    r_y = param["r_y"]
    r_h = param["r_h"]
    r_w = param["r_w"]
    
    # Initialize opencv windows
    if is_show:
        WINDOW_SCALE = 0.7
        cv2.namedWindow("Swordfish Tail Tracking", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Swordfish Tail Tracking", int((r_w-r_x)*WINDOW_SCALE), int((r_h-r_y)*WINDOW_SCALE))
        cv2.namedWindow("Contour", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Contour", int((r_w-r_x)*WINDOW_SCALE), int((r_h-r_y)*WINDOW_SCALE))
        # cv2.resizeWindow("Swordfish Tail Tracking", 1080, 1920)

    # Contour crop
    c_x = 50;
    c_y = 1400;
    c_h = r_h-c_y-50;
    c_w = r_w-c_x-50;
    im_contour = im.copy() # Copy image for contour
    im_contour_crop = im.copy() # Copy image for contour
    im_contour_crop = im_contour_crop[c_y:c_y+c_h, c_x:c_x+c_w, :] # Crop image for contour
    im_contour_crop_gray = cv2.cvtColor(im_contour_crop, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    ret, im_contour_crop_gray_binary = cv2.threshold(im_contour_crop, 185, 255, cv2.THRESH_BINARY) # Convert to grayscale
    # cv2.imshow("Binary", im_contour_crop_gray_binary)
    # im_contour_crop_gray_threshold = cv2.adaptiveThreshold(im_contour_crop_gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 20) # Convert to grayscale
    # cv2.imshow("Gray", im_contour_crop_gray_threshold) # Show contour image
    
    # im_contour_crop_gray_edges = cv2.merge((im_contour_crop_gray_edges, im_contour_crop_gray_edges, im_contour_crop_gray_edges))
    # print(f"shape = {im_contour_crop_gray_edges.shape}")
    
    im_contour_crop_gray_edges = cv2.Canny(im_contour_crop_gray_binary, 50, 200) # Detect edges using Canny
    # cv2.imshow("Edge", im_contour_crop_gray_edges) # Show contour image
    # cv2.waitKey(10000)
    
    contours, hierarchy = cv2.findContours(
        im_contour_crop_gray_edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE ) # Draw contours from edges detected
    cv2.drawContours(im_contour_crop, contours, -1, (0, 255, 255), 3)
    im_contour[c_y:c_y+c_h, c_x:c_x+c_w, :] = im_contour_crop
    if is_show:
        # Draw rectangle of contour crop
        cv2.rectangle(im_contour, [c_x, c_y], [c_x+c_w, c_y+c_h], (0, 255, 255), 2)
        cv2.imshow("Contour", im_contour) # Show contour image
    # cv2.waitKey(10000)
    
    contour_maxs = [] # Initialize array to store x, y coordinates of the swordfish tail
    for i, x in enumerate(contours):
        xnp = np.array(x)
        xnp = np.resize(xnp, (xnp.shape[0], 2))
        maxindex = np.argmax(xnp, axis=0)
        temp_endpos = xnp[maxindex[1]]
        contour_maxs.append(temp_endpos)
        if is_log_fn:
            print(f"frame = {i}, x: {temp_endpos[0]}, y: {temp_endpos[1]}")
        
    contour_maxs = np.array(contour_maxs)
    maxindex = np.argmax(contour_maxs, axis=0)
    endpos = contour_maxs[maxindex[1]]
    endpos = [endpos[0]+c_x, endpos[1]+c_y]
    
    
    # # Draw dot and line on the swordfish tail
    
    FONT_THICKNESS = 2
    FONT_SCALE = 1.
    2
    FONT_FAM = cv2.FONT_HERSHEY_SIMPLEX
    cv2.circle(im, endpos, radius=1, color=(0, 0, 255), thickness=5)

    cv2.circle(im, rotation_center, radius=1, color=(0, 0, 255), thickness=5)

    cv2.line(im, rotation_center, endpos, (0, 255, 0), 2) # Draw line from rotation center to endpos
    cv2.line(im, endpos, [rotation_center[0], endpos[1]], (255, 0, 0), 2) # Draw projective horizontal line
    cv2.line(im, rotation_center, [rotation_center[0], endpos[1]], (255, 0, 0), 2) # Draw projective vertical line
    # Draw text at middle of the projective horizontal line
    x_origin = endpos[0]-rotation_center[0] # x position from rotation center to endpos
    y_origin = endpos[1]-rotation_center[1] # y position from rotation center to endpos


    h_start = np.array([0, endpos[1]])
    h_end = np.array([endpos[0], endpos[1]])
    v_start = np.array([endpos[0], 0])
    v_end = np.array([endpos[0], endpos[1]])
    cv2.line(im, h_start, h_end, (0, 0, 255), 2) # Draw horizontal line
    cv2.line(im, v_start, v_end, (0, 0, 255), 2) # Draw vertical line
    text_pos_ab = (10, r_h-15)
    text_pos_xy = (10, r_h-60)

    cv2.putText(im, f"[a, b] = [{endpos[0]} {endpos[1]}] [pixel] = [{endpos[0]*px2cm:.2f} {endpos[1]*px2cm:.2f}] [cm]" , text_pos_ab, FONT_FAM, FONT_SCALE, (0, 0, 255), FONT_THICKNESS)
    cv2.putText(im, "a", (int(endpos[0]/2), endpos[1]-10), FONT_FAM, FONT_SCALE, (0, 0, 255), FONT_THICKNESS)
    cv2.putText(im, "b", (endpos[0]-25, int(endpos[1]/2)), FONT_FAM, FONT_SCALE, (0, 0, 255), FONT_THICKNESS)
    
    cv2.putText(im, f"[x, y] = [{x_origin} {y_origin}] [pixel] = [{x_origin*px2cm:.2f} {y_origin*px2cm:.2f}] [cm]" , text_pos_xy, FONT_FAM, FONT_SCALE, (255, 0, 0), FONT_THICKNESS)
    cv2.putText(im, "x", (int(endpos[0]+(rotation_center[0]-endpos[0])/2), endpos[1]-10), FONT_FAM, FONT_SCALE, (255, 0, 0), FONT_THICKNESS)
    cv2.putText(im, "y", (rotation_center[0]-25, int(rotation_center[1]+(endpos[1]-rotation_center[1])/2)), FONT_FAM, FONT_SCALE, (255, 0, 0), FONT_THICKNESS)
    

    
    if is_show:
        cv2.imshow("Swordfish Tail Tracking", im)
    
    if save_param["is_save"]:
        output_folder = save_param["output_folder"]
        filename = save_param["filename"]
        extension = save_param["extension"]
        cv2.imwrite(os.path.join(output_folder, filename + f"_contour_{count:05d}" + extension), im_contour)
        cv2.imwrite(os.path.join(output_folder, filename + f"_tracking_{count:05d}" + extension), im)
    return im_contour, im, endpos, [x_origin*px2cm, y_origin*px2cm]