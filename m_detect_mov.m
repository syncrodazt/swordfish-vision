filename = 'swordfish 05.mp4';
vidObj = VideoReader(filename);
while(hasFrame(vidObj))
    frame = readFrame(vidObj);

    BW = im2bw(frame, 0.80);
    BW = bwareaopen(BW,30);
%     se = strel('disk',2);
%     BW = imclose(BW,se);
    BW = 1-BW;

    imshow(BW);
    title(sprintf('Current Time = %.3f sec', vidObj.CurrentTime));
    pause(2/vidObj.FrameRate);
end