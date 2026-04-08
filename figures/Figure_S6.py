import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import numpy as np

sns.set_style("ticks")

models = ['cooler', 'hotter']
duration_df = pd.read_csv('drought_timefrac_by_conus_nca_hist+future_withclimateonly_timeseries.csv')
duration_dfs = {model: duration_df[duration_df['scenario'].str.endswith(f'-NF-{model}') | (duration_df['scenario'] == 'hist')].copy() for model in models}

region_abbrev = {'CONUS': 'CONUS', 'Northeast': 'NE', 'Southeast': 'SE', 'Midwest': 'MW',
                 'N. Great Plains': 'NGP', 'S. Great Plains': 'SGP', 'Northwest': 'NW', 'Southwest': 'SW'}
region_order = ['CONUS', 'MW', 'NGP', 'SGP', 'NW', 'SW', 'SE', 'NE']

all_crop_results = {}

def plot_drought_duration_only(duration_dfs, region_abbrev, region_order,
                               output_file, add_legend=False):
    """
    Plots only the Drought Duration panel for all three crops in one figure (1 row × 3 columns).
    Reuses as much logic as possible from the original function, but focuses on the duration metric.
    Excludes the same regions as in your original calls.
    """
    crops = ['corn', 'wheat', 'soybean']
    exclude_regions_list = [
        ['NW', 'SW'],  # for corn
        ['NE'],        # for wheat
        ['NW', 'SW']   # for soybean
    ]
    subplot_labels = ['(a)', '(b)', '(c)']  

    fig, axes = plt.subplots(1, 3, figsize=(20, 5), sharey=True)  # Share y-axis since all are duration

    title = 'Drought Duration (% of Growing Season)'
    value_col = 'drought_duration(% of growing season)'
    scenario_groups = ['hist', 'RCP-only', 'RCP+SSP']
    colors = {'hist': 'darkgrey', 'RCP-only': 'green', 'RCP+SSP': 'orange'}

    for ax, crop, exclude_regions, label in zip(axes, crops, exclude_regions_list, subplot_labels):
        df_dict = {model: duration_dfs[model][duration_dfs[model]['crop'] == crop].copy() for model in models}
        for model in models:
            df_dict[model]['region_abbrev'] = df_dict[model]['region_name'].map(region_abbrev)

        if exclude_regions:
            for model in models:
                mask = df_dict[model]['region_abbrev'].isin(exclude_regions)
                df_dict[model].loc[mask, value_col] = np.nan

        member_stats = []
        for model in models:
            temp = df_dict[model].copy()
            temp['scenario_clean'] = temp['scenario'].str.replace(f'-NF-{model}', '', regex=True)
            temp['group'] = temp['scenario_clean'].map({
                'hist': 'hist',
                'RCP4.5': 'RCP-only',
                'RCP8.5': 'RCP-only',
                'SSP3-4.5': 'RCP+SSP',
                'SSP5-8.5': 'RCP+SSP'
            })
            stats = temp.groupby(['region_abbrev', 'group', 'scenario_clean'])[value_col].mean().reset_index()
            stats = stats.rename(columns={value_col: 'value'})
            member_stats.append(stats)
        all_members = pd.concat(member_stats, ignore_index=True)
        summary = (all_members.groupby(['region_abbrev', 'group'])
                              .agg(mean=('value', 'mean'),
                                   lower=('value', 'min'),
                                   upper=('value', 'max'))
                              .reset_index()
                              .rename(columns={'group': 'scenario'}))

        full_grid = pd.DataFrame([(r, s) for r in region_order for s in scenario_groups],
                                 columns=['region_abbrev', 'scenario'])
        summary = pd.merge(full_grid, summary, on=['region_abbrev', 'scenario'], how='left')
        summary['region_abbrev'] = pd.Categorical(summary['region_abbrev'], categories=region_order, ordered=True)
        summary = summary.sort_values(['region_abbrev', 'scenario']).reset_index(drop=True)

        # Plotting
        bar_width = 0.25
        for i, region in enumerate(region_order):
            region_data = summary[summary['region_abbrev'] == region]
            for j, scenario in enumerate(scenario_groups):
                row = region_data[region_data['scenario'] == scenario]
                mean_val = row['mean'].iloc[0] if not row.empty and pd.notna(row['mean'].iloc[0]) else 0.0
                lower = row['lower'].iloc[0] if not row.empty and pd.notna(row['lower'].iloc[0]) else mean_val
                upper = row['upper'].iloc[0] if not row.empty and pd.notna(row['upper'].iloc[0]) else mean_val
                x_pos = i + (j - 1) * bar_width
                ax.bar(x_pos, mean_val, bar_width,
                       color=colors[scenario], edgecolor='black', linewidth=1.0,
                       alpha=0.85 if mean_val > 0 else 0.0)
                if scenario != 'hist' and mean_val > 0:
                    ax.errorbar(x_pos, mean_val,
                                yerr=[[mean_val - lower], [upper - mean_val]],
                                color='black', capsize=4, capthick=1.5, linewidth=1.5)

        ax.set_xticks(range(len(region_order)))
        ax.set_xticklabels(region_order)
        ax.tick_params(axis='x', rotation=0, labelsize=14)
        ax.tick_params(axis='y', labelsize=16)
        ax.text(0.05, 0.95, label, transform=ax.transAxes, fontsize=20, va='top', ha='left')
        ax.set_ylim(30, 80)  

    fig.text(0.08, 0.5, 'Drought Duration\n(% of Growing Season)', fontsize=18, va='center', ha='center', rotation='vertical')

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
                   loc='lower center', bbox_to_anchor=(0.5, -0.02),
                   ncol=4, fontsize=15, frameon=False,
                   handlelength=2.2, handletextpad=0.4, columnspacing=1.6)
        legend_ax.remove()

    plt.tight_layout(rect=[0.1, 0.1, 1, 1])  
    plt.savefig(output_file, bbox_inches='tight', dpi=300)
    plt.show()
    

plot_drought_duration_only(duration_dfs, region_abbrev, region_order,
                           output_file='duration.png',
                           add_legend=True)