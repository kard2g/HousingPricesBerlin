#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 25 19:24:37 2020

@author: kn
"""

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from os.path import isfile, join, isdir
from os import listdir
import statistics
import math

rawDataPath = 'rawData'
# rawDataPath = 'rawData/personal'
rawDataDays = [f for f in listdir(rawDataPath) if isdir(join(rawDataPath, f))]
rawDataDays = sorted(rawDataDays)
try: 
    rawDataDays.remove('personal')
except ValueError: 
    pass
    
df_dict = {}

objectsInDataset = []
medianPricePerM2 = []
meanPricePerM2 = []
for day in rawDataDays:
    
    df_tmp = pd.read_csv(rawDataPath + "/" + day + "/ScrapedDataClean.csv", error_bad_lines=False, warn_bad_lines=False, sep=";", index_col=0, decimal=",")
    
    df_tmp["purchasePrice"] = df_tmp["purchasePrice"].astype(float)
    df_tmp["price_per_m2"] = df_tmp["price_per_m2"].astype(float)
    df_tmp.sort_values('purchasePrice', inplace=True, ascending=False)
    
    prices = df_tmp["purchasePrice"].astype(float)
    space = df_tmp["livingSpace"].astype(float)
    zipCode = df_tmp["zipCode"].astype(float)
    pricesPerM2 = df_tmp['price_per_m2'].astype(float)
    
    # filtNan = prices.notnull()
    filtNan = ~np.isnan(prices) & ~np.isnan(pricesPerM2)
    filtPrice = prices < 4000000 # ex luxury filter
    # filtPrice = (prices > 500000) & (prices < 1000000) # our range filter
    
    filtUseless = df_tmp["useless"]==False
    
    prices = prices[filtNan & filtPrice & filtUseless]
    space = space[filtNan & filtPrice & filtUseless]
    pricesPerM2 = pricesPerM2[filtNan & filtPrice & filtUseless]
    zipCode = zipCode[filtNan & filtPrice & filtUseless]
    
    totalPrice = prices.sum()
    totalSpace = space.sum()
    
    priceSdev = statistics.stdev(prices)
    spaceSdev = statistics.stdev(space)
    
    medianPricePerM2.append(statistics.median(pricesPerM2))
    meanPricePerM2.append(statistics.mean(pricesPerM2))
    objectsInDataset.append(prices.size)

    priceSdev = statistics.stdev(prices)
    spaceSdev = statistics.stdev(space)
    
    df_save = pd.DataFrame({'prices': prices, 'space': space, 'pricesPerM2': pricesPerM2, 'zipCode': zipCode})
    df_dict[day] = df_save


lightgrey = (0.6, 0.6, 0.6)
darkgrey = (0.2, 0.2, 0.2)

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(FormatStrFormatter('%1.0f'))
plt.plot(rawDataDays,objectsInDataset, '--o', color = lightgrey, markersize=8, markerfacecolor = darkgrey, markeredgecolor = darkgrey)
plt.ylabel('Objects')
plt.xlabel('date')
plt.ylim((int(math.floor(min(objectsInDataset) / 10.0))*10-1, int(math.ceil(max(objectsInDataset) / 10.0))*10+1 ))
plt.title('objects in the dataset')
plt.show()

# fig, ax = plt.subplots()
# # ax.yaxis.set_major_formatter(FormatStrFormatter('%1.0f'))
# data1 = df_dict['2020-05-11']['pricesPerM2']
# data2 = df_dict['2020-05-24']['pricesPerM2']
# ax.boxplot([data1, data2])
# ax.set_xticklabels(rawDataDays)

fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(FormatStrFormatter('%1.0f'))
plt.plot(rawDataDays,medianPricePerM2, '--o', color = lightgrey, markersize=8, markerfacecolor = darkgrey, markeredgecolor = darkgrey)
plt.ylabel('Euros/m2')
plt.xlabel('date')
plt.ylim((int(math.floor(min(medianPricePerM2) / 5.0))*5-1, int(math.ceil(max(medianPricePerM2) / 5.0))*5+1 ))
plt.title('median price/m2 trend')
plt.show()

y = meanPricePerM2
fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(FormatStrFormatter('%1.0f'))
plt.plot(rawDataDays,y, '--o', color = lightgrey, markersize=8, markerfacecolor = darkgrey, markeredgecolor = darkgrey)
plt.ylabel('Euros/m2')
plt.xlabel('date')
plt.ylim((int(math.floor(min(y) / 5.0))*5-1, int(math.ceil(max(y) / 5.0))*5+1 ))
plt.title('mean price/m2 trend')
plt.show()

