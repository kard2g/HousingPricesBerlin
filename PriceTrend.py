import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import FormatStrFormatter
from os.path import isfile, join, isdir
from os import listdir
import statistics
import math
import datetime
import matplotlib.dates as mdates
from UsefulFunctions import quickOpen

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
    df_dict= np.load(rawDataPath + "/summarizedData/summarizedDataTill_" + rawDataDays[-1] + ".npy",allow_pickle='TRUE').item()
    df_meta= np.load(rawDataPath + "/summarizedData/summarizedMetaDataTill_" + rawDataDays[-1] + ".npy",allow_pickle='TRUE').item()
    print('Data from ' + str(rawDataDays[-1]) + ' loaded (newest possible).')
except:
    print('Newest data not available. Please run CleanData.py first.')

#%% find new objects in the dataset

if False:
    df_newDay = df_dict[rawDataDays[-1]]
    df_lastDay = df_dict[rawDataDays[-2]]
    
    soldObjects = pd.DataFrame()
    for el in df_lastDay.URL:
        if df_newDay.URL.str.contains(el).sum()==0:
            soldObjects = soldObjects.append(df_lastDay[df_lastDay.URL==el])
    print('There are ' + str(soldObjects.shape[0]) + ' objects sold since the last day')
    # print('Since the last day (' + str(rawDataDays[-2]) + '), these objects have been removed from the dataset:')
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'expand_frame_repr', False):  
    #     print(soldObjects)
    
    newObjects = pd.DataFrame()
    for el in df_newDay.URL:
        if df_lastDay.URL.str.contains(el).sum()==0:
            newObjects = newObjects.append(df_newDay[df_newDay.URL==el])
    print('There are ' + str(newObjects.shape[0]) + ' NEW objects in the dataset')
    # print('\nThese objects are NEW in the dataset:')
    # with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'expand_frame_repr', False):  
    #     print(newObjects)
    # for el in newObjects.URL: # NEVER do this on a big dataset!!!
    #     quickOpen(el)

#%%
lightgrey = (0.6, 0.6, 0.6)
darkgrey = (0.2, 0.2, 0.2)

x = [datetime.datetime.strptime(d,"%Y-%m-%d").date() for d in rawDataDays]

y = df_meta[rawDataDays[-1]].objectsInDataset
fig, ax = plt.subplots()
plt.plot(x,y, '--o', color = lightgrey, markersize=8, markerfacecolor = darkgrey, markeredgecolor = darkgrey)
plt.ylabel('Objects')
ax.yaxis.set_major_formatter(FormatStrFormatter('%1.0f'))
plt.ylim((int(math.floor(min(y) / 10.0))*10-1, int(math.ceil(max(y) / 10.0))*10+1 ))
plt.xlabel('date')
plt.xticks(rotation=50)
formatter = mdates.DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)
plt.title('objects in the dataset')
plt.show()


y = df_meta[rawDataDays[-1]].medianPricePerM2
fig, ax = plt.subplots()
plt.plot(x,y, '--o', color = lightgrey, markersize=8, markerfacecolor = darkgrey, markeredgecolor = darkgrey)
plt.ylabel('Euros/m2')
ax.yaxis.set_major_formatter(FormatStrFormatter('%1.0f'))
plt.ylim((int(math.floor(min(y) / 10.0))*10-1, int(math.ceil(max(y) / 10.0))*10+1 ))
plt.xlabel('date')
plt.xticks(rotation=50)
formatter = mdates.DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)
plt.title('medianPricePerM2 trend')
plt.show()

y = df_meta[rawDataDays[-1]].meanPricePerM2
fig, ax = plt.subplots()
plt.plot(x,y, '--o', color = lightgrey, markersize=8, markerfacecolor = darkgrey, markeredgecolor = darkgrey)
plt.ylabel('Euros/m2')
plt.ylim((int(math.floor(min(y) / 10.0))*10-1, int(math.ceil(max(y) / 10.0))*10+1 ))
ax.yaxis.set_major_formatter(FormatStrFormatter('%1.0f'))
plt.xlabel('date')
plt.xticks(rotation=50)
formatter = mdates.DateFormatter("%Y-%m-%d")
ax.xaxis.set_major_formatter(formatter)
locator = mdates.DayLocator()
ax.xaxis.set_major_locator(locator)
plt.title('meanPricePerM2 trend')
plt.show()

#%%

df_tmp = df_dict[rawDataDays[-1]]
x = df_tmp['livingSpace'].astype(float)
y = df_tmp['price_per_m2'].astype(float)
plt.scatter(x, y, c = 'blue', marker = 's')
plt.xlabel('space [m2]')
plt.ylabel('prices [Euro/m2]')
plt.show()

#%%

df_tmp = df_dict[rawDataDays[-1]]
x = df_tmp['livingSpace'].astype(float)
y = df_tmp['purchasePrice'].astype(float)
plt.scatter(x, y, c = 'blue', marker = 's')
plt.xlabel('space [m2]')
plt.ylabel('prices [Euro/m2]')
plt.show()