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

rawDataPath = 'rawData/'
rawDataDays = [f for f in listdir(rawDataPath) if isdir(join(rawDataPath, f))]
rawDataDays.remove('personal')
rawDataDay = max(rawDataDays)

df_raw = pd.read_csv(rawDataPath + rawDataDay + '/ScrapedDataClean.csv', error_bad_lines=False, warn_bad_lines=False, sep=";", index_col=0, decimal=",")

df_raw = df_raw[df_raw['purchasePrice']<600000]
# df_raw = df_raw[df_raw['purchasePrice']>150000]
df_raw = df_raw[df_raw['useless']!=True]

y = df_raw['purchasePrice']
fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(FormatStrFormatter('%1.0f'))
plt.hist(y)
plt.show()

#%%

# TRAIN_COLUMNS = ['purchasePrice', 'livingSpace', 'zipCode', 'useless', 'lift', 'rented', 'newlyConst', 'noRooms', 'balcony', 'floor']
TRAIN_COLUMNS = ['purchasePrice', 'livingSpace', 'zipCode', 'useless', 'lift', 'rented', 'balcony']
df_model = df_raw[TRAIN_COLUMNS]
df_model = df_model.dropna(axis=0)

# SCALE_COLUMNS = ['purchasePrice', 'livingSpace', 'zipCode']
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
