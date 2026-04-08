
clear all; clc

% Data for each category (rows = regions NW..CONUS, cols = SSP345-L, SSP345-H, SSP585-L, SSP585-H)

rainfed_corn = [
    0.03 0.04 0.03 0.03;
    0.00 0.01 0.01 0.02;
    0.44 0.52 0.52 0.56;
    0.05 0.06 0.07 0.09;
    0.79 0.77 0.60 0.64;
    0.17 0.15 0.10 0.11;
    0.29 0.28 0.19 0.22;
    1.78 1.85 1.51 1.68];

rainfed_wheat = [
    0.92 1.03 0.50 0.49;
    0.58 0.58 0.32 0.34;
    2.30 2.22 1.17 1.21;
    1.52 1.63 0.82 0.88;
    0.27 0.20 -0.10 -0.10;
    0.08 0.08 -0.04 -0.04;
    -0.02 -0.02 -0.04 -0.04;
    5.64 5.72 2.63 2.74];

rainfed_soybean = [
    0.00 0.00 0.00 0.00;
    0.02 0.02 0.02 0.01;
    0.57 0.65 0.54 0.43;
    -0.04 -0.05 0.05 -0.06;
    1.15 1.13 0.96 0.73;
    0.88 0.71 0.56 0.52;
    0.18 0.09 0.08 0.11;
    2.76 2.54 2.22 1.76];

bioenergy_crop = [
    0.20 0.18 0.14 0.14;
    0.30 0.27 0.25 0.20;
    0.23 0.20 0.18 0.17;
    0.79 0.80 0.47 0.54;
    0.29 0.32 0.22 0.17;
    0.27 0.26 0.20 0.17;
    0.09 0.08 0.05 0.04;
    2.16 2.12 1.51 1.44];

forest = [
    -0.15 -0.18 0.81 0.81;
    3.21 3.23 3.68 3.69;
    -0.12 -0.16 0.46 0.45;
    0.15 0.15 0.53 0.52;
    0.07 0.21 0.62 0.68;
    -0.58 -0.37 0.89 0.99;
    -0.32 -0.22 0.11 0.10;
    2.26 2.66 7.10 7.24];

grass = [
    -2.66 -2.68 -2.36 -2.37;
    -3.91 -3.93 -2.86 -2.85;
    -7.69 -7.77 -6.31 -6.23;
    -6.18 -6.21 -5.26 -5.29;
    -4.44 -4.42 -4.07 -3.98;
    -4.23 -4.18 -3.83 -3.80;
    -1.26 -1.27 -1.23 -1.24;
    -30.39 -30.45 -25.91 -25.75];

shrub = [
    0.43 0.42 0.49 0.49;
    2.35 2.37 2.75 2.76;
    0.06 0.05 0.08 0.08;
    0.20 0.20 0.27 0.27;
    0.00 0.00 0.00 0.00;
    0.00 0.00 0.00 0.00;
    0.00 0.00 0.00 0.00;
    3.03 3.04 3.59 3.60];

urban = [
    0.00 0.00 0.09 0.09;
    0.01 0.01 0.24 0.24;
    0.01 0.01 0.08 0.08;
    0.02 0.02 0.21 0.21;
    0.04 0.04 0.41 0.41;
    -0.02 -0.02 0.45 0.45;
    -0.02 -0.02 0.22 0.22;
    0.04 0.04 1.70 1.70];

bare_area = [
    -0.58 -0.58 -0.58 -0.58;
    -6.52 -6.52 -6.52 -6.52;
    -0.85 -0.84 -0.85 -0.85;
    -0.59 -0.59 -0.59 -0.59;
    -0.01 -0.01 -0.01 -0.01;
    -0.04 -0.04 -0.04 -0.04;
    -0.01 -0.01 -0.01 -0.01;
    -8.59 -8.59 -8.59 -8.59];

% Put data in a cell array for easy looping
data_all = {rainfed_corn, rainfed_wheat, rainfed_soybean, bioenergy_crop, forest, grass, shrub, urban, bare_area};
titles_all = {'(a) Rainfed Corn', ' (b) Rainfed Wheat', '(c) Rainfed Soybean', '(d) Bioenergy Crop', '(e) Forest', '(f) Grass', '(g) Shrub', '(h) Urban', '(i) Bareground'};



% Define custom colors: light blue, dark blue, light red, dark red
colors = [
    0.70, 0.85, 1.00;  % SSP345-L
    0.00, 0.30, 0.80;  % SSP345-H
    1.00, 0.75, 0.75;  % SSP585-L
    0.75, 0.00, 0.00   % SSP585-H
];


figure;
for i = 1:9
    subplot(3,3,i);
    b = bar(data_all{i}, 'grouped');
    for k = 1:4
        b(k).FaceColor = colors(k,:);
    end
    title(titles_all{i});
    ylabel('2055 - 2015 (% CONUS)');
    xticklabels({'NW','SW','NGP','SGP','MW','SE','NE','CONUS'});
    xtickangle(45);
    grid on;
    if i == 1
        legend({'atm45cooler_ssp3','atm45hotter_ssp3','atm85cooler_ssp5','atm85hotter_ssp5'}, ...
    'Location', 'northwest', 'Interpreter', 'none');
    end
end











%% output the plot

fig = gcf;
fig.PaperUnits = 'inches';

% fig.PaperPosition = [0 0 17.7 8];
fig.PaperPosition = [0 0 12 8];
print('ScreenSizeFigure', '-dpng', '-r300')


