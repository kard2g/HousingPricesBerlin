"""
Created on Mon May 25 19:24:37 2020

@author: kn
"""

import pandas as pd
import numpy as np
import statistics
import math
from os import listdir
from os.path import isfile, join, isdir
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
import datetime
import matplotlib.dates as mdates
from UsefulFunctions import quickOpen

#%%

rawDataPath = 'rawData'
rawDataDays = [f for f in listdir(rawDataPath) if isdir(join(rawDataPath, f))]
rawDataDays = sorted(rawDataDays)
try: 
    rawDataDays.remove('personal')
except ValueError: 
    pass
try: 
    rawDataDays.remove('summarizedData')
except ValueError: 
    pass

#%%

try:
    df_dict = np.load(rawDataPath + "/summarizedData/summarizedDataTill_" + rawDataDays[-1] + ".npy",allow_pickle='TRUE').item()
    df_meta = np.load(rawDataPath + "/summarizedData/summarizedMetaDataTill_" + rawDataDays[-1] + ".npy",allow_pickle='TRUE').item()
    print('Data from ' + str(rawDataDays[-1]) + ' loaded (newest possible).')
except:
    print('Newest data not available. Please run CleanData.py first.')


#%%

day_tmp = rawDataDays[-1]
df_tmp = df_dict[day_tmp]

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
