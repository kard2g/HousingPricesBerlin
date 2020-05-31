"""
Created on Mon May 25 19:24:37 2020

@author: kn
"""

import pandas as pd
import numpy as np
from os import listdir
from os.path import isfile, join, isdir
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
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
df_tmp = df_dict[day_tmp]

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

#%%

# TRAIN_COLUMNS = ['purchasePrice', 'livingSpace', 'price_per_m2', 'lift', 'balcony', 'floor', 'yearConstructed', 'lastRefurbish', 'regio3']
TRAIN_COLUMNS = ['purchasePrice', 'livingSpace', 'price_per_m2']
df_model = df_tmp[TRAIN_COLUMNS]


# SCALE_COLUMNS = ['purchasePrice', 'livingSpace']
# scaling_values = [df_model[SCALE_COLUMNS].mean(), df_model[SCALE_COLUMNS].max(), df_model[SCALE_COLUMNS].min()]
# df_model[SCALE_COLUMNS] = (df_model[SCALE_COLUMNS] - df_model[SCALE_COLUMNS].mean())/(df_model[SCALE_COLUMNS].max() - df_model[SCALE_COLUMNS].min())

n_trainingExamples = int(0.7*len(df_model.index))
dftrain = df_model.iloc[:n_trainingExamples]
dfeval = df_model.iloc[n_trainingExamples:]

y_train = dftrain.pop("purchasePrice")
y_eval = dfeval.pop("purchasePrice")

price_model = RandomForestRegressor(random_state=1)
price_model.fit(dftrain, y_train)

# print('Prediction for the following 5 appartments:')
# dftrain.head()
# print('The predictions are:')
# print(price_model.predict(dfeval.head()))
# print('The real prices are:')
# print(y_eval.head())

print('Training MAE:')
print(int(mean_absolute_error(y_train, price_model.predict(dftrain))))

print('Test MAE:')
print(int(mean_absolute_error(y_eval, price_model.predict(dfeval))))
