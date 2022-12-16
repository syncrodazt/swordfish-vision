# python - Getting timestamp of each frame in a video - Stack Overflow
# https://stackoverflow.com/questions/47743246/getting-timestamp-of-each-frame-in-a-video

import sys
import numpy as np
import cv2
import moviepy.editor as mpy
from matplotlib import pyplot as plt

vid = mpy.VideoFileClip('swordfish 01.mov')

for i, (tstamp, frame) in enumerate(vid.iter_frames(with_times=True)):
    print(tstamp % 60)
    plt.imshow(frame)
    plt.show()
