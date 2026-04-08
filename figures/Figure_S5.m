
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

annual = [
   -2.8,  -2.5,  -4.1,  -2.9;
   -4.9,  -7.3,  -6.3,  -8.7;
   -1.4,  -1.2,  -4.2,  -4.6;
   -2.2,  -6.7,  -3.7,  -6.5;
   -6.8, -12.8, -10.8, -16.0;
   -4.1,  -9.3,  -7.4, -10.7;
    1.4,  -2.8,  -0.5,  -0.4;
   -3.3,  -7.0,  -5.9,  -8.2;
];

% DJF data
djf = [
   -4.72,  -2.30,  -5.46,  -2.55;
   -3.32,  -1.27,  -4.31,  -0.65;
   -0.57,   2.39,  -1.93,   1.76;
    3.77,   5.93,   3.15,   6.89;
   -4.02,  -6.48,  -7.57,  -6.79;
   -1.32,  -4.85,  -5.57,  -7.36;
   -2.58,  -8.85,  -5.17,  -7.28;
   -2.08,  -2.84,  -4.39,  -3.31;
];

% MAM data
mam = [
   -2.91,  -3.60,  -6.09,  -4.84;
   -3.43,  -4.20,  -6.06,  -3.97;
    1.62,  -2.37,  -3.51,  -3.25;
   -0.61,  -2.26,  -0.65,   1.47;
   -2.85,  -8.84,  -5.78,  -9.89;
   -4.02,  -9.53,  -5.78,  -9.83;
    1.68,  -2.68,   0.14,  -4.11;
   -1.66,  -5.47,  -4.07,  -5.60;
];

% JJA data
jja = [
   -3.13,  -0.35,  -3.17,  -1.13;
  -14.17, -22.46, -15.56, -28.86;
   -8.94,  -0.31, -11.66,  -9.05;
  -13.19, -20.74, -15.34, -25.03;
  -14.42, -19.95, -19.82, -25.75;
   -7.98, -13.20, -11.61, -16.30;
    4.07,  -1.06,   2.50,   5.06;
   -8.45, -12.28, -11.62, -15.67;
];

% SON data
son = [
   -1.24,  -4.02,  -2.16,  -4.54;
   -2.18,  -8.41,  -3.18, -11.53;
    1.64,  -3.10,   0.59,  -6.19;
    1.32,  -9.01,  -2.18,  -9.82;
   -4.74, -13.16,  -8.66, -18.22;
   -1.70,  -8.32,  -5.66,  -8.02;
    1.40,   0.42,  -1.77,   2.27;
   -1.13,  -7.19,  -3.94,  -8.72;
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

    title([season_names{i} ' ΔAridity (%)'], 'FontWeight', 'bold')
    ylabel('ΔAridity (%)')
    xticks(1:8)
    xticklabels(regions)
    xtickangle(45)
    ylim([-30 10])
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


