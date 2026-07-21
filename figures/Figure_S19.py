import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.patches import Rectangle
import numpy as np

sns.set_style("ticks")

# ==========================================
# 1. Load CSV
# ==========================================
csv_file = "/filepath/winterwheat_growing_season_drought_characteristics.csv"


df = pd.read_csv(csv_file)

# Clean strings
df["Region_Name"] = df["Region_Name"].astype(str).str.strip()
df["Season"] = df["Season"].astype(str).str.strip()
df["Scenario"] = df["Scenario"].astype(str).str.strip()

# ==========================================
# 2. Configuration
# ==========================================
target_season = "Winter Wheat Season (Sep-Jun)"

region_abbrev = {
    "CONUS": "CONUS",
    "Northeast": "NE",
    "Southeast": "SE",
    "Midwest": "MW",
    "N. Great Plains": "NGP",
    "S. Great Plains": "SGP",
    "Northwest": "NW",
    "Southwest": "SW"
}

region_order = ["CONUS", "MW", "NGP", "SGP", "NW", "SW", "SE", "NE"]

# Keep NE label on x axis, but hide its bars
exclude_regions = ["NE"]

metric_info = {
    "Exposed_Area": "Drought-Exposed Area (% of CONUS planted)",
    "Intensity_Ratio": "Drought Intensity (/month)",
    "Duration": "Drought Duration (% of Growing Season)"

}

colors = {
    "Historical": "darkgrey",
    "Future": "orange"
}

output_file = "/filepath/winterwheat_drought_characteristics_3panel.png"

# ==========================================
# 3. Prepare winter wheat data
# ==========================================
df_winter = df[df["Season"] == target_season].copy()

df_winter["region_abbrev"] = df_winter["Region_Name"].map(region_abbrev)

# Keep only regions in desired plotting list
df_winter = df_winter[df_winter["region_abbrev"].isin(region_order)].copy()

# Historical vs future grouping
df_winter["period_group"] = np.where(
    df_winter["Scenario"].str.lower() == "historical",
    "Historical",
    "Future"
)

# ==========================================
# 4. Plot function
# ==========================================
def plot_winter_wheat_compact(
    df_winter,
    metric_info,
    region_order,
    colors,
    output_file,
    exclude_regions=None
):
    fig, axes = plt.subplots(1, 3, figsize=(16, 3.8), sharex=True)

    fig.text(
        0.005, 0.5, "Winter wheat",
        fontsize=18,
        va="center",
        ha="center",
        rotation="vertical"
    )

    panel_labels = ["(a)", "(b)", "(c)"]
    bar_width = 0.25

    for ax, (metric_col, title), panel_label in zip(axes, metric_info.items(), panel_labels):

        # Historical mean
        hist = (
            df_winter[df_winter["period_group"] == "Historical"]
            .groupby("region_abbrev")[metric_col]
            .mean()
            .reset_index()
            .rename(columns={metric_col: "hist_mean"})
        )

        # Future mean and range across scenarios
        fut = (
            df_winter[df_winter["period_group"] == "Future"]
            .groupby("region_abbrev")[metric_col]
            .agg(fut_mean="mean", fut_lower="min", fut_upper="max")
            .reset_index()
        )

        # Full grid preserves order and keeps empty regions
        full_grid = pd.DataFrame({"region_abbrev": region_order})
        summary = full_grid.merge(hist, on="region_abbrev", how="left")
        summary = summary.merge(fut, on="region_abbrev", how="left")

        # Exclude certain regions by masking values, but keep x-axis labels
        if exclude_regions is not None:
            mask = summary["region_abbrev"].isin(exclude_regions)
            summary.loc[mask, ["hist_mean", "fut_mean", "fut_lower", "fut_upper"]] = np.nan

        x = np.arange(len(region_order))

        hist_values = summary["hist_mean"].values
        fut_values = summary["fut_mean"].values
        fut_lower = summary["fut_lower"].values
        fut_upper = summary["fut_upper"].values

        # Plot bars region by region
        for i in range(len(region_order)):
            # Historical bar
            hist_val = hist_values[i]
            hist_plot_val = 0 if np.isnan(hist_val) else hist_val
            hist_alpha = 0.0 if np.isnan(hist_val) else 0.9

            ax.bar(
                x[i] - bar_width / 2,
                hist_plot_val,
                bar_width,
                color=colors["Historical"],
                edgecolor="black",
                linewidth=0.8,
                alpha=hist_alpha,
                label="Historical" if i == 0 else None
            )

            # Future bar
            fut_val = fut_values[i]
            fut_plot_val = 0 if np.isnan(fut_val) else fut_val
            fut_alpha = 0.0 if np.isnan(fut_val) else 0.9

            ax.bar(
                x[i] + bar_width / 2,
                fut_plot_val,
                bar_width,
                color=colors["Future"],
                edgecolor="black",
                linewidth=0.8,
                alpha=fut_alpha,
                label="Future mean" if i == 0 else None
            )

            # Future error bar
            if not np.isnan(fut_val):
                lower_err = fut_val - fut_lower[i]
                upper_err = fut_upper[i] - fut_val

                ax.errorbar(
                    x[i] + bar_width / 2,
                    fut_val,
                    yerr=[[lower_err], [upper_err]],
                    color="black",
                    capsize=3,
                    capthick=1,
                    linewidth=1.2,
                    fmt="none"
                )

        # Styling
        ax.set_title(title, fontsize=14, pad=10)
        ax.set_xlabel("")
        ax.set_ylabel("")
        ax.set_xticks(x)
        ax.set_xticklabels(region_order)
        ax.tick_params(axis="x", rotation=0, labelsize=13)
        ax.tick_params(axis="y", labelsize=13)
        ax.text(
            0.88, 0.92, panel_label,
            transform=ax.transAxes,
            fontsize=16,
            va="top",
            ha="left"
        )

        sns.despine(ax=ax)

        # Optional y-axis ranges
        if metric_col == "Exposed_Area":
            ax.set_ylim(0, 85)
        elif metric_col == "Duration":
            ax.set_ylim(0, 50)
        elif metric_col == "Intensity_Ratio":
            ax.set_ylim(0.5, 2.5)
            ax.yaxis.set_major_locator(
                plt.FixedLocator([0.5, 1.0, 1.5, 2.0, 2.5])
            )
            ax.yaxis.set_major_formatter(
                plt.FixedFormatter(["0.5", "1.0", "1.5", "2.0", "2.5"])
            )

    # Legend
    color_elements = [
        Rectangle((0, 0), 1, 1, fc=colors["Historical"], ec="black", lw=0.8, alpha=0.9),
        Rectangle((0, 0), 1, 1, fc=colors["Future"], ec="black", lw=0.8, alpha=0.9)
    ]

    # Create real errorbar handle for legend
    legend_ax = fig.add_axes([0, 0, 0.01, 0.01])
    legend_ax.set_xlim(0, 1)
    legend_ax.set_ylim(0, 1)
    legend_ax.axis("off")

    eb_handle = legend_ax.errorbar(
        0.5, 0.5,
        yerr=0.25,
        color="black",
        capsize=3,
        capthick=1.2,
        lw=1.2,
        fmt="none"
    )

    fig.legend(
        handles=color_elements + [eb_handle],
        labels=["Historical", "ATM+LAND", "Range across 4 scenarios"],
        loc="lower center",
        bbox_to_anchor=(0.5, -0.01),
        ncol=3,
        fontsize=14,
        frameon=False,
        handlelength=2.2,
        handletextpad=0.4,
        columnspacing=1.6
    )

    legend_ax.remove()

    plt.subplots_adjust(
        left=0.055,
        right=0.98,
        top=0.86,
        bottom=0.22,
        wspace=0.18
    )

    plt.savefig(output_file, bbox_inches="tight", dpi=400)
    plt.show()

    print(f"Saved figure to: {output_file}")

# ==========================================
# 5. Generate figure
# ==========================================
plot_winter_wheat_compact(
    df_winter=df_winter,
    metric_info=metric_info,
    region_order=region_order,
    colors=colors,
    output_file=output_file,
    exclude_regions=exclude_regions
)
