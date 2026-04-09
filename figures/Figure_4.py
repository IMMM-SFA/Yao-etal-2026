import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

nca_id_list = [0,7,8,6,5,4,2,1]  # CONUS as ID 0
nca_name = ['CONUS', 'SW', 'NW', 'SGP',	'NGP', 'MW', 'SE', 'NE']  

nca_df = pd.DataFrame({'nca_id': nca_id_list, 'nca_name': nca_name})

nca_mapping_path = 'state_nca_mapping.csv'
nca_mapping = pd.read_csv(nca_mapping_path)
future_path = '/future/'
hist_path = '/hist/'
climate_change_only_path = '/climate_change_only/'

# Store data for all crops
crop_data = {}
for crop in ['corn', 'wheat', 'soybean']:
    print(f"Processing crop: {crop}")
    df_hist = pd.read_csv(f'{hist_path}{crop}_production_loss_hist_cl100.csv')
    df_hist = df_hist.merge(nca_mapping, on='state_id', how='left')
    df_hist_per_year = df_hist.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']]

    for segment in ['nf']:
        segtime = '2021-2055' if segment == 'nf' else '2061-2095'
        yeardif = 40 if segment == 'nf' else 80

        df_345c = pd.read_csv(f'{future_path}{crop}_production_loss_{segment}_3_45_c_{segtime}.csv')
        df_345h = pd.read_csv(f'{future_path}{crop}_production_loss_{segment}_3_45_h_{segtime}.csv')
        df_345c = df_345c.merge(nca_mapping, on='state_id', how='left')
        df_345h = df_345h.merge(nca_mapping, on='state_id', how='left')
        df_345c['Year'] = df_345c['Year'] - yeardif
        df_345h['Year'] = df_345h['Year'] - yeardif
        df_345c_per_year = df_345c.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']]
        df_345h_per_year = df_345h.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']]

        df_45c = pd.read_csv(f'{climate_change_only_path}{crop}_production_loss_{segment}_45_c_{segtime}.csv')
        df_45h = pd.read_csv(f'{climate_change_only_path}{crop}_production_loss_{segment}_45_h_{segtime}.csv')
        df_45c = df_45c.merge(nca_mapping, on='state_id', how='left')
        df_45h = df_45h.merge(nca_mapping, on='state_id', how='left')
        df_45c['Year'] = df_345c['Year']
        df_45h['Year'] = df_345h['Year']
        df_45c_per_year = df_45c.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']]
        df_45h_per_year = df_45h.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']]

        df_585c = pd.read_csv(f'{future_path}{crop}_production_loss_{segment}_5_85_c_{segtime}.csv')
        df_585h = pd.read_csv(f'{future_path}{crop}_production_loss_{segment}_5_85_h_{segtime}.csv')
        df_585c = df_585c.merge(nca_mapping, on='state_id', how='left')
        df_585h = df_585h.merge(nca_mapping, on='state_id', how='left')
        df_585c['Year'] = df_585c['Year'] - yeardif
        df_585h['Year'] = df_585h['Year'] - yeardif
        df_585c_per_year = df_585c.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']]
        df_585h_per_year = df_585h.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']]

        df_85c = pd.read_csv(f'{climate_change_only_path}{crop}_production_loss_{segment}_85_c_{segtime}.csv')
        df_85h = pd.read_csv(f'{climate_change_only_path}{crop}_production_loss_{segment}_85_h_{segtime}.csv')
        df_85c = df_85c.merge(nca_mapping, on='state_id', how='left')
        df_85h = df_85h.merge(nca_mapping, on='state_id', how='left')
        df_85c['Year'] = df_585c['Year']
        df_85h['Year'] = df_585h['Year']
        df_85c_per_year = df_85c.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']].reset_index()
        df_85h_per_year = df_85h.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']].reset_index()

        df_hist345c_per_year = pd.merge(df_hist_per_year.rename(columns={'Production_Loss(ton)': 'Hist_Production_Loss'}),
                                        df_345c_per_year.rename(columns={'Production_Loss(ton)': 'Future_345c_Production_Loss'}),
                                        on=['nca_id', 'Year'], how='inner')
        df_hist345h_per_year = pd.merge(df_hist_per_year.rename(columns={'Production_Loss(ton)': 'Hist_Production_Loss'}),
                                        df_345h_per_year.rename(columns={'Production_Loss(ton)': 'Future_345h_Production_Loss'}),
                                        on=['nca_id', 'Year'], how='inner')

        df_hist345c_per_year = pd.merge(df_hist345c_per_year,
                                        df_45c_per_year.rename(columns={'Production_Loss(ton)': 'Climate_45c_Production_Loss'}),
                                        on=['nca_id', 'Year'], how='inner')
        df_hist345h_per_year = pd.merge(df_hist345h_per_year,
                                        df_45h_per_year.rename(columns={'Production_Loss(ton)': 'Climate_45h_Production_Loss'}),
                                        on=['nca_id', 'Year'], how='inner')

        df_hist585c_per_year = pd.merge(df_hist_per_year.rename(columns={'Production_Loss(ton)': 'Hist_Production_Loss'}),
                                        df_585c_per_year.rename(columns={'Production_Loss(ton)': 'Future_585c_Production_Loss'}),
                                        on=['nca_id', 'Year'], how='inner')
        df_hist585c_per_year = pd.merge(df_hist585c_per_year,
                                        df_85c_per_year.rename(columns={'Production_Loss(ton)': 'Climate_85c_Production_Loss'}),
                                        on=['nca_id', 'Year'], how='inner')

        df_hist585h_per_year = pd.merge(df_hist_per_year.rename(columns={'Production_Loss(ton)': 'Hist_Production_Loss'}),
                                        df_585h_per_year.rename(columns={'Production_Loss(ton)': 'Future_585h_Production_Loss'}),
                                        on=['nca_id', 'Year'], how='inner')
        df_hist585h_per_year = pd.merge(df_hist585h_per_year,
                                        df_85h_per_year.rename(columns={'Production_Loss(ton)': 'Climate_85h_Production_Loss'}),
                                        on=['nca_id', 'Year'], how='inner')

        # Aggregate to mean annual per nca_id
        df_mean_345c = df_hist345c_per_year.groupby('nca_id').mean(numeric_only=True).reset_index()
        df_mean_345h = df_hist345h_per_year.groupby('nca_id').mean(numeric_only=True).reset_index()
        df_mean_585c = df_hist585c_per_year.groupby('nca_id').mean(numeric_only=True).reset_index()
        df_mean_585h = df_hist585h_per_year.groupby('nca_id').mean(numeric_only=True).reset_index()

        # Reindex to include all nca_ids (excluding CONUS initially)
        all_nca_ids = pd.DataFrame({'nca_id': nca_id_list[1:]})  # Exclude CONUS (0)
        df_mean_345c = all_nca_ids.merge(df_mean_345c, on='nca_id', how='left').fillna({'Hist_Production_Loss': 0, 'Future_345c_Production_Loss': 0, 'Climate_45c_Production_Loss': 0})
        df_mean_345h = all_nca_ids.merge(df_mean_345h, on='nca_id', how='left').fillna({'Hist_Production_Loss': 0, 'Future_345h_Production_Loss': 0, 'Climate_45h_Production_Loss': 0})
        df_mean_585c = all_nca_ids.merge(df_mean_585c, on='nca_id', how='left').fillna({'Hist_Production_Loss': 0, 'Future_585c_Production_Loss': 0, 'Climate_85c_Production_Loss': 0})
        df_mean_585h = all_nca_ids.merge(df_mean_585h, on='nca_id', how='left').fillna({'Hist_Production_Loss': 0, 'Future_585h_Production_Loss': 0, 'Climate_85h_Production_Loss': 0})

        # Calculate CONUS-level metrics
        conus_row_345c = {
            'nca_id': 0,
            'nca_name': 'CONUS',
            'Hist_Production_Loss': df_mean_345c['Hist_Production_Loss'].sum(),
            'Future_345c_Production_Loss': df_mean_345c['Future_345c_Production_Loss'].sum(),
            'Climate_45c_Production_Loss': df_mean_345c['Climate_45c_Production_Loss'].sum()
        }
        conus_row_345h = {
            'nca_id': 0,
            'nca_name': 'CONUS',
            'Hist_Production_Loss': df_mean_345h['Hist_Production_Loss'].sum(),
            'Future_345h_Production_Loss': df_mean_345h['Future_345h_Production_Loss'].sum(),
            'Climate_45h_Production_Loss': df_mean_345h['Climate_45h_Production_Loss'].sum()
        }
        conus_row_585c = {
            'nca_id': 0,
            'nca_name': 'CONUS',
            'Hist_Production_Loss': df_mean_585c['Hist_Production_Loss'].sum(),
            'Future_585c_Production_Loss': df_mean_585c['Future_585c_Production_Loss'].sum(),
            'Climate_85c_Production_Loss': df_mean_585c['Climate_85c_Production_Loss'].sum()
        }
        conus_row_585h = {
            'nca_id': 0,
            'nca_name': 'CONUS',
            'Hist_Production_Loss': df_mean_585h['Hist_Production_Loss'].sum(),
            'Future_585h_Production_Loss': df_mean_585h['Future_585h_Production_Loss'].sum(),
            'Climate_85h_Production_Loss': df_mean_585h['Climate_85h_Production_Loss'].sum()
        }

        # Append CONUS rows
        df_mean_345c = pd.concat([pd.DataFrame([conus_row_345c]), df_mean_345c], ignore_index=True)
        df_mean_345h = pd.concat([pd.DataFrame([conus_row_345h]), df_mean_345h], ignore_index=True)
        df_mean_585c = pd.concat([pd.DataFrame([conus_row_585c]), df_mean_585c], ignore_index=True)
        df_mean_585h = pd.concat([pd.DataFrame([conus_row_585h]), df_mean_585h], ignore_index=True)

        # Calculate impacts
        df_mean_345c['Total_Impact'] = df_mean_345c['Future_345c_Production_Loss'] - df_mean_345c['Hist_Production_Loss']
        df_mean_345c['Climate_Contribution'] = df_mean_345c['Climate_45c_Production_Loss'] - df_mean_345c['Hist_Production_Loss']
        df_mean_345c['LULCC_Contribution'] = df_mean_345c['Future_345c_Production_Loss'] - df_mean_345c['Climate_45c_Production_Loss']
        df_mean_345h['Total_Impact'] = df_mean_345h['Future_345h_Production_Loss'] - df_mean_345h['Hist_Production_Loss']
        df_mean_345h['Climate_Contribution'] = df_mean_345h['Climate_45h_Production_Loss'] - df_mean_345h['Hist_Production_Loss']
        df_mean_345h['LULCC_Contribution'] = df_mean_345h['Future_345h_Production_Loss'] - df_mean_345h['Climate_45h_Production_Loss']
        df_mean_585c['Total_Impact'] = df_mean_585c['Future_585c_Production_Loss'] - df_mean_585c['Hist_Production_Loss']
        df_mean_585c['Climate_Contribution'] = df_mean_585c['Climate_85c_Production_Loss'] - df_mean_585c['Hist_Production_Loss']
        df_mean_585c['LULCC_Contribution'] = df_mean_585c['Future_585c_Production_Loss'] - df_mean_585c['Climate_85c_Production_Loss']
        df_mean_585h['Total_Impact'] = df_mean_585h['Future_585h_Production_Loss'] - df_mean_585h['Hist_Production_Loss']
        df_mean_585h['Climate_Contribution'] = df_mean_585h['Climate_85h_Production_Loss'] - df_mean_585h['Hist_Production_Loss']
        df_mean_585h['LULCC_Contribution'] = df_mean_585h['Future_585h_Production_Loss'] - df_mean_585h['Climate_85h_Production_Loss']

        # Merge nca_name into DataFrames before normalization
        df_mean_345c = df_mean_345c.drop(columns=['nca_name'], errors='ignore').merge(nca_df, on='nca_id', how='left')
        df_mean_345h = df_mean_345h.drop(columns=['nca_name'], errors='ignore').merge(nca_df, on='nca_id', how='left')
        df_mean_585c = df_mean_585c.drop(columns=['nca_name'], errors='ignore').merge(nca_df, on='nca_id', how='left')
        df_mean_585h = df_mean_585h.drop(columns=['nca_name'], errors='ignore').merge(nca_df, on='nca_id', how='left')

        # Normalize impacts by CONUS historical production loss
        CONUS_Hist_Production_Loss = df_mean_345c.loc[df_mean_345c['nca_id'] == 0, 'Hist_Production_Loss'].iloc[0]
        print(f"{crop} CONUS Historical Loss: {CONUS_Hist_Production_Loss}")

        df_mean_345c['Total_Impact_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                       (df_mean_345c['Total_Impact'] / CONUS_Hist_Production_Loss) * 100,
                                                       np.nan)
        df_mean_345c['Climate_Contribution_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                              (df_mean_345c['Climate_Contribution'] / CONUS_Hist_Production_Loss) * 100,
                                                              np.nan)
        df_mean_345c['LULCC_Contribution_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                             (df_mean_345c['LULCC_Contribution'] / CONUS_Hist_Production_Loss) * 100,
                                                             np.nan)

        df_mean_345h['Total_Impact_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                       (df_mean_345h['Total_Impact'] / CONUS_Hist_Production_Loss) * 100,
                                                       np.nan)
        df_mean_345h['Climate_Contribution_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                              (df_mean_345h['Climate_Contribution'] / CONUS_Hist_Production_Loss) * 100,
                                                              np.nan)
        df_mean_345h['LULCC_Contribution_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                             (df_mean_345h['LULCC_Contribution'] / CONUS_Hist_Production_Loss) * 100,
                                                             np.nan)

        df_mean_585c['Total_Impact_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                       (df_mean_585c['Total_Impact'] / CONUS_Hist_Production_Loss) * 100,
                                                       np.nan)
        df_mean_585c['Climate_Contribution_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                              (df_mean_585c['Climate_Contribution'] / CONUS_Hist_Production_Loss) * 100,
                                                              np.nan)
        df_mean_585c['LULCC_Contribution_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                             (df_mean_585c['LULCC_Contribution'] / CONUS_Hist_Production_Loss) * 100,
                                                             np.nan)

        df_mean_585h['Total_Impact_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                       (df_mean_585h['Total_Impact'] / CONUS_Hist_Production_Loss) * 100,
                                                       np.nan)
        df_mean_585h['Climate_Contribution_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                              (df_mean_585h['Climate_Contribution'] / CONUS_Hist_Production_Loss) * 100,
                                                              np.nan)
        df_mean_585h['LULCC_Contribution_Scaled'] = np.where(CONUS_Hist_Production_Loss != 0,
                                                             (df_mean_585h['LULCC_Contribution'] / CONUS_Hist_Production_Loss) * 100,
                                                             np.nan)

        # Apply region exclusions for non-CONUS regions
        if crop in ['corn', 'soybean']:
            exclude_nca_ids = [8, 7]  # Northwest, Southwest
            for df in [df_mean_345c, df_mean_345h, df_mean_585c, df_mean_585h]:
                df.loc[df['nca_id'].isin(exclude_nca_ids), ['Total_Impact_Scaled', 'Climate_Contribution_Scaled', 'LULCC_Contribution_Scaled']] = np.nan
        elif crop == 'wheat':
            exclude_nca_ids = [1]  # Northeast
            for df in [df_mean_345c, df_mean_345h, df_mean_585c, df_mean_585h]:
                df.loc[df['nca_id'].isin(exclude_nca_ids), ['Total_Impact_Scaled', 'Climate_Contribution_Scaled', 'LULCC_Contribution_Scaled']] = np.nan

        # Ensure DataFrame order matches nca_id_list
        df_mean_345c = df_mean_345c.set_index('nca_id').reindex(nca_id_list).reset_index()
        df_mean_345h = df_mean_345h.set_index('nca_id').reindex(nca_id_list).reset_index()
        df_mean_585c = df_mean_585c.set_index('nca_id').reindex(nca_id_list).reset_index()
        df_mean_585h = df_mean_585h.set_index('nca_id').reindex(nca_id_list).reset_index()

        # Store data for plotting
        crop_data[crop] = {
            'df_mean_345c': df_mean_345c,
            'df_mean_345h': df_mean_345h,
            'df_mean_585c': df_mean_585c,
            'df_mean_585h': df_mean_585h,
            'CONUS_Hist_Production_Loss': CONUS_Hist_Production_Loss
        }

# Plotting for mean of cooler and hotter variants
fig, axes = plt.subplots(1, 3, figsize=(19, 8.5))

desired_order_ids   = [1, 2, 7, 8, 6, 5, 4, 0]
desired_order_names = ['NE', 'SE', 'SW', 'NW', 'SGP', 'NGP', 'MW', 'CONUS']
panel_labels = ['(a)', '(b)', '(c)']
for idx, crop in enumerate(['corn', 'wheat', 'soybean']):
    ax = axes[idx]

    # Extract the 4 original (non-averaged) scaled contributions
    df1 = crop_data[crop]['df_mean_345c']   
    df2 = crop_data[crop]['df_mean_345h']   
    df3 = crop_data[crop]['df_mean_585c'] 
    df4 = crop_data[crop]['df_mean_585h']   

    # Stack the four climate and LULCC values per region
    climate_vals = np.stack([
        df1['Climate_Contribution_Scaled'].fillna(np.nan),
        df2['Climate_Contribution_Scaled'].fillna(np.nan),
        df3['Climate_Contribution_Scaled'].fillna(np.nan),
        df4['Climate_Contribution_Scaled'].fillna(np.nan)
    ], axis=1)  

    lulcc_vals = np.stack([
        df1['LULCC_Contribution_Scaled'].fillna(np.nan),
        df2['LULCC_Contribution_Scaled'].fillna(np.nan),
        df3['LULCC_Contribution_Scaled'].fillna(np.nan),
        df4['LULCC_Contribution_Scaled'].fillna(np.nan)
    ], axis=1)

    # Compute mean, min, max across the 4 members
    climate_mean = np.nanmean(climate_vals, axis=1)
    climate_min  = np.nanmin(climate_vals, axis=1)
    climate_max  = np.nanmax(climate_vals, axis=1)

    lulcc_mean = np.nanmean(lulcc_vals, axis=1)
    lulcc_min  = np.nanmin(lulcc_vals, axis=1)
    lulcc_max  = np.nanmax(lulcc_vals, axis=1)

 
    df_plot = pd.DataFrame({
        'nca_id': df1['nca_id'],
        'nca_name': df1['nca_name'],
        'Climate_mean': climate_mean,
        'Climate_low':  climate_mean - climate_min,
        'Climate_high': climate_max - climate_mean,
        'LULCC_mean': lulcc_mean,
        'LULCC_low':  lulcc_mean - lulcc_min,
        'LULCC_high': lulcc_max - lulcc_mean,
    }).set_index('nca_id').reindex(nca_id_list).reset_index()
    
    df_plot = df_plot.set_index('nca_id').loc[desired_order_ids].reset_index()
    # Apply exclusions (set both mean and error to NaN)
    if crop in ['corn', 'soybean']:
        exclude = [7, 8]   # SW, NW
    elif crop == 'wheat':
        exclude = [1]      # NE
    else:
        exclude = []
    df_plot.loc[df_plot['nca_id'].isin(exclude),
                ['Climate_mean','Climate_low','Climate_high',
                 'LULCC_mean','LULCC_low','LULCC_high']] = np.nan

    valid = df_plot[['Climate_mean', 'LULCC_mean']].notna().any(axis=1)

    y = np.arange(len(nca_name)) * 1.9
    bar_height = 0.55

    # === Plot bars + error bars ===
    # Climate bar (upper)
    bars1 = ax.barh(y[valid] + bar_height/2, df_plot.loc[valid, 'Climate_mean'],
                    height=bar_height, color='#FF6699', label='Climate' if idx==0 else "")
    # LULCC bar (lower)
    bars2 = ax.barh(y[valid] - bar_height/2, df_plot.loc[valid, 'LULCC_mean'],
                    height=bar_height, color='#009988', label='Land-Use' if idx==0 else "") 

    # Error bars (min–max range)
    ax.errorbar(df_plot.loc[valid, 'Climate_mean'], y[valid] + bar_height/2,
                xerr=[df_plot.loc[valid, 'Climate_low'], df_plot.loc[valid, 'Climate_high']],
                fmt='none', ecolor='black', capsize=3, capthick=1, linewidth=1.2)

    ax.errorbar(df_plot.loc[valid, 'LULCC_mean'], y[valid] - bar_height/2,
                xerr=[df_plot.loc[valid, 'LULCC_low'], df_plot.loc[valid, 'LULCC_high']],
                fmt='none', ecolor='black', capsize=3, capthick=1, linewidth=1.2)

    
    # Axis settings
    if crop == 'corn':
        ax.set_xlim(-12, 55)
    elif crop == 'wheat':
        ax.set_xlim(-40, 250)
    else:  # soybean
        ax.set_xlim(-12, 100)

    ax.set_ylim(-1, len(nca_name)*1.9 - 0.3)
    ax.set_yticks(y)
    ax.set_yticklabels(df_plot['nca_name'], fontsize=18.5, ha='right')
    ax.set_title(crop.capitalize(), fontsize=21, pad=20)
    ax.tick_params(axis='x', labelsize=18)
    ax.axvline(0, color='black', linewidth=1)
    ax.set_xlabel('Change in crop loss\n(% of CONUS historical)', fontsize=20)

    if idx == 0:
        err = ax.errorbar(999, 999, xerr=1,
                          color='black',
                          capsize=3,    
                          capthick=1.2,   
                          linewidth=1.2,
                          fmt='none', label='Scenario range')

        from matplotlib.patches import Patch
        p1 = Patch(facecolor='#FF6699', label='ΔATM')
        p2 = Patch(facecolor='#009988', label='LULCC')

        ax.legend(handles=[p1, p2, err],
                  loc='lower right',
                  fontsize=18,
                  frameon=False,
                  handlelength=1.6,
                  handletextpad=0.7)

    ax.text(
        0.98, 0.4, panel_labels[idx],
        transform=ax.transAxes,
        fontsize=24,
        ha='right', va='bottom',
        zorder=20,
        clip_on=False
    )    
# Final layout
plt.tight_layout(rect=[0, 0.02, 1, 0.96])
plt.savefig(f'{future_path}production_loss_contribution_2bars_with_range_errorbars.png',
            dpi=400, bbox_inches='tight')
plt.show()



