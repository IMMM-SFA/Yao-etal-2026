
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
    5.4, 7.2, 6.1, 8.7;   % NW
    5.0, 7.1, 5.8, 8.3;   % SW
    5.8, 8.2, 7.2, 10.5;  % NGP
    4.9, 7.2, 5.9, 8.3;   % SGP
    7.3, 11.0, 9.0, 13.3; % MW
    5.4, 7.9, 6.6, 9.3;   % SE
    5.1, 7.8, 6.0, 8.8;   % NE
    5.5, 8.0, 6.6, 9.5;   % CONUS
];

% DJF data
djf = [
    6.14, 7.87, 7.23, 10.10;
    5.91, 7.91, 7.08, 10.05;
    5.45, 6.00, 6.96, 8.27;
    5.20, 6.71, 6.54, 9.26;
    6.77, 8.59, 8.85, 11.44;
    5.30, 7.61, 7.27, 10.04;
    5.35, 8.16, 7.65, 10.88;
    5.64, 7.48, 7.22, 9.90;
];

% MAM data
mam = [
    5.55, 6.81, 6.32, 8.07;
    4.97, 6.24, 5.51, 7.21;
    5.91, 8.41, 7.79, 10.14;
    4.30, 5.79, 5.01, 6.03;
    6.39, 8.95, 7.73, 10.41;
    4.75, 6.60, 5.57, 7.48;
    5.19, 6.97, 5.69, 8.44;
    5.17, 6.95, 6.10, 7.99;
];

% JJA data
jja = [
    4.86, 6.73, 5.69, 8.23;
    4.55, 6.86, 5.50, 7.88;
    5.55, 7.23, 6.74, 9.67;
    5.18, 7.35, 6.10, 8.38;
    7.47, 10.45, 9.04, 13.13;
    5.94, 8.35, 7.14, 10.15;
    4.85, 7.72, 5.49, 8.26;
    5.49, 7.78, 6.57, 9.41;
];

% SON data
son = [
    6.19, 8.48, 6.72, 10.25;
    5.60, 8.43, 6.49, 9.96;
    6.32, 10.88, 7.68, 13.32;
    5.19, 9.08, 6.17, 10.32;
    8.09, 15.04, 10.27, 17.51;
    5.51, 8.88, 6.86, 9.99;
    5.20, 8.69, 6.80, 9.58;
    5.98, 9.91, 7.22, 11.55;
];

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

    title([season_names{i} ' ΔPET (%)'], 'FontWeight', 'bold')
    ylabel('ΔPET (%)')
    xticks(1:8)
    xticklabels(regions)
    xtickangle(45)
    ylim([0 20])
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


