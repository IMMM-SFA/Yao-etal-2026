import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
import pandas as pd

# Set up figure parameters
side = 0.6
r = side / np.cos(np.radians(30))
a = 2 * side
offset_x = 0.5
offset_y = 1.4
vertical_offset = side * np.sqrt(3)

path = '/filepath/sensitivity_analyses/median_nondrought_reference_yield/'

df = pd.read_csv(f'{path}projection_divergence_production_loss_change.csv')

df = df[df['scenario'] == 'NF']

regions = [
    'Northwest', 'N. Great Plains', 'Midwest', 'Northeast',
    'Southwest', 'S. Great Plains', 'Southeast'
]
abbreviations = ['NW', 'NGP', 'MW', 'NE', 'SW', 'SGP', 'SE']

positions = [
    {'x': offset_x, 'y': offset_y},
    {'x': offset_x + a, 'y': offset_y},
    {'x': offset_x + 2 * a, 'y': offset_y},
    {'x': offset_x + 3 * a, 'y': offset_y},
    {'x': offset_x + 0.5 * a, 'y': offset_y - vertical_offset},
    {'x': offset_x + 1.5 * a, 'y': offset_y - vertical_offset},
    {'x': offset_x + 2.5 * a, 'y': offset_y - vertical_offset}
]

crops = ['corn', 'soybean']

comparison_types = [
    {
        'label': 'atm45_ssp3 vs atm85_ssp5',
        'nrmse_col': 'scenario_nrmse_mean',
        'sign_col': 'scenario_sign_agreement_mean'
    },
    {
        'label': 'Cooler vs Hotter',
        'nrmse_col': 'esm_variant_nrmse_mean',
        'sign_col': 'esm_variant_sign_agreement_mean'
    }
]

subplot_labels = ['(a)', '(b)', '(c)', '(d)']

fig, axes = plt.subplots(2, 2, figsize=(18, 6.2), sharex=True, sharey=True)
axes = axes.flatten()

norm = plt.Normalize(0.5, 1.0)

cmap = plt.get_cmap('YlOrRd_r')

idx = 0
for crop in crops:
    for comp in comparison_types:
        ax = axes[idx]
        ax.set_aspect('equal')
        ax.set_xlim(-0.5, 5.0)
        ax.set_ylim(-0.4, 2.4)
        ax.axis('off')

        nrmse_col = comp['nrmse_col']
        sign_col = comp['sign_col']

        # Select data for this crop
        data_crop = df[df['crop'] == crop]

        # Create dictionaries
        sign_dict = dict(zip(data_crop['region_name'], data_crop[sign_col]))
        nrmse_dict = dict(zip(data_crop['region_name'], data_crop[nrmse_col]))

        # Draw hexagons
        for region, pos, abbr in zip(regions, positions, abbreviations):
            sign_agree = sign_dict.get(region, np.nan)
            nrmse_val = nrmse_dict.get(region, np.nan)

            if not pd.isna(sign_agree):
                color = cmap(norm(sign_agree))
            else:
                color = (0.9, 0.9, 0.9)

            if not pd.isna(nrmse_val):
                nrmse_text = f'{nrmse_val:.2f}'
                text_color = 'black'
            else:
                nrmse_text = 'N/A'
                text_color = 'gray'

            hexagon = patches.RegularPolygon(
                (pos['x'], pos['y']),
                numVertices=6,
                radius=r,
                orientation=0,
                facecolor=color,
                edgecolor='black',
                linewidth=1
            )
            ax.add_patch(hexagon)

            # Region abbreviation
            ax.text(
                pos['x'], pos['y'] + 0.12,
                abbr,
                ha='center', va='center',
                fontsize=8,
                color='black',
                fontweight='bold'
            )

            # NRMSE value inside hex
            ax.text(
                pos['x'], pos['y'] - 0.13,
                nrmse_text,
                ha='center', va='center',
                fontsize=8,
                color=text_color
            )

        # Subplot label
        ax.text(
            0.06, 0.2,
            subplot_labels[idx],
            transform=ax.transAxes,
            ha='left', va='top',
            fontsize=12
        )

        idx += 1

row_positions = [0.71, 0.38]
for crop, y_pos in zip(crops, row_positions):
    fig.text(
        0.3, y_pos,
        crop.capitalize(),
        ha='right', va='center',
        fontsize=12,
        rotation=90
    )

fig.text(0.4, 0.81, comparison_types[0]['label'], ha='center', va='center', fontsize=12)
fig.text(0.6, 0.81, comparison_types[1]['label'], ha='center', va='center', fontsize=12)

# Colorbar for sign agreement
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])

cbar = fig.colorbar(
    sm,
    ax=axes.ravel().tolist(),
    orientation='horizontal',
    fraction=0.025, 
    pad=0.06
)

cbar.set_ticks([0.5, 0.75, 1.0])
cbar.ax.tick_params(labelsize=12)
cbar.set_label('Directional agreement', fontsize=12)

fig.text(
    0.51, 0.16, 
    'Color: directional agreement; numbers: normalized RMSE',
    ha='center', va='top',
    fontsize=11
)

plt.subplots_adjust(
    wspace=0.0,
    hspace=0.0,
    left=0.3,
    right=0.7,
    top=0.85, 
    bottom=0.18
)

# Save figure
plt.savefig(
    f'{path}/projection_divergence_sign_agreement_nrmse_NF_cornsoybeanonly.png',
    format='png',
    bbox_inches='tight',
    dpi=300
)

plt.show()