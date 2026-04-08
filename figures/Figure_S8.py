import numpy as np
import pandas as pd 
import matplotlib.pyplot as plt

path = '/data_path/'

df1 = pd.read_csv(f'{path}prices_atm45cooler_ssp3_USA.csv') 
df2 = pd.read_csv(f'{path}prices_atm85cooler_ssp5_USA.csv') 

df3 = pd.read_csv(f'{path}prices_atm45hotter_ssp3_USA.csv') 
df4 = pd.read_csv(f'{path}prices_atm85hotter_ssp5_USA.csv')
crop_labels = {'Corn': 'Corn', 'OilCrop': 'Soybean', 'Wheat': 'Wheat'}
crop_color = {'Corn': 'blue', 'OilCrop': 'orange', 'Wheat': 'green'}
plt.figure(figsize=(6, 5))
for crop in ['Corn', 'OilCrop', 'Wheat']:
    df1_crop = df1[(df1['sector'] == crop) & (df1['Year'] >= 2021) & (df1['Year'] <= 2055)][['Year', 'value']]
    df2_crop = df2[(df2['sector'] == crop) & (df2['Year'] >= 2021) & (df2['Year'] <= 2055)][['Year', 'value']]
    df3_crop = df3[(df3['sector'] == crop) & (df3['Year'] >= 2021) & (df3['Year'] <= 2055)][['Year', 'value']]
    df4_crop = df4[(df4['sector'] == crop) & (df4['Year'] >= 2021) & (df4['Year'] <= 2055)][['Year', 'value']]

    ratio_c = df1_crop['value'] / df2_crop['value']
    ratio_h = df3_crop['value'] / df4_crop['value']

    label = crop_labels[crop] 
    color = crop_color[crop]
    plt.plot(df1_crop['Year'], ratio_c, label = label + ', cooler',linewidth=2,color= color )
    plt.plot(df1_crop['Year'], ratio_h, label = label + ', hotter',linewidth=2,color= color , linestyle='--')
    print ()

    plt.legend(fontsize = 12)

plt.xlim(2020,2056)
plt.xticks(ticks=np.arange(2020, 2060, 5))
plt.ylim(1.0,1.8)
plt.tick_params(axis='both', labelsize=12)

plt.ylabel('Price Ratio (atmp45_ssp3 / atm85_ssp5)', fontsize=14,labelpad=10)

plt.savefig(f'{path}/price_ratio.png', dpi=300, bbox_inches='tight')
plt.show()
