from mpl_toolkits.axes_grid1 import make_axes_locatable
# 1 'Northeast', 2 'Southeast', 4 'Midwest', 5'N. Great Plains', 6'S. Great Plains', 8'Northwest', 7'Southwest'
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# state to NCA mapping CSV file
nca_mapping_path = 'state_nca_mapping.csv'  
nca_mapping = pd.read_csv(nca_mapping_path)


# Colorblind-friendly colors for crops
crop_colors = {
    'corn': '#4c78a8',  # Blue
    'wheat': '#f58518',  # Orange
    'soybean': '#009e73'  # Teal
}

plt.figure(figsize=(5, 5))

# Data path
path = '/data_path/'

# Define region colors
# Colorblind-friendly colors for regions
region_colors = {
    1: '#4c78a8',  # Northeast: Blue
    2: '#f58518',  # Southeast: Orange
    4: '#54a24b',  # Midwest: Olive green 
    5: '#b79a20',  # N. Great Plains: Gold
    6: '#7b4e99',  # S. Great Plains: Purple 
    8: '#e45756',  # Northwest: Salmon
    7: '#79706e'   # Southwest: Gray
}
region_names = {
    1: 'NE',
    2: 'SE',
    4: 'MW',
    5: 'NGP',
    6: 'SGP',
    8: 'NW',
    7: 'SW'
}


# Create figure and split axes
fig = plt.figure(figsize=(5, 6))  # Increased height for two subplots
fig.set_facecolor('white')  # Ensure consistent background
ax = plt.gca()
ax.set_facecolor('white')  # Match subplot background to figure
divider = make_axes_locatable(ax)
ax_top = divider.append_axes("top", size="40%", pad=0.0, sharex=ax)
ax_bottom = ax  # Bottom axis is the main axis
ax_top.spines['bottom'].set_visible(False)  # Hide bottom spine of top subplot
ax_bottom.spines['top'].set_visible(False)  # Hide top spine of bottom subplot
# Plot on both axes
for crop in ['corn']:
    ## near future
    df_345c_nf = pd.read_csv(f'{path}{crop}_financial_loss_nf_3_45_c_2021-2055.csv')
    df_585c_nf = pd.read_csv(f'{path}{crop}_financial_loss_nf_5_85_c_2021-2055.csv')
    df_345h_nf = pd.read_csv(f'{path}{crop}_financial_loss_nf_3_45_h_2021-2055.csv')
    df_585h_nf = pd.read_csv(f'{path}{crop}_financial_loss_nf_5_85_h_2021-2055.csv')
    # Merge the NCA mapping to the original data based on 'state_id'
    df_345c_nf = df_345c_nf.merge(nca_mapping, on='state_id', how='left')
    df_585c_nf = df_585c_nf.merge(nca_mapping, on='state_id', how='left')
    df_345h_nf = df_345h_nf.merge(nca_mapping, on='state_id', how='left')
    df_585h_nf = df_585h_nf.merge(nca_mapping, on='state_id', how='left')
    # Replace zeros with a small value (1e-10) to avoid division by zero
    df_585c_nf['Financial_Loss($)'] = df_585c_nf['Financial_Loss($)'].replace(0, 1e-10)
    df_585h_nf['Financial_Loss($)'] = df_585h_nf['Financial_Loss($)'].replace(0, 1e-10)
    # Group by 'Year' for CONUS aggregates
    df_345c_conus_nf = df_345c_nf.groupby('Year').sum()[['Production_Loss(ton)', 'Financial_Loss($)']]
    df_585c_conus_nf = df_585c_nf.groupby('Year').sum()[['Production_Loss(ton)', 'Financial_Loss($)']]
    df_345h_conus_nf = df_345h_nf.groupby('Year').sum()[['Production_Loss(ton)', 'Financial_Loss($)']]
    df_585h_conus_nf = df_585h_nf.groupby('Year').sum()[['Production_Loss(ton)', 'Financial_Loss($)']]
    # Replace zeros in CONUS aggregates
    df_585c_conus_nf['Financial_Loss($)'] = df_585c_conus_nf['Financial_Loss($)'].replace(0, 1e-10)
    df_585h_conus_nf['Financial_Loss($)'] = df_585h_conus_nf['Financial_Loss($)'].replace(0, 1e-10)
    # Now group by 'nca_id' and 'Year' for regional data
    df_345c_nca_nf = df_345c_nf.groupby(['nca_id', 'Year']).sum()[['Production_Loss(ton)', 'Financial_Loss($)']]
    df_585c_nca_nf = df_585c_nf.groupby(['nca_id', 'Year']).sum()[['Production_Loss(ton)', 'Financial_Loss($)']]
    df_345h_nca_nf = df_345h_nf.groupby(['nca_id', 'Year']).sum()[['Production_Loss(ton)', 'Financial_Loss($)']]
    df_585h_nca_nf = df_585h_nf.groupby(['nca_id', 'Year']).sum()[['Production_Loss(ton)', 'Financial_Loss($)']]
    # Calculate the relative difference in financial loss
    diff_h_nf = (df_345h_nca_nf['Financial_Loss($)'] - df_585h_nca_nf['Financial_Loss($)']) / df_585h_nca_nf['Financial_Loss($)'] * 100
    diff_c_nf = (df_345c_nca_nf['Financial_Loss($)'] - df_585c_nca_nf['Financial_Loss($)']) / df_585c_nca_nf['Financial_Loss($)'] * 100
    diff_nf = (diff_c_nf + diff_h_nf)/2.0
    diff_nf = diff_c_nf
    
    # Calculate the relative change in financial loss for CONUS
    diff_h_nf_conus = (df_345h_conus_nf['Financial_Loss($)'] - df_585h_conus_nf['Financial_Loss($)']) / df_585h_conus_nf['Financial_Loss($)'] * 100
    diff_c_nf_conus = (df_345c_conus_nf['Financial_Loss($)'] - df_585c_conus_nf['Financial_Loss($)']) / df_585c_conus_nf['Financial_Loss($)'] * 100
    # diff_nf_conus = (diff_c_nf_conus + diff_h_nf_conus)/2.0
    diff_nf_conus = diff_c_nf_conus 
    
    # Apply Kernel Density Estimation (KDE) for smoothing
    kde_nf_conus = gaussian_kde(diff_nf_conus, bw_method=0.1)
    x_nf_conus = np.linspace(min(diff_nf_conus), max(diff_nf_conus), 2000)
    pdf_nf_conus = kde_nf_conus.evaluate(x_nf_conus)
    cdf_nf_conus = np.cumsum(pdf_nf_conus) * (x_nf_conus[1] - x_nf_conus[0]) / np.max(np.cumsum(pdf_nf_conus) * (x_nf_conus[1] - x_nf_conus[0]))
    
    # Plot CONUS on both axes
    ax_top.plot(x_nf_conus, cdf_nf_conus, linestyle='-', color='black', linewidth=3, label='CONUS')
    ax_bottom.plot(x_nf_conus, cdf_nf_conus, linestyle='-', color='black', linewidth=3, label='CONUS')
    # Find x-value where CDF reaches y=0.99 for CONUS
    idx_conus = np.argmin(np.abs(cdf_nf_conus - 0.99))
    x_conus_99 = x_nf_conus[idx_conus]
    ax_top.vlines(x=x_conus_99, ymin=0.9, ymax=0.99, color='black', linestyle=':', linewidth=1.5, alpha=0.7)
    ax_bottom.vlines(x=x_conus_99, ymin=0, ymax=min(0.99, 0.9), color='black', linestyle=':', linewidth=1.5, alpha=0.7)
    # Iterate through each NCA and apply KDE for each NCA
    ax_bottom.text(x_conus_99 - 20, 0.015, f'{x_conus_99:.0f}', color='black', fontsize=12, ha='left', va='center', weight="bold") # crop_colors[crop],
    
    for nca_id in [4, 5, 6]:
        diff_nf_nca = diff_nf.loc[nca_id].dropna()
        kde_nf = gaussian_kde(diff_nf_nca, bw_method=0.1)
        x_nf = np.linspace(min(diff_nf_nca), max(diff_nf_nca), 2000)
        pdf_nf = kde_nf.evaluate(x_nf)
        cdf_nf = np.cumsum(pdf_nf) * (x_nf[1] - x_nf[0]) / np.max(np.cumsum(pdf_nf) * (x_nf[1] - x_nf[0]))
        # Plotting the CDF for the relative change in financial loss for each NCA
        ax_top.plot(x_nf, cdf_nf, linestyle='-', color=region_colors[nca_id], linewidth=2, label=f'{region_names[nca_id]}')
        ax_bottom.plot(x_nf, cdf_nf, linestyle='-', color=region_colors[nca_id], linewidth=2, label=f'{region_names[nca_id]}')
        # Find x-value where CDF reaches y=0.99 for this region
        idx_nca = np.argmin(np.abs(cdf_nf - 0.99))
        x_nca_99 = x_nf[idx_nca]
        ax_top.vlines(x=x_nca_99, ymin=0.9, ymax=0.99, color=region_colors[nca_id], linestyle=':', linewidth=1.5, alpha=0.7)
        ax_bottom.vlines(x=x_nca_99, ymin=0, ymax=min(0.99, 0.9), color=region_colors[nca_id], linestyle=':', linewidth=1.5, alpha=0.7)
        if nca_id == 6:
            ax_bottom.text(x_nca_99+2 , 0.015, f'{x_nca_99:.0f}', color=region_colors[nca_id], fontsize=12, ha='left', va='center', weight="bold")
        elif nca_id == 4:
            ax_bottom.text(x_nca_99 -15, 0.015, f'{x_nca_99:.0f}', color=region_colors[nca_id], fontsize=12, ha='left', va='center', weight="bold")
        elif nca_id == 5:
            ax_bottom.text(x_nca_99-4, 0.015, f'{x_nca_99:.0f}', color=region_colors[nca_id], fontsize=12, ha='left', va='center', weight="bold")   
        elif nca_id == 8:
            ax_bottom.text(x_nca_99-7, 0.015, f'{x_nca_99:.0f}', color=region_colors[nca_id], fontsize=12, ha='left', va='center', weight="bold")   
            
# Final plot settings
ax_top.set_ylim(0.90, 1.0)  # Zoomed-in range for high probabilities
ax_bottom.set_ylim(0, 0.90)  # Lower range to align at y=0.9
ax_top.set_xlim(-80, 150)
ax_bottom.set_xlim(-80, 150)
ax_bottom.set_xlabel('atm45_ssp3 vs atm85_ssp5 in Financial Loss (%)', fontsize=14)
# ax_bottom.set_ylabel('Cumulative Probability', fontsize=14, labelpad=10)
# Final plot settings
fig.text(-0.001, 0.5, 'Cumulative Probability', rotation=90, ha='center', va='center', fontsize=16)
fig.text(0.23, 0.93, '(a1) Corn', rotation=0, ha='center', va='center', fontsize=14)

ax_top.set_ylabel('', fontsize=14)  # No y-label for top axis
ax_top.tick_params(axis='x', which='both', bottom=False, labelbottom=False)  # Hide x-ticks on top axis
ax_top.set_yticks([0.95, 0.99])  # Ticks for top axis
ax_bottom.set_yticks([0, 0.3, 0.6, 0.9])  # Ticks for bottom axis, including 0.9
ax_top.tick_params(axis='y', labelsize=14)
ax_bottom.tick_params(axis='both', labelsize=14)
ax_top.grid(True, linestyle='--', alpha=0.7, which='major', axis='y')
ax_bottom.grid(True, linestyle='--', alpha=0.7, which='major', axis='y')
ax_top.axvline(x=0, color='gray', linestyle='--', linewidth=2, alpha=0.8)
ax_bottom.axvline(x=0, color='gray', linestyle='--', linewidth=2, alpha=0.8)
# ax_bottom.legend(fontsize=12, loc='center right')
fig.tight_layout(pad=0.5)
plt.savefig(f'{path}/financial_loss_345diff585_corn_cooler.png', dpi=300, bbox_inches='tight')
print ('done')