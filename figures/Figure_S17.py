################################################# plot (a)
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import matplotlib.ticker as ticker
import pandas as pd

path = 'filepath/'
df_usda = pd.read_csv(f'{path}state_wheat_usda_1981-2015.csv')
df_usda['Value'] = pd.to_numeric(df_usda['Value'].str.replace(',', ''), errors='coerce')


area_target_items = [
'WHEAT - ACRES HARVESTED'
]
df_usda_area = df_usda[df_usda['Data Item'].isin(area_target_items)]
usda_harvested_area = df_usda_area[['State', 'Year', 'Value']].rename(columns={'Value': 'Harvest_Area(acre)'})

production_target_items = [
'WHEAT - PRODUCTION, MEASURED IN BU'
]


df_usda_production = df_usda[df_usda['Data Item'].isin(production_target_items)]
usda_production = df_usda_production[['State', 'Year', 'Value']].rename(columns={'Value': 'Production(BU)'})
usda_merged = pd.merge(usda_harvested_area ,usda_production , on = ['State','Year'])

usda_merged['Yield_bu_per_acre'] = usda_merged['Production(BU)'] / usda_merged['Harvest_Area(acre)']



df_clm = pd.read_csv('/filepath/wheat_1981-2015.csv')
state_list = list(np.unique(df_usda['State']))


df_clm_filtered = df_clm[df_clm['State_Name'].isin(state_list)]


df_clm_filtered['Yield_bu_per_acre'] = df_clm_filtered['Production(BU)'] / (df_clm_filtered['Harvest_Area(km^2)']*247.105)

df_clm_clear = df_clm_filtered[['State_Name', 'Year', 'Yield_bu_per_acre','Production(BU)','Harvest_Area(km^2)']]

comparison = pd.merge(
    usda_merged,
    df_clm_clear,
    left_on=['State', 'Year'],
    right_on=['State_Name', 'Year'],
    suffixes=('_usda', '_clm')
)

states = ["NORTH DAKOTA", "MONTANA",  "SOUTH DAKOTA", "WYOMING", "NEBRASKA"]
comparison = comparison[comparison['State_Name'].isin(states)]

fig, ax = plt.subplots(1, 1, figsize=(4, 4))
plt.scatter(comparison['Production(BU)_usda']/36.7437,comparison['Production(BU)_clm']/36.7437,color='green',s=15, alpha=0.8)
correlation_coefficient, p_value = pearsonr(comparison['Production(BU)_usda'],comparison['Production(BU)_clm'])
print ('correlation_coefficient, p_value',correlation_coefficient, p_value)


comparison_selected = comparison[comparison['State_Name'].isin(states)]

correlation_coefficient_selected, p_value_selected = pearsonr(comparison_selected['Production(BU)_usda'],comparison_selected['Production(BU)_clm'])
print ('correlation_coefficient_selected, p_value_selected',correlation_coefficient_selected, p_value_selected)

# Format the annotation text
corr_text = f"Pearson r = {correlation_coefficient:.3f}\np-value = {p_value:.3f}"
plt.text(
    0.05, 0.95, corr_text,
    transform=plt.gca().transAxes,
    verticalalignment='top',
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.6)
)

plt.text(
    0.8, 0.1, '(a)',
    transform=plt.gca().transAxes,
    verticalalignment='top',
    fontsize=13,
    # bbox=dict(boxstyle="round", facecolor="white", alpha=0.6)
)

plt.ylim(200,1e8)
plt.xlim(200,1e8)
plt.xscale('log')
plt.yscale('log')

# Set same major and minor tick locators
ax = plt.gca()
ax.xaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs='auto', numticks=10))
ax.yaxis.set_minor_locator(ticker.LogLocator(base=10.0, subs='auto', numticks=10))

ax.xaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=10))
ax.yaxis.set_major_locator(ticker.LogLocator(base=10.0, numticks=10))

ax.xaxis.set_minor_formatter(ticker.NullFormatter())
ax.yaxis.set_minor_formatter(ticker.NullFormatter())


plt.xlabel('USDA-NASS Annual production (ton)',fontsize=12)
plt.ylabel('CLM5 Annual production (ton)',fontsize=12)
plt.tick_params(axis='both', labelsize=12) 
plt.tight_layout()
plt.savefig('/filepath/USDA_vs_CLM_wheat_state-year_NGP.png', dpi=500, bbox_inches='tight')

################################################# plot (b)

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress, pearsonr
import pandas as pd

path = 'filepath/'
df_usda = pd.read_csv(f'{path}state_wheat_usda_1981-2015.csv')
df_usda['Value'] = pd.to_numeric(df_usda['Value'].str.replace(',', ''), errors='coerce')

# Harvested Area
area_target_items = ['WHEAT - ACRES HARVESTED']
df_usda_area = df_usda[df_usda['Data Item'].isin(area_target_items)]
usda_harvested_area = df_usda_area[['State', 'Year', 'Value']].rename(columns={'Value': 'Harvest_Area(acre)'})

# Production
production_target_items = ['WHEAT - PRODUCTION, MEASURED IN BU']
df_usda_production = df_usda[df_usda['Data Item'].isin(production_target_items)]
usda_production = df_usda_production[['State', 'Year', 'Value']].rename(columns={'Value': 'Production(BU)'})

usda_merged = pd.merge(usda_harvested_area ,usda_production , on = ['State','Year'])
usda_merged['Yield_bu_per_acre'] = usda_merged['Production(BU)'] / usda_merged['Harvest_Area(acre)']


df_clm = pd.read_csv('/filepath/wheat_1981-2015.csv')
state_list = list(np.unique(usda_merged['State']))

df_clm_filtered = df_clm[df_clm['State_Name'].isin(state_list)].copy()
df_clm_filtered['Yield_bu_per_acre'] = df_clm_filtered['Production(BU)'] / (df_clm_filtered['Harvest_Area(km^2)']*247.105)
df_clm_clear = df_clm_filtered[['State_Name', 'Year', 'Yield_bu_per_acre','Production(BU)','Harvest_Area(km^2)']]


comparison = pd.merge(
    usda_merged,
    df_clm_clear,
    left_on=['State', 'Year'],
    right_on=['State_Name', 'Year'],
    suffixes=('_usda', '_clm')
)

def calculate_anomalies(group):
    # Skip if not enough data points to calculate a trend
    if len(group) > 2:
        # 1. Detrend USDA Yield using linear regression
        base_year = group['Year'].min()
        slope_usda, _, _, _, _ = linregress(group['Year'], group['Yield_bu_per_acre_usda'])
        group['USDA_Detrended_Yield'] = group['Yield_bu_per_acre_usda'] - (slope_usda * (group['Year'] - base_year))
        mean_detrended_usda = group['USDA_Detrended_Yield'].mean()
        group['USDA_Yield_Anomaly'] = group['USDA_Detrended_Yield'] - mean_detrended_usda
                
        # 2. Detrend CLM5 Yield using linear regression
        slope_clm, _, _, _, _ = linregress(group['Year'], group['Yield_bu_per_acre_clm'])
        group['CLM5_Detrended_Yield'] = group['Yield_bu_per_acre_clm'] - (slope_clm * (group['Year'] - base_year))
        mean_detrended_clm = group['CLM5_Detrended_Yield'].mean()
        group['CLM5_Yield_Anomaly'] = group['CLM5_Detrended_Yield'] - mean_detrended_clm
    else:
        group['USDA_Detrended_Yield'] = np.nan
        group['USDA_Yield_Anomaly'] = np.nan
        group['CLM5_Detrended_Yield'] = np.nan
        group['CLM5_Yield_Anomaly'] = np.nan
    return group

# Apply the anomaly calculation state by state
comparison = comparison.groupby('State_Name').apply(calculate_anomalies).reset_index(drop=True)
comparison = comparison.dropna(subset=['USDA_Yield_Anomaly', 'CLM5_Yield_Anomaly'])


# =====================================================================
def state_correlation(group):
    if len(group) > 2:
        r, p = pearsonr(group['USDA_Yield_Anomaly'], group['CLM5_Yield_Anomaly'])
        return pd.Series({'Pearson_r': r, 'p_value': p, 'Years_of_Data': len(group)})
    else:
        return pd.Series({'Pearson_r': np.nan, 'p_value': np.nan, 'Years_of_Data': len(group)})

state_corr_df = comparison.groupby('State_Name').apply(state_correlation).reset_index()
state_corr_df = state_corr_df.sort_values(by='Pearson_r', ascending=False)

print("\n--- Pearson Correlation by State for Wheat (Detrended) ---")
print(state_corr_df.to_string(index=False))
print("----------------------------------------------------------\n")
# =====================================================================


fig, ax = plt.subplots(1, 1, figsize=(4, 4))

states = ["NORTH DAKOTA", "MONTANA",  "SOUTH DAKOTA", "WYOMING", "NEBRASKA"]

comparison_major = comparison[comparison['State_Name'].isin(states)]
comparison_other = comparison[~comparison['State_Name'].isin(states)]

# Calculate Correlations
corr_major, p_major = pearsonr(comparison_major['USDA_Yield_Anomaly'], comparison_major['CLM5_Yield_Anomaly'])


plt.scatter(comparison_major['USDA_Yield_Anomaly'], comparison_major['CLM5_Yield_Anomaly'], 
            color='green', s=15, alpha=0.8, label='Major Wheat States')

plt.axhline(0, color='black', linestyle='--', linewidth=0.8)
plt.axvline(0, color='black', linestyle='--', linewidth=0.8)

corr_text = f"Pearson r = {corr_major:.3f}\np-value = {p_major:.3f}"
plt.text(
    0.55, 0.95, corr_text,
    transform=plt.gca().transAxes,
    verticalalignment='top',
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.8)
)

plt.text(
    0.8, 0.1, '(b)',
    transform=plt.gca().transAxes,
    verticalalignment='top',
    fontsize=13,
)

ticks = np.arange(-40, 60, 20)

ax.set_xticks(ticks)
ax.set_yticks(ticks)

plt.xlabel('USDA-NASS Yield Anomalies (bu/acre)', fontsize=12)
plt.ylabel('CLM5 Yield Anomalies (bu/acre)', fontsize=12)
plt.tick_params(axis='both', labelsize=12) 
plt.tight_layout()
plt.savefig('/filepath/USDA_vs_CLM_wheat_yield_anomaly_both_detrended_NGP.png', dpi=500, bbox_inches='tight')
plt.show()

################################################# plot (c)

import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy.stats import spearmanr
from scipy.stats import pearsonr
from scipy.stats import pearsonr

# Calculate ubRMSE (Unbiased RMSE) for each crop
def calculate_ubrmse(predictions, observations):
    x_mean = np.mean(predictions)
    y_mean = np.mean(observations)
    ub_rmse = np.sqrt(np.mean((predictions - x_mean - (observations - y_mean))**2))
    return ub_rmse

price = 'projected_price'
path = '/filepath/'

df1_wheat = pd.read_csv(path +'wheat_insurance_drought.csv')
df2_wheat = pd.read_csv(path + 'wheat_production_loss_hist_cl100.csv')
df3_wheat = pd.read_csv(path +'wheat_price.csv')

df1_wheat['State'] = df1_wheat['State'].str.upper()  # Convert to uppercase to match df2
df1_wheat['payment_per_acreage'] = df1_wheat['Payment Indemnity']/df1_wheat['Payment Acreage']
df2_wheat = df2_wheat.merge(df3_wheat[['Year', price]], on='Year', how='left')
conversion_factor_wheat = 36.743  # wheat 1 ton = 36.743 bushels
df2_wheat['economy_loss'] = df2_wheat['Production_Loss(ton)'] * conversion_factor_wheat * df2_wheat[price]
df2_wheat['loss_per_acreage'] = df2_wheat['economy_loss']/(df2_wheat['Area_Loss(km^2)']*247.105)

df1_wheat = df1_wheat[(df1_wheat['Year'] >= 2001) & (df1_wheat['Year'] <= 2015)]
df2_wheat = df2_wheat[(df2_wheat['Year'] >= 2001) & (df2_wheat['Year'] <= 2015)]
df2_wheat = df2_wheat.rename(columns={'State_Name': 'State'})
df_merged_wheat = pd.merge(df1_wheat[['Year', 'State', 'payment_per_acreage']], df2_wheat[['Year', 'State', 'loss_per_acreage']], on=['Year', 'State'], how='inner')


states = ["NORTH DAKOTA", "MONTANA",  "SOUTH DAKOTA", "WYOMING", "NEBRASKA"]
states_to_keep_wheat = [state.upper() for state in states]
df_merged_filtered_wheat = df_merged_wheat[df_merged_wheat['State'].isin(states_to_keep_wheat)]
df_merged_filtered_wheat = df_merged_filtered_wheat.fillna(0)
df_clean_wheat = df_merged_filtered_wheat.dropna(subset=['loss_per_acreage', 'payment_per_acreage'])
spearman_corr_wheat, p_value_wheat = spearmanr(df_clean_wheat['loss_per_acreage'], df_clean_wheat['payment_per_acreage'])
print(f"Spearman Correlation_wheat: {spearman_corr_wheat:.4f}")
print(f"P-value_wheat: {p_value_wheat:.4f}")

# Plot scatter plot for Wheat
fig, ax = plt.subplots(1, 1, figsize=(4, 4))
plt.scatter(df_merged_filtered_wheat['payment_per_acreage'], df_merged_filtered_wheat['loss_per_acreage'], color='green', label='Wheat',s=15, alpha=0.8)
plt.xlim(0, 250)
plt.ylim(0, 250)
plt.xlabel('Indemnity Payments ($/acre) ',fontsize=12)
plt.ylabel('Estimated Financial Losses ($/acre)',fontsize=12)
plt.tick_params(axis='both', labelsize=12) 

pearson_corr_wheat, p_value_wheat = pearsonr(df_clean_wheat['loss_per_acreage'], df_clean_wheat['payment_per_acreage'])
print(f"Pearson Correlation for Wheat: {pearson_corr_wheat:.4f}")
print(f"P-value for Pearson Correlation: {p_value_wheat:.4f}")

ub_rmse_wheat = calculate_ubrmse(df_clean_wheat['loss_per_acreage'], df_clean_wheat['payment_per_acreage'])
print(f"ubRMSE for Wheat: {ub_rmse_wheat:.4f}")


# Format the annotation text
corr_text = f"Pearson r = {pearson_corr_wheat:.3f}\np-value = {p_value_wheat:.3f}\nub-rmse={ub_rmse_wheat:.1f} $/acre"
plt.text(
    0.45, 0.95, corr_text,
    transform=plt.gca().transAxes,
    verticalalignment='top',
    fontsize=10,
    bbox=dict(boxstyle="round", facecolor="white", alpha=0.6)
)

plt.text(
    0.8, 0.1, '(c)',
    transform=plt.gca().transAxes,
    verticalalignment='top',
    fontsize=13,
)

plt.xticks(np.arange(0, 251, 50))  
plt.yticks(np.arange(0, 251, 50))  
plt.tight_layout()

save_path = '/filepath/CLM_vs_AgRiskViewer_scatter_wheat_NGP.png'  
plt.savefig(save_path, format='png',bbox_inches='tight')