##################################################################################### plot (a)
import xarray as xr 
import numpy as np 
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pathlib

# =====================================================================
# 1. GENERAL CONFIGURATION & PATHS
# =====================================================================
nca_id = 6 
region_file = '/filepath/clm_state_nca_area_lon180.nc'

hist_path = '/filepath/'
future_base_path = '/filepath/'

scenarios = [
    {'ssp': '3', 'rcp': '45', 'climate': 'c', 'label': 'atm45cooler_ssp3'},
    {'ssp': '3', 'rcp': '45', 'climate': 'h', 'label': 'atm45hotter_ssp3'},
    {'ssp': '5', 'rcp': '85', 'climate': 'c', 'label': 'atm85cooler_ssp5'},
    {'ssp': '5', 'rcp': '85', 'climate': 'h', 'label': 'atm85hotter_ssp5'}
]


combo_colors = {
    ('3', 'c'): '#aec7e8',  # Light Blue
    ('3', 'h'): '#1f77b4',  # Dark Blue
    ('5', 'c'): '#ffbb78',  # Light Orange
    ('5', 'h'): '#ff7f0e'   # Dark Orange
}

# Spring-First: March -> February
spring_first_indices = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]
month_names_spring_first = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
months_axis = np.arange(1, 13)

# Load region mask
ds_region = xr.open_dataset(region_file)

fig, ax = plt.subplots(figsize=(7, 5.5))

# =====================================================================
# 2. ADD SEASONAL BACKGROUND SHADING
# =====================================================================
ax.axvspan(0.5, 3.5, color='green', alpha=0.05)
ax.axvspan(3.5, 6.5, color='red', alpha=0.05)
ax.axvspan(6.5, 9.5, color='orange', alpha=0.05)
ax.axvspan(9.5, 12.5, color='blue', alpha=0.05)

# Storage for building the legend step-by-step
legend_handles = []
legend_labels = []

# =====================================================================
# 3. PROCESS & PLOT HISTORICAL BASELINE
# =====================================================================
print("Processing historical data...")
ds_hist = xr.open_dataset(f'{hist_path}pft19_lai_gpp_monthly_mean_1980-2015.nc')
ds_hist = ds_hist.assign_coords(lon=(((ds_hist.lon + 180) % 360) - 180))
ds_hist['GPP'] = ds_hist['GPP'] * 86400
ds_hist = ds_hist.sel(time=slice('1981', '2015'))

gpp_hist_region = ds_hist['GPP'].where(ds_region['nca'] == nca_id)
gpp_hist_climatology = gpp_hist_region.mean(dim=['lat', 'lon']).groupby('time.month').mean(dim='time')

# Reorder historical array to match Spring-First indexing mapping rules
hist_values = gpp_hist_climatology.values
reordered_hist = [hist_values[idx] for idx in spring_first_indices]

hist_line, = ax.plot(
    months_axis, reordered_hist,
    label='historical', color='#7f8c8d', 
    linewidth=1.8, marker='o', markersize=4
)
legend_handles.append(hist_line)
legend_labels.append('historical')

# =====================================================================
# 4. LOOP AND PLOT FUTURE SCENARIOS
# =====================================================================
for sc in scenarios:
    ssp, rcp, climate, label = sc['ssp'], sc['rcp'], sc['climate'], sc['label']
    file_name = f'pft19_lai_gpp_nf_{ssp}_{rcp}_{climate}_2020-2055_monthly_mean.nc'
    file_path = pathlib.Path(future_base_path) / file_name
    
    if not file_path.exists():
        continue
        
    print(f"Processing future scenario: {label}...")
    ds_fut = xr.open_dataset(file_path)
    ds_fut = ds_fut.assign_coords(lon=(((ds_fut.lon + 180) % 360) - 180))
    ds_fut['GPP'] = ds_fut['GPP'] * 86400
    ds_fut = ds_fut.sel(time=slice('2021', '2055'))
    
    gpp_fut_region = ds_fut['GPP'].where(ds_region['nca'] == nca_id)
    gpp_fut_climatology = gpp_fut_region.mean(dim=['lat', 'lon']).groupby('time.month').mean(dim='time')
    
    # Extract values and apply Spring-First reordering
    fut_values = gpp_fut_climatology.values
    reordered_fut = [fut_values[idx] for idx in spring_first_indices]
    
    line_color = combo_colors[(ssp, climate)]
    
    fut_line, = ax.plot(
        months_axis, reordered_fut,
        label=label, color=line_color, 
        linewidth=1.8, marker='o', markersize=4
    )
    legend_handles.append(fut_line)
    legend_labels.append(label)

# =====================================================================
# 5. FORMAT STYLING CONSTRAINTS 
# =====================================================================
gpp_units = ds_hist['GPP'].attrs.get('units', 'gC/m^2/d')

ax.set_title('S. Great Plains', fontsize=14, pad=10) 
ax.set_ylabel(r"Mean GPP ($\mathregular{gC/m^2/d}$)", fontsize=14)
ax.set_xticks(months_axis)
ax.set_xticklabels(month_names_spring_first, rotation=30, fontsize=14)
ax.tick_params(axis='y', labelsize=14)
ax.set_xlim(0.75, 12.25)

# Generate manual patch items for the calendar seasonal markers inside the legend
spring_patch = mpatches.Patch(facecolor='green', alpha=0.05, label='Spring (MAM)')
summer_patch = mpatches.Patch(facecolor='red', alpha=0.05, label='Summer (JJA)')
autumn_patch = mpatches.Patch(facecolor='orange', alpha=0.05, label='Autumn (SON)')
winter_patch = mpatches.Patch(facecolor='blue', alpha=0.05, label='Winter (DJF)')

# Append structural parameters together cleanly
all_handles = legend_handles + [spring_patch, summer_patch, autumn_patch, winter_patch]
all_labels = legend_labels #+ ['Spring (MAM)', 'Summer (JJA)', 'Autumn (SON)', 'Winter (DJF)']

# Draw clean consolidated outline box legend
ax.legend(
    handles=all_handles,
    labels=all_labels,
    loc='upper right',
    fontsize=14,         
    frameon=True,
    edgecolor='black',
    facecolor='white',
    ncol=1
)

plt.tight_layout()
out_fig_name = r'{filepath}/gpp_climatology_formatted_sgp.png'
plt.savefig(out_fig_name, dpi=300, bbox_inches='tight')
plt.show()


##################################################################################### plot (b)


import xarray as xr
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==========================================
# 1. Configuration & Base Maps
# ==========================================
path = '/filepath/'

# Load the NCA region map (already on -180 to 180 grid)
ds_nca = xr.open_dataset(f'{path}clm_state_nca_area_lon180.nc')
nca_map = ds_nca['nca'].load()

unique_regions = np.unique(nca_map.values)
unique_regions = [int(r) for r in unique_regions if not np.isnan(r)]
unique_regions.sort()

# Master nested storage for the final 12-month curves
# Structure: monthly_relative_changes[region_id][scenario_label] = numpy array of length 12
monthly_relative_changes = {r: {} for r in unique_regions}

# ==========================================
# 2. Process Historical Monthly Base Data
# ==========================================
print("Processing historical monthly soil moisture baseline...")
ds_sm_hist = xr.open_dataset(f'{path}/SM_1981-2015.nc')

# Fix longitude convention mapping and group by month over the 35-year window
ds_sm_hist = ds_sm_hist.assign_coords(lon=(((ds_sm_hist.lon + 180) % 360) - 180)).sortby('lon')
sm_hist_monthly_mean = ds_sm_hist['SOILLIQ_SUM'].groupby('time.month').mean(dim='time').load()

ds_area_hist = xr.open_dataset(f'{path}/wheat_area_hist_1981-2015.nc')
area_hist_static = ds_area_hist['area'].mean(dim='time').load()

# Pre-calculate the static historical baseline map per region
hist_regional_base = {}
for r_id in unique_regions:
    sm_region = sm_hist_monthly_mean.where(nca_map == r_id)
    area_region = area_hist_static.where(nca_map == r_id)
    
    weighted_sum = (sm_region * area_region).sum(dim=['lat', 'lon'])
    total_area = area_region.sum(dim=['lat', 'lon'])
    
    # Store the 12 absolute baseline numbers for this region
    hist_regional_base[r_id] = (weighted_sum / total_area.where(total_area > 0)).values

# ==========================================
# 3. Future Scenarios Execution Loops & Relative Change Math
# ==========================================
scenario_pairs = [('3', '45'), ('5', '85')]

for period in ['nf']:
    for ssp, rcp in scenario_pairs:
        for model in ['c', 'h']:
            model_full = 'hotter' if model == 'h' else 'cooler'
            yr_start, yr_end = 2021, 2055
            
            # Reconstruct string identifiers pointing to our new SM files
            sm_file = f'SM_{period}_{ssp}_{rcp}_{model}_{yr_start}-{yr_end}.nc'
            area_file = f'wheat_area_ssp{ssp}_rcp{rcp}_{model_full}_2021-2055.nc'
            scen_label = f"{period.upper()} SSP{ssp}-RCP{rcp} ({model_full})"
            
            print(f"Calculating relative monthly change for: {scen_label}...")
            
            # Load and fix longitude ranges
            ds_sm_future = xr.open_dataset(f'{path}/{sm_file}')
            ds_sm_future = ds_sm_future.assign_coords(lon=(((ds_sm_future.lon + 180) % 360) - 180)).sortby('lon')
            sm_future_monthly_mean = ds_sm_future['SOILLIQ_SUM'].groupby('time.month').mean(dim='time').load()
            
            ds_area_future = xr.open_dataset(f'{path}/{area_file}')
            area_future_static = ds_area_future['area'].mean(dim='time').load()
            
            for r_id in unique_regions:
                f_sm_region = sm_future_monthly_mean.where(nca_map == r_id)
                f_area_region = area_future_static.where(nca_map == r_id)
                
                f_weighted_sum = (f_sm_region * f_area_region).sum(dim=['lat', 'lon'])
                f_total_area = f_area_region.sum(dim=['lat', 'lon'])
                
                # Absolute future mean for the 12 months
                future_absolute = (f_weighted_sum / f_total_area.where(f_total_area > 0)).values
                historical_absolute = hist_regional_base[r_id]

                with np.errstate(divide='ignore', invalid='ignore'):
                    relative_change = ((future_absolute - historical_absolute) / historical_absolute) * 100.0
                
                # Save calculation arrays
                monthly_relative_changes[r_id][scen_label] = relative_change
            
            # Release cached datasets
            ds_sm_future.close()
            ds_area_future.close()
            
spring_first_indices = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 0, 1]
month_names_spring_first = ['Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb']
months_axis = np.arange(1, 13)

combo_colors = {
    ('3', 'c'): '#aec7e8',  # Light Blue
    ('3', 'h'): '#1f77b4',  # Dark Blue
    ('5', 'c'): '#ffbb78',  # Light Orange
    ('5', 'h'): '#ff7f0e'   # Dark Orange
}


desired_order_ids   = [ 6, 5, 8, 1, 2, 7,  4]
desired_order_names = ['S. Great Plains', 'N. Great Plains', 'Northwest', 'Northeast', 'Southeast', 'Southwest', 'Midwest']
nca_name_map = dict(zip(desired_order_ids, desired_order_names))

sgp_id = 6  # Southern Great Plains region ID

if sgp_id in monthly_relative_changes:
    print(f"\nGenerating focused single-panel plot for {nca_name_map[sgp_id]}...")
    
    # Initialize a new independent figure container
    fig_sgp, ax_sgp = plt.subplots(figsize=(7, 5.5))
    sgp_data = monthly_relative_changes[sgp_id]
    
    # 1. Apply Shifted Seasonal Shading Maps (Spring-First Matrix Tracking)
    ax_sgp.axvspan(0.5, 3.5, color='green', alpha=0.05)
    ax_sgp.axvspan(3.5, 6.5, color='red', alpha=0.05)
    ax_sgp.axvspan(6.5, 9.5, color='orange', alpha=0.05)
    ax_sgp.axvspan(9.5, 12.5, color='blue', alpha=0.05)
    
    # Absolute zero balance baseline line
    ax_sgp.axhline(0, color='black', linestyle='-', linewidth=1.5, alpha=0.8)
    
    # 2. Trace Scenario Curves with Coordinated Array Values
    for ssp, rcp in scenario_pairs:
        for model in ['c', 'h']:
            model_full = 'hotter' if model == 'h' else 'cooler'
            storage_label = f"NF SSP{ssp}-RCP{rcp} ({model_full})"
            plot_legend_label = f"atm{rcp}{model_full}_ssp{ssp}"
            
            relative_values = sgp_data.get(storage_label, None)
            
            if relative_values is not None and not np.isnan(relative_values).all():
                line_color = combo_colors[(ssp, model)]
                # Reorder to match: Mar -> Feb timeline
                reordered_values = [relative_values[idx] for idx in spring_first_indices]
                
                ax_sgp.plot(
                    months_axis, 
                    reordered_values, 
                    label=plot_legend_label, 
                    color=line_color, 
                    linewidth=1.8,  # Synced with master figure
                    marker='o', 
                    markersize=4    # Synced with master figure
                )
                
    # 3. Structural Axes Layout Configurations (All fontsizes synced to master)
    region_title = nca_name_map.get(sgp_id, f"Region {sgp_id:02d}")
    ax_sgp.set_title(region_title, fontsize=14, pad=10)
    ax_sgp.set_ylabel("Relative SM Change (%)", fontsize=14)
    
    ax_sgp.set_xticks(months_axis)
    ax_sgp.set_xticklabels(month_names_spring_first, rotation=30, fontsize=14)
    ax_sgp.set_xlim(0.75, 12.25)
    
    ax_sgp.tick_params(axis='y', labelsize=14)
    
    # Position clear descriptive legend matching the master panel's fontsize exactly
    ax_sgp.legend(
        loc='upper right', 
        bbox_to_anchor=(0.6, 0.99), 
        fontsize=14, 
        frameon=True, 
        edgecolor='black', 
        facecolor='white'
    )
    
    plt.tight_layout()

    sgp_fig_path = f'{path}/sm_S_Great_Plains_only.png'
    plt.show()
else:
    print(f"\nError: Data array key indicator index {sgp_id} not available in processed maps matrix.")