filename = 'input/swordfish 08.mov';
vidObj = VideoReader(filename);
ts_fromfile = zeros(1, vidObj.NumFrames);
count = 1;
while(hasFrame(vidObj))
    frame = readFrame(vidObj);
    imshow(frame);
    BW = im2bw(frame, 0.80);
    BW = bwareaopen(BW,30);
%     se = strel('disk',2);
%     BW = imclose(BW,se);
    BW = 1-BW;
    ts_fromfile(count) = vidObj.CurrentTime;
%     imshow(BW);
    title(sprintf('Current Time = %.3f sec', vidObj.CurrentTime));
%     pause(2/vidObj.FrameRate);
    count = count + 1;
end