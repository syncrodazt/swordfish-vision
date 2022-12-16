close all;
pos = csvread("swordfish 01.csv");
N = length(pos);
origin = [500 200];
figure;
i = 1;
scatter(-(pos(i, 1)-origin(1)), pos(i, 2)-origin(2), '.b', 'MarkerEdgeAlpha', i/N)
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
    scatter(-(pos(i, 1)-origin(1)), pos(i, 2)-origin(2), '.b', 'MarkerEdgeAlpha', i/N)
%     xlim([0 1080])
%     ylim([0 1920])
%     axis equal

    pause(0.001)
end
