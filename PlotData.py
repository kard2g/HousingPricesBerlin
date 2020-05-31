
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import statistics
import math

from UsefulFunctions import writeAllDataToDict, quickOpen

#%%

df_dict = writeAllDataToDict('rawData')

days = list(df_dict.keys())

#%%

day_tmp = days[-1]

# filt_space = df_dict[day_tmp].livingSpace>100
filt_space = df_dict[day_tmp].livingSpace>0
# filt_price = df_dict[day_tmp].purchasePrice<1900000
filt_price = df_dict[day_tmp].purchasePrice>0
# filt_zipCode = df_dict[day_tmp].zipCode==10245.0
filt_zipCode = df_dict[day_tmp].zipCode>0

df_tmp = df_dict[day_tmp][filt_space & filt_price & filt_zipCode]

#%% remove difficult segments
# I would not define these as outliers, but as a segment that is difficult to analyze/predict, because there is very sparse data.
# Partially its the high price segment, partially some specific sparse feature ranges
# Its probably best to exclude them
filt_outlier_price = df_tmp['purchasePrice']<2000000 
filt_outlier_space = df_tmp['livingSpace']<250 
filt_outlier_price_M2 = df_tmp['price_per_m2']<12000
filt_outlier_floor1 = df_tmp['floor']<6
filt_outlier_floor2 = df_tmp['floor']>=0
filt_outlier_useless = df_tmp['useless']==False
df_tmp = df_tmp[filt_outlier_price & filt_outlier_space & filt_outlier_price_M2 & filt_outlier_floor1 & filt_outlier_floor2 & filt_outlier_useless]

#%% first plot: price over living space
x = df_tmp['livingSpace'].astype(float)
y = df_tmp['purchasePrice']

plt.scatter(x, y, c = 'blue', marker = 's')
plt.xlabel('living space')
plt.ylabel('purchase price')
plt.title('price over living space')
plt.show()

#%% second plot: price/m2 over living space
y = df_tmp['price_per_m2']
plt.scatter(x, y, c = 'blue', marker = 's')
plt.xlabel('living space')
plt.ylabel('price per m2')
plt.title('price/m2 over living space')
plt.show()

#%% third plot: histogramm floor
y = df_tmp['floor']
plt.hist(y)
plt.xlabel('floor')
plt.ylabel('number of object')
plt.title('floor count histogramm')
plt.show()
