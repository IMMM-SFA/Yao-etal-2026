
clear all; clc

% Define regions and scenarios
regions = {'NW','SW','NGP','SGP','MW','SE','NE','CONUS'};
scenarios = {'SSP345-L','SSP345-H','SSP585-L','SSP585-H'};

% Define custom colors: light blue, dark blue, light red, dark red
colors = [
    0.70, 0.85, 1.00;  % SSP345-L
    0.00, 0.30, 0.80;  % SSP345-H
    1.00, 0.75, 0.75;  % SSP585-L
    0.75, 0.00, 0.00   % SSP585-H
];

% Define delta precipitation data (%)
annual = [
    2.4 4.5 1.8 5.5;
   -0.1 -0.7 -0.8 -1.1;
    4.3 6.9 2.6 5.4;
    2.6 0.0 1.9 1.3;
   -0.1 -3.2 -2.8 -4.8;
    1.1 -2.1 -1.2 -2.3;
    6.6 4.8 5.5 8.4;
    2.0 0.5 0.3 0.5];

djf = [
    1.13 5.39 1.38 7.29;
    2.40 6.54 2.46 9.33;
    4.85 8.53 4.89 10.17;
    9.16 13.04 9.89 16.78;
    2.47 1.55 0.61 3.87;
    3.91 2.39 1.30 1.94;
    2.64 -1.42 2.09 2.80;
    3.44 4.42 2.52 6.26];

mam = [
    2.48 2.97 -0.16 2.84;
    1.37 1.78 -0.89 2.95;
    7.62 5.84 4.00 6.56;
    3.66 3.39 4.32 7.59;
    3.36 -0.68 1.51 -0.51;
    0.54 -3.56 -0.54 -3.09;
    6.95 4.10 5.84 3.98;
    3.43 1.11 1.78 1.94];

jja = [
    1.58 6.36 2.33 7.01;
   -10.27 -17.14 -10.92 -23.26;
   -3.88 6.90 -5.70 -0.25;
   -8.69 -14.91 -10.18 -18.75;
   -8.03 -11.58 -12.58 -16.00;
   -2.51 -5.95 -5.30 -7.80;
    9.11 6.57 8.13 13.73;
   -3.43 -5.46 -5.81 -7.74];

son = [
    4.88 4.11 4.42 5.24;
    3.30 -0.69 3.10 -2.72;
    8.06 7.45 8.31 6.31;
    6.58 -0.75 3.85 -0.52;
    2.97 -0.10 0.71 -3.90;
    3.72 -0.18 0.81 1.17;
    6.68 9.15 4.91 12.07;
    4.78 2.01 3.00 1.82];

% Combine into cell array
seasonal_data = {annual, djf, mam, jja, son};
season_names = {'Annual','DJF','MAM','JJA','SON'};

% Create figure
figure('Position', [100, 100, 1200, 900])
t = tiledlayout(3,2, 'TileSpacing', 'compact', 'Padding', 'compact');

legend_handles = gobjects(4,1);

% Plot each season
for i = 1:5
    nexttile
    data = seasonal_data{i};

    b = bar(data, 'grouped');
    for j = 1:4
        b(j).FaceColor = colors(j,:);
        if i == 1
            legend_handles(j) = b(j);
        end
    end

    title([season_names{i} ' ΔPrecip (%)'], 'FontWeight', 'bold')
    ylabel('ΔPrecipitation (%)')
    xticks(1:8)
    xticklabels(regions)
    xtickangle(45)
    ylim([-25 20])
    yline(0, '--k')  % zero-change reference line
    grid on
end

% Add legend in the 6th tile
ax_dummy = nexttile(6);
cla(ax_dummy)
axis off
hold on
for j = 1:4
    ph(j) = plot(nan, nan, '-', 'LineWidth', 8, 'Color', colors(j,:));
end
hold off
lgd = legend(ax_dummy, ph, scenarios, ...
    'Orientation', 'vertical', ...
    'Box', 'off', ...
    'Location', 'north');
title(lgd, '(Mean 2021–2055 − Mean 1981–2015) / Mean 1981–2015 × 100%', 'FontSize', 10)


%% output the plot

fig = gcf;
fig.PaperUnits = 'inches';

% fig.PaperPosition = [0 0 17.7 8];
fig.PaperPosition = [0 0 10 10];
print('ScreenSizeFigure', '-dpng', '-r300')


