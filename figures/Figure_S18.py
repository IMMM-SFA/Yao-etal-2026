######################### plot a-c, please see the code for fig.2 
######################### plot d-f
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import numpy as np

sns.set_style("ticks")

# === 1. Loading the Data ===
models = ['cooler', 'hotter']

area_df = pd.read_csv('/filepath/drought_area_by_conus_nca_hist+nearfuture_withclimateonly_timeseries.csv')
intensity_df = pd.read_csv('/filepath/drought_intensity_by_conus_nca_hist+future_withclimateonly_timeseries.csv')
duration_df = pd.read_csv('/filepath/drought_timefrac_by_conus_nca_hist+future_withclimateonly_timeseries.csv')

area_dfs = {model: area_df[area_df['scenario'].str.endswith(f'-NF-{model}') | (area_df['scenario'] == 'hist')].copy() for model in models}
intensity_dfs = {model: intensity_df[intensity_df['scenario'].str.endswith(f'-NF-{model}') | (intensity_df['scenario'] == 'hist')].copy() for model in models}
duration_dfs = {model: duration_df[duration_df['scenario'].str.endswith(f'-NF-{model}') | (duration_df['scenario'] == 'hist')].copy() for model in models}

region_abbrev = {'CONUS': 'CONUS', 'Northeast': 'NE', 'Southeast': 'SE', 'Midwest': 'MW',
                 'N. Great Plains': 'NGP', 'S. Great Plains': 'SGP', 'Northwest': 'NW', 'Southwest': 'SW'}
region_order = ['CONUS', 'MW', 'NGP', 'SGP', 'NW', 'SW', 'SE', 'NE']

# === 2. Plotting Function ===
def plot_wheat_all_metrics(area_dfs, intensity_dfs, duration_dfs, region_abbrev, region_order,
                           exclude_regions, output_file):
    
    # 1 row, 3 columns for the 3 variables
    fig, axes = plt.subplots(1, 3, figsize=(20, 4.2))

    datasets = [area_dfs, intensity_dfs, duration_dfs]
    titles = ['Drought-Exposed Area\n(% of CONUS Planted)', 'Drought Intensity\n(/month)', 'Drought Duration\n(% of Growing Season)']
    
    value_cols = ['area_in_drought(% of planted)', 'drought_intensity', 'drought_duration(% of growing season)']
    labels = ['(d)', '(e)', '(f)']
    y_limits = [(0, 80), (0.5, 2.5), (30, 80)]

    scenario_groups = ['hist', 'RCP-only', 'RCP+SSP']
    colors = {'hist': 'darkgrey', 'RCP-only': 'green', 'RCP+SSP': 'orange'}

    for ax, source_dfs, title, value_col, label, ylim in zip(axes, datasets, titles, value_cols, labels, y_limits):
        
        df_dict = {model: source_dfs[model][source_dfs[model]['crop'] == 'wheat'].copy() for model in models}
        
        for model in models:
            df_dict[model]['region_abbrev'] = df_dict[model]['region_name'].map(region_abbrev)
            if exclude_regions:
                mask = df_dict[model]['region_abbrev'].isin(exclude_regions)
                df_dict[model].loc[mask, value_col] = np.nan

        member_stats = []
        for model in models:
            temp = df_dict[model].copy()
            temp['scenario_clean'] = temp['scenario'].str.replace(f'-NF-{model}', '', regex=True)
            temp['group'] = temp['scenario_clean'].map({
                'hist': 'hist',
                'RCP4.5': 'RCP-only', 'RCP8.5': 'RCP-only',
                'SSP3-4.5': 'RCP+SSP', 'SSP5-8.5': 'RCP+SSP'
            })
            stats = temp.groupby(['region_abbrev', 'group', 'scenario_clean'])[value_col].mean().reset_index()
            stats = stats.rename(columns={value_col: 'value'})
            member_stats.append(stats)

        all_members = pd.concat(member_stats, ignore_index=True)
        summary = (all_members.groupby(['region_abbrev', 'group'])
                              .agg(mean=('value', 'mean'), lower=('value', 'min'), upper=('value', 'max'))
                              .reset_index()
                              .rename(columns={'group': 'scenario'}))

        full_grid = pd.DataFrame([(r, s) for r in region_order for s in scenario_groups],
                                 columns=['region_abbrev', 'scenario'])
        summary = pd.merge(full_grid, summary, on=['region_abbrev', 'scenario'], how='left')
        summary['region_abbrev'] = pd.Categorical(summary['region_abbrev'], categories=region_order, ordered=True)
        summary = summary.sort_values(['region_abbrev', 'scenario']).reset_index(drop=True)

        # Draw the bars and error bars
        bar_width = 0.22
        for i, region in enumerate(region_order):
            region_data = summary[summary['region_abbrev'] == region]
            for j, scenario in enumerate(scenario_groups):
                row = region_data[region_data['scenario'] == scenario]
                mean_val = row['mean'].iloc[0] if not row.empty and pd.notna(row['mean'].iloc[0]) else 0.0
                lower = row['lower'].iloc[0] if not row.empty and pd.notna(row['lower'].iloc[0]) else mean_val
                upper = row['upper'].iloc[0] if not row.empty and pd.notna(row['upper'].iloc[0]) else mean_val
                x_pos = i + (j - 1) * bar_width

                ax.bar(x_pos, mean_val, bar_width,
                       color=colors[scenario], edgecolor='black', linewidth=0.8,
                       alpha=0.9 if mean_val > 0 else 0.0)

                if scenario != 'hist' and mean_val > 0:
                    ax.errorbar(x_pos, mean_val,
                                yerr=[[mean_val - lower], [upper - mean_val]],
                                color='black', capsize=3, capthick=1, linewidth=1.2)


        ax.set_ylabel(title, fontsize=18, labelpad=10) 
        ax.set_xticks(range(len(region_order)))
        ax.set_xticklabels(region_order)
        ax.tick_params(axis='x', rotation=0, labelsize=14.5)
        ax.tick_params(axis='y', labelsize=16)
        
        ax.text(0.22, 0.94, label, transform=ax.transAxes, fontsize=23, va='top', ha='left')
        
        ax.set_ylim(ylim)
        if "Intensity" in title:
            ax.yaxis.set_major_locator(plt.FixedLocator([0.5, 1.0, 1.5, 2.0, 2.5]))
            ax.yaxis.set_major_formatter(plt.FixedFormatter(['0.5', '1.0', '1.5', '2.0', '2.5']))

    # === 3. Legend (Inside the first plot) ===
    color_elements = [
        Rectangle((0,0),1,1, fc=colors[s], ec='black', lw=0.8, alpha=0.9, label=l)
        for s, l in zip(scenario_groups, ['Historical', 'ATM-only', 'ATM+LAND'])
    ]
    
    legend_ax = fig.add_axes([0, 0, 0.01, 0.01])  
    legend_ax.axis('off')
    eb = legend_ax.errorbar(0.3, 0.5, yerr=0.25, color='black', capsize=3, capthick=1.2, lw=1.2, fmt='none')
    
    axes[0].legend(handles=color_elements + [eb],
                   labels=['Historical', 'ATM-only', 'ATM+LAND', 'Scenario range'],
                   loc='upper right', 
                   ncol=1, fontsize=18, frameon=False,
                   handlelength=1.5, handletextpad=0.5,prop={'size': 16, 'weight': 'roman'})
    
    legend_ax.remove()

    plt.subplots_adjust(left=0.04, right=0.98, top=0.85, bottom=0.12, wspace=0.25)
    plt.savefig(output_file, bbox_inches='tight', dpi=400)
    plt.show()

# === 4. Execute ===
output_path = '/filepath/wheat_3panels.png'

plot_wheat_all_metrics(area_dfs=area_dfs, 
                       intensity_dfs=intensity_dfs, 
                       duration_dfs=duration_dfs, 
                       region_abbrev=region_abbrev, 
                       region_order=region_order,
                       exclude_regions=['NE'], 
                       output_file=output_path)


######################### plot g
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

nca_id_list = [0,7,8,6,5,4,2,1]  # CONUS as ID 0
nca_name = ['CONUS', 'SW', 'NW', 'SGP',	'NGP', 'MW', 'SE', 'NE']  


nca_df = pd.DataFrame({'nca_id': nca_id_list, 'nca_name': nca_name})

nca_mapping_path = '/filepath/state_nca_mapping.csv'
nca_mapping = pd.read_csv(nca_mapping_path)
future_path = '/filepath/'
hist_path = '/filepath/'
climate_change_only_path = '/filepath/'

# Store data for all crops
crop_data = {}
for crop in ['corn', 'wheat', 'soybean']:
# for crop in ['wheat']:
    print(f"Processing crop: {crop}")
    df_hist = pd.read_csv(f'{hist_path}{crop}_production_loss_hist_cl100.csv')
    df_hist = df_hist.merge(nca_mapping, on='state_id', how='left')
    df_hist_per_year = df_hist.groupby(['nca_id', 'Year']).sum(numeric_only=True)[['Production_Loss(ton)']]

    for segment in ['nf']:
        segtime = '2021-2055' if segment == 'nf' else '2061-2095'
        yeardif = 40 if segment == 'nf' else 80

        # SSP3 RCP4.5 data
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

        # SSP5 RCP8.5 data
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

        # Merges for SSP3 RCP4.5
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

        # Merges for SSP5 RCP8.5
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

        crop_data[crop] = {
            'df_mean_345c': df_mean_345c,
            'df_mean_345h': df_mean_345h,
            'df_mean_585c': df_mean_585c,
            'df_mean_585h': df_mean_585h,
            'CONUS_Hist_Production_Loss': CONUS_Hist_Production_Loss
        }



fig, ax = plt.subplots(1, 1, figsize=(5.2, 6))

desired_order_ids   = [1, 2, 7, 8, 6, 5, 4, 0]
desired_order_names = ['NE', 'SE', 'SW', 'NW', 'SGP', 'NGP', 'MW', 'CONUS']
crop = 'wheat'

# Extract the 4 original (non-averaged) scaled contributions
df1 = crop_data[crop]['df_mean_345c']   # SSP3-4.5 cooler
df2 = crop_data[crop]['df_mean_345h']   # SSP3-4.5 hotter
df3 = crop_data[crop]['df_mean_585c']   # SSP5-8.5 cooler
df4 = crop_data[crop]['df_mean_585h']   # SSP5-8.5 hotter

# Stack the four climate and LULCC values per region
climate_vals = np.stack([
    df1['Climate_Contribution_Scaled'].fillna(np.nan),
    df2['Climate_Contribution_Scaled'].fillna(np.nan),
    df3['Climate_Contribution_Scaled'].fillna(np.nan),
    df4['Climate_Contribution_Scaled'].fillna(np.nan)
], axis=1)  # shape: (8 regions, 4 members)

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
})
# Reindex and sort based on the desired order
df_plot = df_plot.set_index('nca_id').loc[desired_order_ids].reset_index()

# Apply exclusions for Wheat (NE region)
exclude = [1]      
df_plot.loc[df_plot['nca_id'].isin(exclude),
            ['Climate_mean','Climate_low','Climate_high',
             'LULCC_mean','LULCC_low','LULCC_high']] = np.nan

valid = df_plot[['Climate_mean', 'LULCC_mean']].notna().any(axis=1)

y = np.arange(len(desired_order_names)) * 1.9
bar_height = 0.55

# === Plot bars + error bars ===
# Climate bar (upper)
bars1 = ax.barh(y[valid] + bar_height/2, df_plot.loc[valid, 'Climate_mean'],
                height=bar_height, color='#FF6699', label='ΔATM')
# LULCC bar (lower)
bars2 = ax.barh(y[valid] - bar_height/2, df_plot.loc[valid, 'LULCC_mean'],
                height=bar_height, color='#009988', label='LULCC')

# Error bars (min–max range)
ax.errorbar(df_plot.loc[valid, 'Climate_mean'], y[valid] + bar_height/2,
            xerr=[df_plot.loc[valid, 'Climate_low'], df_plot.loc[valid, 'Climate_high']],
            fmt='none', ecolor='black', capsize=3, capthick=1, linewidth=1.2)

ax.errorbar(df_plot.loc[valid, 'LULCC_mean'], y[valid] - bar_height/2,
            xerr=[df_plot.loc[valid, 'LULCC_low'], df_plot.loc[valid, 'LULCC_high']],
            fmt='none', ecolor='black', capsize=3, capthick=1, linewidth=1.2)

# Axis settings for Wheat
ax.set_xlim(-40, 250)
ax.set_ylim(-1, len(desired_order_names)*1.9 - 0.3)
ax.set_yticks(y)
ax.set_yticklabels(df_plot['nca_name'], fontsize=18.5, ha='right')
# ax.set_title(crop.capitalize(), fontsize=21, pad=20)
ax.tick_params(axis='x', labelsize=18)
ax.axvline(0, color='black', linewidth=1)
ax.set_xlabel('Change in crop loss\n(% of CONUS historical)', fontsize=18) #, fontweight='bold'
ax.text(0.72, 0.54, "(g)", transform=ax.transAxes, fontsize=23, va='top', ha='left')
# Legend setup
err = ax.errorbar(999, 999, xerr=1, color='black', capsize=3, capthick=1.2, 
                  linewidth=1.2, fmt='none', label='Scenario range')

p1 = Patch(facecolor='#FF6699', label='ΔATM')
p2 = Patch(facecolor='#009988', label='LULCC')

ax.legend(handles=[p1, p2, err],
          loc='lower right',
          fontsize=18,
          frameon=False,
          handlelength=1.6,
          handletextpad=0.7)

# Final layout
plt.tight_layout(rect=[0, 0.02, 1, 0.96])
plt.savefig(f'{future_path}production_loss_contribution_wheat_only.tif',dpi=500, bbox_inches='tight')
plt.show()

######################### plot h
from mpl_toolkits.axes_grid1 import make_axes_locatable
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde

# state to NCA mapping CSV file
nca_mapping_path = '/filepath/state_nca_mapping.csv'  
nca_mapping = pd.read_csv(nca_mapping_path)


# Colorblind-friendly colors for crops
crop_colors = {
    'corn': '#4c78a8',  
    'wheat': '#f58518',  
    'soybean': '#009e73'  
}

plt.figure(figsize=(5.2, 6))

# Data path
path = '/filepath/'

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
fig = plt.figure(figsize=(5, 5.5))  
fig.set_facecolor('white')  
ax = plt.gca()
ax.set_facecolor('white')  
divider = make_axes_locatable(ax)
ax_top = divider.append_axes("top", size="40%", pad=0.0, sharex=ax)
ax_bottom = ax  # Bottom axis is the main axis
ax_top.spines['bottom'].set_visible(False)  
ax_bottom.spines['top'].set_visible(False)  

for crop in ['wheat']:
    ## near future
    df_345c_nf = pd.read_csv(f'{path}/{crop}_financial_loss_nf_3_45_c_2021-2055.csv')
    df_585c_nf = pd.read_csv(f'{path}/{crop}_financial_loss_nf_5_85_c_2021-2055.csv')
    df_345h_nf = pd.read_csv(f'{path}/{crop}_financial_loss_nf_3_45_h_2021-2055.csv')
    df_585h_nf = pd.read_csv(f'{path}/{crop}_financial_loss_nf_5_85_h_2021-2055.csv')
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
    # Calculate the relative change in financial loss for CONUS
    diff_h_nf_conus = (df_345h_conus_nf['Financial_Loss($)'] - df_585h_conus_nf['Financial_Loss($)']) / df_585h_conus_nf['Financial_Loss($)'] * 100
    diff_c_nf_conus = (df_345c_conus_nf['Financial_Loss($)'] - df_585c_conus_nf['Financial_Loss($)']) / df_585c_conus_nf['Financial_Loss($)'] * 100
    diff_nf_conus = (diff_c_nf_conus + diff_h_nf_conus)/2.0
    # Apply Kernel Density Estimation (KDE) for smoothing
    kde_nf_conus = gaussian_kde(diff_nf_conus, bw_method=0.1)
    x_nf_conus = np.linspace(min(diff_nf_conus), max(diff_nf_conus), 2000)
    pdf_nf_conus = kde_nf_conus.evaluate(x_nf_conus)
    cdf_nf_conus = np.cumsum(pdf_nf_conus) * (x_nf_conus[1] - x_nf_conus[0]) / np.max(np.cumsum(pdf_nf_conus) * (x_nf_conus[1] - x_nf_conus[0]))

    # Print y-value (CDF) at x=0 for CONUS
    y_conus_at_zero = np.interp(0, x_nf_conus, cdf_nf_conus)
    print(f"CONUS CDF at x=0 for {crop}: {y_conus_at_zero:.3f}")
    
    
    # Plot CONUS on both axes
    ax_top.plot(x_nf_conus, cdf_nf_conus, linestyle='-', color='black', linewidth=3, label='CONUS')
    ax_bottom.plot(x_nf_conus, cdf_nf_conus, linestyle='-', color='black', linewidth=3, label='CONUS')
    # Find x-value where CDF reaches y=0.99 for CONUS
    idx_conus = np.argmin(np.abs(cdf_nf_conus - 0.99))
    x_conus_99 = x_nf_conus[idx_conus]
    ax_top.vlines(x=x_conus_99, ymin=0.9, ymax=0.99, color='black', linestyle=':', linewidth=1.5, alpha=0.7)
    ax_bottom.vlines(x=x_conus_99, ymin=0, ymax=min(0.99, 0.9), color='black', linestyle=':', linewidth=1.5, alpha=0.7)
    # Iterate through each NCA and apply KDE for each NCA
    ax_bottom.text(x_conus_99 + 0, 0.015, f'{x_conus_99:.0f}', color='black', fontsize=12, ha='left', va='center', weight="bold")
    
    for nca_id in [4, 5, 6, 8]:
        diff_nf_nca = diff_nf.loc[nca_id].dropna()
        kde_nf = gaussian_kde(diff_nf_nca, bw_method=0.1)
        x_nf = np.linspace(min(diff_nf_nca), max(diff_nf_nca), 2000)
        pdf_nf = kde_nf.evaluate(x_nf)
        cdf_nf = np.cumsum(pdf_nf) * (x_nf[1] - x_nf[0]) / np.max(np.cumsum(pdf_nf) * (x_nf[1] - x_nf[0]))

        # Print y-value (CDF) at x=0 for this region
        y_nca_at_zero = np.interp(0, x_nf, cdf_nf)
        print(f"{region_names[nca_id]} CDF at x=0 for {crop}: {y_nca_at_zero:.3f}")
        
        # Plotting the CDF for the relative change in financial loss for each NCA
        ax_top.plot(x_nf, cdf_nf, linestyle='-', color=region_colors[nca_id], linewidth=2, label=f'{region_names[nca_id]}')
        ax_bottom.plot(x_nf, cdf_nf, linestyle='-', color=region_colors[nca_id], linewidth=2, label=f'{region_names[nca_id]}')
        # Find x-value where CDF reaches y=0.99 for this region
        idx_nca = np.argmin(np.abs(cdf_nf - 0.99))
        x_nca_99 = x_nf[idx_nca]
        ax_top.vlines(x=x_nca_99, ymin=0.9, ymax=0.99, color=region_colors[nca_id], linestyle=':', linewidth=1.5, alpha=0.7)
        ax_bottom.vlines(x=x_nca_99, ymin=0, ymax=min(0.99, 0.9), color=region_colors[nca_id], linestyle=':', linewidth=1.5, alpha=0.7)
        if nca_id == 6 or nca_id == 4:
            ax_bottom.text(x_nca_99-60 , 0.015, f'{x_nca_99:.0f}', color=region_colors[nca_id], fontsize=12, ha='left', va='center', weight="bold")
        elif nca_id == 8:
            ax_bottom.text(x_nca_99+10 , 0.015, f'{x_nca_99:.0f}', color=region_colors[nca_id], fontsize=12, ha='left', va='center', weight="bold")
        else:
            ax_bottom.text(x_nca_99 + 5, 0.015, f'{x_nca_99:.0f}', color=region_colors[nca_id], fontsize=12, ha='left', va='center', weight="bold")
        
# Final plot settings
ax_top.set_ylim(0.90, 1.0)  # Zoomed-in range for high probabilities
ax_bottom.set_ylim(0, 0.90)  # Lower range to align at y=0.9
ax_top.set_xlim(-100, 600)
ax_bottom.set_xlim(-100, 600)
ax_bottom.set_xlabel('atm45_ssp3 vs atm85_ssp5\nin Financial Loss (%)', fontsize=18)
fig.text(-0.001, 0.55, 'Cumulative Probability', rotation=90, ha='center', va='center', fontsize=18) 
fig.text(0.72, 0.6, '(h)', rotation=0, ha='center', va='center', fontsize=23)

ax_top.set_ylabel('', fontsize=14)  
ax_top.tick_params(axis='x', which='both', bottom=False, labelbottom=False)  
ax_top.set_yticks([0.95, 0.99])  
ax_bottom.set_yticks([0, 0.3, 0.6, 0.9])  
ax_top.tick_params(axis='y', labelsize=16)
ax_bottom.tick_params(axis='both', labelsize=14)
ax_top.grid(True, linestyle='--', alpha=0.7, which='major', axis='y')
ax_bottom.grid(True, linestyle='--', alpha=0.7, which='major', axis='y')
ax_top.axvline(x=0, color='gray', linestyle='--', linewidth=2, alpha=0.8)
ax_bottom.axvline(x=0, color='gray', linestyle='--', linewidth=2, alpha=0.8)
ax_bottom.legend(fontsize=16, loc='lower right', bbox_to_anchor=(0.94, 0.10), frameon=True, facecolor='white', framealpha=0.9, edgecolor='gray')

fig.tight_layout(pad=0.5)
plt.savefig(f'{path}/financial_loss_345diff585_wheat_mean.png', dpi=300, bbox_inches='tight')
