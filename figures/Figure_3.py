import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import numpy as np

sns.set_style("ticks")


models = ['cooler', 'hotter']
area_df = pd.read_csv('drought_area_by_conus_nca_hist+nearfuture_withclimateonly_timeseries.csv')
intensity_df = pd.read_csv('drought_intensity_by_conus_nca_hist+future_withclimateonly_timeseries.csv')

area_dfs = {model: area_df[area_df['scenario'].str.endswith(f'-NF-{model}') | (area_df['scenario'] == 'hist')].copy() for model in models}
intensity_dfs = {model: intensity_df[intensity_df['scenario'].str.endswith(f'-NF-{model}') | (intensity_df['scenario'] == 'hist')].copy() for model in models}

region_abbrev = {'CONUS': 'CONUS', 'Northeast': 'NE', 'Southeast': 'SE', 'Midwest': 'MW',
                 'N. Great Plains': 'NGP', 'S. Great Plains': 'SGP', 'Northwest': 'NW', 'Southwest': 'SW'}
region_order = ['CONUS', 'MW', 'NGP', 'SGP', 'NW', 'SW', 'SE', 'NE']

def plot_drought_area_intensity_compact(crop, area_dfs, intensity_dfs, region_abbrev, region_order,
                                        exclude_regions, output_file, add_legend=False):

    fig, axes = plt.subplots(1, 2, figsize=(14, 3.6), sharex=True)
    fig.text(0.003, 0.5, crop.capitalize(), fontsize=18, va='center', ha='center', rotation='vertical')

    if crop == 'corn':
        labels = ['(a1)', '(b1)']
    elif crop == 'wheat':
        labels = ['(a2)', '(b2)']
    elif crop == 'soybean':
        labels = ['(a3)', '(b3)']

    dfs = [
        {model: area_dfs[model][area_dfs[model]['crop'] == crop].copy() for model in models},
        {model: intensity_dfs[model][intensity_dfs[model]['crop'] == crop].copy() for model in models}
    ]
    titles = ['Drought-Exposed Area (% of CONUS Planted)', 'Drought Intensity (/month)']
    value_cols = ['area_in_drought(% of planted)', 'drought_intensity']

    scenario_groups = ['hist', 'RCP-only', 'RCP+SSP']
    colors = {'hist': 'darkgrey', 'RCP-only': 'green', 'RCP+SSP': 'orange'}

    for ax, df_dict, title, value_col, label in zip(axes, dfs, titles, value_cols, labels):
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

        # Plotting
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

        # Compact styling
        if crop == 'corn':
            ax.set_title(title, fontsize=16, pad=10)
        else:
            ax.set_title("", fontsize=16)
        ax.set_xlabel(''); ax.set_ylabel('')
        ax.set_xticks(range(len(region_order)))
        ax.set_xticklabels(region_order)
        ax.tick_params(axis='x', rotation=0, labelsize=14)
        ax.tick_params(axis='y', labelsize=15)
        ax.text(0.88, 0.92, label, transform=ax.transAxes, fontsize=18, va='top', ha='left')

        if "Area" in title:
            ax.set_ylim(0, 80)
        else:
            ax.set_ylim(0.5, 2.5)
            ax.yaxis.set_major_locator(plt.FixedLocator([0.5, 1.0, 1.5, 2.0, 2.5]))
            ax.yaxis.set_major_formatter(plt.FixedFormatter(['0.5', '1.0', '1.5', '2.0', '2.5']))

    if add_legend:
        color_elements = [
            Rectangle((0,0),1,1, fc=colors[s], ec='black', lw=0.8, alpha=0.9, label=l)
            for s, l in zip(scenario_groups, ['Historical', 'RCP-only', 'RCP+SSP'])
        ]
        
        legend_ax = fig.add_axes([0, 0, 0.01, 0.01])  
        legend_ax.set_xlim(0,1); legend_ax.set_ylim(0,1)
        legend_ax.axis('off')
        
        eb = legend_ax.errorbar(0.5, 0.5, yerr=0.25,
                                color='black', capsize=3, capthick=1.2, lw=1.2,
                                fmt='none') 
        
        eb_handle = eb
        
        fig.legend(handles=color_elements + [eb_handle],
                   labels=['Historical', 'ATM-only', 'ATM+LAND', 'Range across 4 scenarios'],
                   loc='lower center', bbox_to_anchor=(0.5, -0.1),
                   ncol=4, fontsize=15, frameon=False,
                   handlelength=2.2, handletextpad=0.4, columnspacing=1.6)
        
        legend_ax.remove()  
    
    

    plt.subplots_adjust(left=0.06, right=0.98, top=0.88, bottom=0.18, wspace=0.1)
    plt.savefig(output_file, bbox_inches='tight', dpi=400)
    plt.show()


plot_drought_area_intensity_compact('corn', area_dfs, intensity_dfs, region_abbrev, region_order,
                                    exclude_regions=['NW', 'SW'],
                                    output_file='corn.png')


plot_drought_area_intensity_compact('soybean', area_dfs, intensity_dfs, region_abbrev, region_order,
                                    exclude_regions=['NW', 'SW'],
                                    output_file='soybean.png',
                                    add_legend=True)
