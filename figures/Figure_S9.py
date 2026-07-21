import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. Paths and settings
# ============================================================

nca_mapping_path = '/filepath/state_nca_mapping.csv'

price_path = (
    '/filepath//'
    'ssmi-1_based/StateBase_GridYield/future/GCAM_crop_price/'
)

proloss_path = (
    '/filepath//'
    'ssmi-1_based/StateBase_GridYield/revision_npj/'
)

outdir = f'{proloss_path}/SI_financial_loss_components/'
os.makedirs(outdir, exist_ok=True)

nca_mapping = pd.read_csv(nca_mapping_path)

# Crop name used in production-loss files -> GCAM commodity sector name
crop_map = {
    'corn': 'Corn',
    'wheat': 'Wheat',
    'soybean': 'OilCrop'
}

region_names = {
    'CONUS': 'CONUS',
    1: 'NE',
    2: 'SE',
    4: 'MW',
    5: 'NGP',
    6: 'SGP',
    8: 'NW',
    7: 'SW'
}

# Major regions to show in the SI figure.
# Modify if needed.
crop_regions = {
    'corn': ['CONUS', 4, 5, 6],
    'soybean': ['CONUS', 4, 5, 6, 2],
    'wheat': ['CONUS', 5, 6, 8]
}

scenario_info = {
    'atm45_ssp3': {'ssp': '3', 'rcp': '45'},
    'atm85_ssp5': {'ssp': '5', 'rcp': '85'}
}

model_info = {
    'c': 'cooler',
    'h': 'hotter'
}

scenario_colors = {
    'atm45_ssp3': '#d55e00',
    'atm85_ssp5': '#0072b2'
}

# Choose crops to plot/save
crops_to_plot = ['corn', 'soybean']  # add 'wheat' if needed

# Small value used to match CDF logic when denominator financial loss is zero
EPS = 1e-10


# ============================================================
# 2. Helper functions
# ============================================================

def load_production_loss(crop, period, ssp, rcp, model):
    """
    Load production-loss file and merge with NCA mapping.
    """
    f = f'{proloss_path}{crop}_production_loss_{period}_{ssp}_{rcp}_{model}_2021-2055.csv'
    df = pd.read_csv(f)

    # Avoid duplicate nca_id if the file already contains it
    df = df.drop(columns=[c for c in ['nca_id'] if c in df.columns], errors='ignore')
    df = df.merge(nca_mapping, on='state_id', how='left')

    return df


def load_price(crop_price, ssp, rcp, model):
    """
    Load GCAM crop price for one commodity sector and scenario.
    """
    model_full = model_info[model]
    f = f'{price_path}prices_rcp{rcp}{model_full}_ssp{ssp}_USA.csv'

    df_price_raw = pd.read_csv(f)
    df_price = (
        df_price_raw[
            (df_price_raw['sector'] == crop_price) & 
            (df_price_raw['Year'] >= 2021) & 
            (df_price_raw['Year'] <= 2055)
        ][['Year', 'value']]
        .rename(columns={'value': 'Price'})
        .sort_values('Year')
        .reset_index(drop=True)
    )

    return df_price


def aggregate_production_loss(df, region):
    """
    Aggregate production loss by year for CONUS or one NCA region.
    """
    if region == 'CONUS':
        out = (
            df.groupby('Year')[['Production_Loss(ton)']]
            .sum()
            .sort_index()
        )
    else:
        out = (
            df[df['nca_id'] == region]
            .groupby('Year')[['Production_Loss(ton)']]
            .sum()
            .sort_index()
        )

    return out['Production_Loss(ton)']


def build_variant_data(crop, period='nf'):
    """
    Build production-loss, price, and financial-loss time series
    for atm45_ssp3 and atm85_ssp5, separately for cooler and hotter variants.
    """
    crop_price = crop_map[crop]
    regions = crop_regions[crop]

    data = {}

    for scen_name, scen in scenario_info.items():
        ssp = scen['ssp']
        rcp = scen['rcp']

        data[scen_name] = {}

        for model in ['c', 'h']:
            df_loss = load_production_loss(crop, period, ssp, rcp, model)
            df_price = load_price(crop_price, ssp, rcp, model)

            price_series = df_price.set_index('Year')['Price']

            data[scen_name][model] = {
                'price': price_series,
                'production_loss': {},
                'financial_loss': {}
            }

            for region in regions:
                prod = aggregate_production_loss(df_loss, region)

                # Align years between production loss and price
                common_years = prod.index.intersection(price_series.index)
                prod = prod.loc[common_years]
                price = price_series.loc[common_years]

                fin = prod * 1000.0 * price

                data[scen_name][model]['production_loss'][region] = prod
                data[scen_name][model]['financial_loss'][region] = fin

    return data


def average_cooler_hotter(data, scen_name, variable, region=None):
    """
    Average cooler and hotter variants for plotting absolute values.
    variable can be 'price', 'production_loss', or 'financial_loss'.
    """
    series_list = []

    for model in ['c', 'h']:
        if variable == 'price':
            s = data[scen_name][model]['price']
        else:
            s = data[scen_name][model][variable][region]
        series_list.append(s)

    return pd.concat(series_list, axis=1).mean(axis=1)


def pairwise_relative_difference(data, region, variable):
    """
    Calculate relative difference using the same logic as the CDF:

    1. Calculate relative difference for cooler:
       (atm45_c - atm85_c) / atm85_c * 100

    2. Calculate relative difference for hotter:
       (atm45_h - atm85_h) / atm85_h * 100

    3. Average the two relative differences.

    variable can be:
    - 'production_loss'
    - 'financial_loss'
    - 'price'

    For price, region is ignored because price is crop/scenario-specific.
    """
    diffs = []

    for model in ['c', 'h']:
        if variable == 'price':
            v45 = data['atm45_ssp3'][model]['price']
            v85 = data['atm85_ssp5'][model]['price']
        else:
            v45 = data['atm45_ssp3'][model][variable][region]
            v85 = data['atm85_ssp5'][model][variable][region]

        common_years = v45.index.intersection(v85.index)
        v45 = v45.loc[common_years]
        v85 = v85.loc[common_years]

        if variable == 'financial_loss':
            denom = v85.replace(0, EPS)
        else:
            denom = v85.replace(0, np.nan)

        diff = (v45 - v85) / denom * 100.0
        diffs.append(diff)

    diff_mean = pd.concat(diffs, axis=1).mean(axis=1)
    diff_mean = diff_mean.replace([np.inf, -np.inf], np.nan)

    return diff_mean


def variant_relative_difference(data, region, variable, model):
    """
    Calculate relative difference for one specific variant.
    Useful for annual output reference.
    """
    if variable == 'price':
        v45 = data['atm45_ssp3'][model]['price']
        v85 = data['atm85_ssp5'][model]['price']
    else:
        v45 = data['atm45_ssp3'][model][variable][region]
        v85 = data['atm85_ssp5'][model][variable][region]

    common_years = v45.index.intersection(v85.index)
    v45 = v45.loc[common_years]
    v85 = v85.loc[common_years]

    if variable == 'financial_loss':
        denom = v85.replace(0, EPS)
    else:
        denom = v85.replace(0, np.nan)

    diff = (v45 - v85) / denom * 100.0
    return diff.replace([np.inf, -np.inf], np.nan)


# ============================================================
# 3. Plot GCAM commodity price first, followed by annual physical production loss
#    No variant mean: show cooler and hotter variants directly using solid colors
# ============================================================

from matplotlib.lines import Line2D

# 1. Isolate the custom price panel y-limits
crop_price_limits = {
    'corn': (0.05, 0.10),
    'soybean': (0.05, 0.25),
    'wheat': (0.0, 0.30)
}

# 2. Map explicit hex codes to establish the blue-vs-red color palette 
variant_colors = {
    'atm45_ssp3': {
        'c': 'lightskyblue',  
        'h': 'blue'   
    },
    'atm85_ssp5': {
        'c': '#fdbf6f',  
        'h': 'red'   
    }
}


def plot_variants_only(ax, data, scen_name, variable, region=None, scale=1.0):
    """
    Plot cooler and hotter variants as distinct solid lines using the color palette.
    """
    for model in ['c', 'h']:
        if variable == 'price':
            series = data[scen_name][model]['price']
        elif variable == 'production_loss':
            series = data[scen_name][model]['production_loss'][region]
        else:
            raise ValueError("variable must be 'price' or 'production_loss'")

        # Fetch the dedicated hex color for this specific scenario-variant pair
        line_color = variant_colors[scen_name][model]

        ax.plot(
            series.index,
            series.values / scale,
            color=line_color,
            linestyle='-',       # Uniform solid lines
            linewidth=1.2,
            alpha=0.7
        )


for crop in crops_to_plot:
    regions = crop_regions[crop]
    data = build_variant_data(crop, period='nf')

    nrows = len(regions) + 1

    fig, axes = plt.subplots(
        nrows=nrows,
        ncols=1,
        figsize=(7.2, 9),
        sharex=True
    )

    if nrows == 1:
        axes = [axes]

    # ----------------------------
    # 1. Commodity price panel (TOP PANEL)
    # ----------------------------
    ax_price = axes[0]

    for scen_name in ['atm85_ssp5', 'atm45_ssp3']:
        plot_variants_only(
            ax=ax_price,
            data=data,
            scen_name=scen_name,
            variable='price',
            region=None,
            scale=1.0
        )

    ax_price.set_ylabel("Price\n(1975 $/kg)", fontsize=12)
    # ax_price.grid(True, linestyle='--', alpha=0.4, axis='y')
    ax_price.tick_params(axis='both', labelsize=12)

    if crop in crop_price_limits:
        ax_price.set_ylim(crop_price_limits[crop])

    ax_price.set_title(
        f"{crop.capitalize()}",
        fontsize=14,
        pad=8
    )

    # Re-mapped Custom Legend using the new hex codes
    legend_handles = [
        Line2D([0], [0], color=variant_colors['atm45_ssp3']['c'], lw=1.2, linestyle='-', label='atm45cooler_ssp3'),
        Line2D([0], [0], color=variant_colors['atm45_ssp3']['h'], lw=1.2, linestyle='-', label='atm45hotter_ssp3'),
        Line2D([0], [0], color=variant_colors['atm85_ssp5']['c'], lw=1.2, linestyle='-', label='atm85cooler_ssp5'),
        Line2D([0], [0], color=variant_colors['atm85_ssp5']['h'], lw=1.2, linestyle='-', label='atm85hotter_ssp5')
    ]

    # ----------------------------
    # 2. Physical production-loss panels (LOWER PANELS)
    # ----------------------------
    for i, region in enumerate(regions):
        ax = axes[i + 1]

        for scen_name in ['atm45_ssp3', 'atm85_ssp5']:
            plot_variants_only(
                ax=ax,
                data=data,
                scen_name=scen_name,
                variable='production_loss',
                region=region,
                scale=1e6  # Convert ton to million tons (Mt)
            )

        ax.set_ylabel(f"{region_names[region]}\nLoss (Mt)", fontsize=12)
        # ax.grid(True, linestyle='--', alpha=0.4, axis='y')
        ax.tick_params(axis='both', labelsize=12)

    # ----------------------------
    # 3. Common x-axis formatting
    # ----------------------------
    for ax in axes:
        ax.set_xlim(2021, 2055)
        ax.set_xticks([2021, 2025, 2030, 2035, 2040, 2045, 2050, 2055])

    fig.tight_layout()

    out_png = f'{outdir}/SI_annual_production_loss_and_price_{crop}_variants_only.png'
    out_pdf = f'{outdir}/SI_annual_production_loss_and_price_{crop}_variants_only.pdf'

    plt.savefig(out_png, dpi=300, bbox_inches='tight')
