close all;
pos = csvread("swordfish 08.csv");
N = length(pos);
origin = [560 89];
figure;
i = 1;
plot(-(pos(i, 1)-origin(1)), pos(i, 2)-origin(2), '.b')
% scatter(-(pos(i, 1)-origin(1)), pos(i, 2)-origin(2), '.b', 'MarkerEdgeAlpha', i/N)
% xlim([0 720])
% ylim([0 1280])
% xlim([0 1080])
% ylim([0 1920])
xlim([-1080/2 1080/2])
ylim([0 1920])
% axis equal
xlabel("x [px]", "Interpreter", "latex")
ylabel("y [px]", "Interpreter", "latex")
set(gca, "TickLabelInterpreter", "latex")
daspect([1 1 1])
grid on;
hold on;


for i = 2:N
% for i = 2:100
%     cla
    plot(-(pos(i, 1)-origin(1)), pos(i, 2)-origin(2), '.b')
%     scatter(-(pos(i, 1)-origin(1)), pos(i, 2)-origin(2), '.b', 'MarkerEdgeAlpha', i/N)
%     xlim([0 1080])
%     ylim([0 1920])
%     axis equal

    pause(0.001)
end

%%

ts = 1:1/240:10;
px2cm = 0.098/900;
pos_cm = (pos(:, 1)-origin(1))*px2cm;
pos_cm_trim = pos_cm(54:end, :);
ts = ts(1:length(pos_cm_trim));

plot(ts, pos_cm_trim)
xlabel("time [sec]", "Interpreter", "latex")
ylabel("x [m]", "Interpreter", "latex")
set(gca, "TickLabelInterpreter", "latex", "FontSize", 18)
grid on
% daspect([1 1 1])




