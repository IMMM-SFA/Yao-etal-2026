
clear all; clc

% Define regions and scenarios
regions = {'NW','SW','NGP','SGP','MW','SE','NE','CONUS'};
scenarios = {'SSP345-L','SSP345-H','SSP585-L','SSP585-H'};

% Define delta T data for each season and annual
annual = [
    1.61 2.10 1.78 2.51;
    1.55 2.07 1.76 2.44;
    1.73 2.40 2.03 2.87;
    1.46 1.94 1.68 2.30;
    1.74 2.46 2.07 2.94;
    1.38 1.82 1.59 2.20;
    1.50 2.16 1.79 2.59;
    1.58 2.14 1.82 2.55];

djf = [
    1.51 1.86 1.71 2.28;
    1.44 1.82 1.67 2.31;
    1.86 2.19 2.18 2.71;
    1.40 1.61 1.65 2.20;
    2.05 2.50 2.47 3.18;
    1.24 1.49 1.54 2.04;
    1.57 2.24 2.09 2.91;
    1.59 1.95 1.89 2.50];

mam = [
    1.48 1.82 1.52 2.10;
    1.46 1.83 1.55 2.12;
    1.58 2.11 1.83 2.47;
    1.31 1.65 1.48 1.87;
    1.54 2.05 1.82 2.38;
    1.28 1.57 1.42 1.82;
    1.43 1.89 1.62 2.24;
    1.44 1.85 1.61 2.15];

jja = [
    1.75 2.47 2.04 2.97;
    1.60 2.28 1.88 2.60;
    1.79 2.66 2.10 3.19;
    1.59 2.12 1.84 2.43;
    1.79 2.56 2.06 3.06;
    1.53 2.01 1.74 2.39;
    1.58 2.17 1.75 2.52;
    1.66 2.33 1.92 2.75];

son = [
    1.73 2.26 1.86 2.71;
    1.72 2.38 1.97 2.75;
    1.71 2.63 2.00 3.12;
    1.55 2.37 1.77 2.69;
    1.59 2.75 1.92 3.15;
    1.46 2.20 1.66 2.55;
    1.43 2.35 1.73 2.72;
    1.61 2.44 1.86 2.83];



% Combine all into a cell array
% Combine all into a cell array
seasonal_data = {annual, djf, mam, jja, son};
season_names = {'Annual','DJF','MAM','JJA','SON'};

% Set up figure
figure('Position', [100, 100, 1200, 900])
t = tiledlayout(3,2, 'TileSpacing', 'compact', 'Padding', 'compact');

% Set colors
colors = [
    0.70, 0.85, 1.00;  % SSP345-L (light blue)
    0.00, 0.30, 0.80;  % SSP345-H (dark blue)
    1.00, 0.75, 0.75;  % SSP585-L (light red)
    0.75, 0.00, 0.00   % SSP585-H (dark red)
];

% Store handles for legend
legend_handles = gobjects(4,1);

% Plot subplots
for i = 1:5
    nexttile
    data = seasonal_data{i};

    % Create grouped bar plot
    b = bar(data, 'grouped');
    for j = 1:4
        b(j).FaceColor = colors(j,:);
        if i == 1
            legend_handles(j) = b(j); % Save only once
        end
    end

    title([season_names{i} ' ΔT (°C)'], 'FontWeight', 'bold')
    ylabel('ΔT (°C)')
    xticks(1:8)
    xticklabels(regions)
    xtickangle(45)
    ylim([1 3.5])
    grid on
end

% Use last tile for legend
% Use last tile (tile 6) for custom legend
ax_dummy = nexttile(6);  % Select tile 6
cla(ax_dummy);           % Clear anything just in case
axis off                 % Hide dummy axes

% Plot invisible bars for legend handles
hold on
for j = 1:4
    ph(j) = plot(nan, nan, '-', 'LineWidth', 8, 'Color', colors(j,:));
end
hold off

% Now create the legend explicitly on that dummy axes
lgd = legend(ax_dummy, ph, scenarios, ...
    'Orientation', 'vertical', ...
    'Box', 'off', ...
    'Location', 'north');  % Inside tile 6
title(lgd, 'Mean (2021–2055) – Mean (1981–2015)', 'FontSize', 10)


%% output the plot

fig = gcf;
fig.PaperUnits = 'inches';

% fig.PaperPosition = [0 0 17.7 8];
fig.PaperPosition = [0 0 10 10];
print('ScreenSizeFigure', '-dpng', '-r300')


