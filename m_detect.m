close all;
I = imread("swordfish 01.png");
figure;
imshow(I);
BW = im2bw(I, 0.60);
figure;
imshow(BW);

figure;
BW = bwareaopen(BW, 30);
imshow(BW);

figure;
se = strel('disk', 2);
BW = imclose(BW, se);
imshow(BW)

figure;
BW = 1 - BW;
imshow(BW)
dim = size(BW);
% col = round(dim(2)/2)-90;
% row = min(find(BW(:,col)));
col = 285;
row = 1307;

boundary = bwtraceboundary(BW, [row, col], 'S', 8, 90);
figure;
imshow(I)
hold on;
plot(boundary(:, 2), boundary(:, 1), 'g', 'LineWidth', 3);

%% remove shadow

I = imread("swordfish 01.png");
I = rgb2gray(I);
imshow(I)

se = strel('disk', 700)
background = imopen(I, se);
imshow(background)
I2 = I - background;
imshow(I2)
I3 = imadjust(I2);
imshow(I3)
bw = imbinarize(I3);
bw = bwareaopen(bw, 50);
imshow(bw)

%% canny
I = imread("swordfish 01.png");
I = rgb2gray(I);
BW1 = edge(I, 'Canny');
BW2 = edge(I, 'Prewitt');
imshowpair(BW1, BW2, 'montage')
