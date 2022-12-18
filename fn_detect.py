import cv2
import numpy as np
import os

def fn_detect(im, is_log, param, save_param):
    r_x = param["r_x"]
    r_y = param["r_y"]
    r_h = param["r_h"]
    r_w = param["r_w"]
    
    # Initialize opencv windows
    WINDOW_SCALE = 1
    # cv2.namedWindow("Swordfish Tail Tracking", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Swordfish Tail Tracking", int((r_w-r_x)*WINDOW_SCALE), int((r_h-r_y)*WINDOW_SCALE))
    # cv2.namedWindow("Contour", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Contour", int((r_w-r_x)*WINDOW_SCALE), int((r_h-r_y)*WINDOW_SCALE))
    # cv2.resizeWindow("Swordfish Tail Tracking", 1080, 1920)

    
    im_contour = im.copy() # Copy image for contour
    imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) # Convert to grayscale
    edges = cv2.Canny(imgray, 100, 200) # Detect edges using Canny
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
        
    contour_maxs = np.array(contour_maxs)
    maxindex = np.argmax(contour_maxs, axis=0)
    endpos = contour_maxs[maxindex[1]]
    
    
    
    # # Draw dot and line on the swordfish tail
    # cv2.circle(im, endpos, radius=1, color=(0, 0, 255), thickness=5)
    # cv2.line(im, (0, endpos[1]), (endpos[0], endpos[1]), (0, 0, 255), 1) # Draw vertical line
    # cv2.line(im, (endpos[0], 0), (endpos[0], endpos[1]), (0, 0, 255), 1) # Draw horizontal line
    # # text_pos = (endpos[0], endpos[1]-10)
    # text_pos = (10, int(r_h)-10)
    # cv2.putText(im, str(endpos), text_pos,
    #         FONT_FAM, 1, (255, 0, 0), 2)
    
    FONT_THICKNESS = 2
    FONT_SCALE = 0.7
    FONT_FAM = cv2.FONT_HERSHEY_SIMPLEX
    cv2.circle(im, endpos, radius=1, color=(0, 0, 255), thickness=5)

    # rotation_center = [466, 929] # Define rotation center from the image
    rotation_center = [560, 89] # Define rotation center from the image
    cv2.circle(im, rotation_center, radius=1, color=(0, 0, 255), thickness=5)

    cv2.line(im, rotation_center, endpos, (0, 255, 0), 2) # Draw line from rotation center to endpos
    cv2.line(im, endpos, [rotation_center[0], endpos[1]], (255, 0, 0), 2) # Draw projective horizontal line
    cv2.line(im, rotation_center, [rotation_center[0], endpos[1]], (255, 0, 0), 2) # Draw projective vertical line
    # Draw text at middle of the projective horizontal line
    x_origin = endpos[0]-rotation_center[0] # x position from rotation center to endpos
    y_origin = endpos[1]-rotation_center[1] # y position from rotation center to endpos
    # cv2.putText(im, f"[x_origin, y_origin] = [{x_origin} {y_origin}]", (rotation_center[0], endpos[1]), FONT_FAM, FONT_SCALE, (255, 0, 0), FONT_THICKNESS)


    h_start = np.array([0, endpos[1]])
    h_end = np.array([endpos[0], endpos[1]])
    v_start = np.array([endpos[0], 0])
    v_end = np.array([endpos[0], endpos[1]])
    cv2.line(im, h_start, h_end, (0, 0, 255), 2) # Draw horizontal line
    cv2.line(im, v_start, v_end, (0, 0, 255), 2) # Draw vertical line
    # text_pos = (endpos[0], endpos[1]-10)
    text_pos = (10, r_h-15)
    text_pos2 = (10, r_h-60)

    known_cm = 5.8 # cm
    known_pixel = 212.0478 # pixel
    px2cm = known_cm / known_pixel
    cv2.putText(im, f"[x, y] = [{endpos[0]} {endpos[1]}] [pixel] = [{endpos[0]*px2cm:.2f} {endpos[1]*px2cm:.2f}] [cm]" , text_pos, FONT_FAM, FONT_SCALE, (0, 0, 255), FONT_THICKNESS)
    cv2.putText(im, "x", (int(endpos[0]/2), endpos[1]-10), FONT_FAM, FONT_SCALE, (0, 0, 255), FONT_THICKNESS)
    cv2.putText(im, "y", (endpos[0]-20, int(endpos[1]/2)), FONT_FAM, FONT_SCALE, (0, 0, 255), FONT_THICKNESS)
    
    cv2.putText(im, f"[x_origin, y_origin] = [{x_origin} {y_origin}] [pixel] = [{x_origin*px2cm:.2f} {y_origin*px2cm:.2f}] [cm]" , text_pos2, FONT_FAM, FONT_SCALE, (255, 0, 0), FONT_THICKNESS)
    cv2.putText(im, "x_origin", (int(endpos[0]+(rotation_center[0]-endpos[0])/2), endpos[1]-10), FONT_FAM, FONT_SCALE, (255, 0, 0), FONT_THICKNESS)
    cv2.putText(im, "y_origin", (rotation_center[0]-90, int(rotation_center[1]+(endpos[1]-rotation_center[1])/2)), FONT_FAM, FONT_SCALE, (255, 0, 0), FONT_THICKNESS)
    
    cv2.imshow("Swordfish Tail Tracking", im)
    if save_param["is_save"]:
        output_folder = save_param["output_folder"]
        filename = save_param["filename"]
        extension = save_param["extension"]
        cv2.imwrite(os.path.join(output_folder, filename + "_contour" + extension), im_contour)
        cv2.imwrite(os.path.join(output_folder, filename + "_tracking" + extension), im)
    return endpos