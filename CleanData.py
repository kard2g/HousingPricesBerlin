import pandas as pd
import numpy as np
from os.path import isfile, join, isdir
from os import listdir
import statistics

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

# 

try:
    df_dict= np.load(rawDataPath + "/summarizedData/summarizedDataTill_" + rawDataDays[-1] + ".npy",allow_pickle='TRUE').item()
    df_meta= np.load(rawDataPath + "/summarizedData/summarizedMetaDataTill_" + rawDataDays[-1] + ".npy",allow_pickle='TRUE').item()
    print('Latest data already exists in rawData/summarizedData. \nRemove those files if you want to repeat the cleaning process.')
except:

    df_dict = {}
    df_meta = {}
    
    objectsInDataset = []
    medianPricePerM2 = []
    meanPricePerM2 = []
    for day in rawDataDays:
        
        df_tmp = pd.read_csv(rawDataPath + "/" + day + "/ScrapedDataClean.csv", error_bad_lines=False, warn_bad_lines=False, sep=";", index_col=0, decimal=",")
                
        prices = df_tmp["purchasePrice"].astype(float)
        space = df_tmp["livingSpace"].astype(float)
        zipCode = df_tmp["zipCode"].astype(float)
        pricesPerM2 = df_tmp['price_per_m2'].astype(float)
        floor = df_tmp['floor'].astype(float)
        
        filters = {}
        
        filtNan = ~np.isnan(prices) & ~np.isnan(pricesPerM2)
        filtPrice = prices < 2000000 # ex luxury filter
        filtSpace = space<250
        filtUseless = df_tmp["useless"]==False
        filtPricePerM2 = pricesPerM2 < 13000
        filtFloor1 = df_tmp.floor.astype(float) < 6
        filtFloor2 = df_tmp.floor.astype(float) >= 0
       
        filtAll = filtNan & filtPrice & filtSpace & filtPricePerM2 & filtUseless & filtFloor1 & filtFloor2
        
        prices = prices[filtAll]
        space = space[filtAll]
        pricesPerM2 = pricesPerM2[filtAll]
        zipCode = zipCode[filtAll]
        
        totalPrice = prices.sum()
        totalSpace = space.sum()        
        priceSdev = statistics.stdev(prices)
        spaceSdev = statistics.stdev(space) 
        medianPricePerM2.append(statistics.median(pricesPerM2))
        meanPricePerM2.append(statistics.mean(pricesPerM2))
        objectsInDataset.append(prices.size)
        
        df_dict[day] = df_tmp[filtAll]
        
        df_save_meta = pd.DataFrame({'medianPricePerM2': medianPricePerM2, 'meanPricePerM2': meanPricePerM2, 'objectsInDataset': objectsInDataset, 'priceSdev': priceSdev, 'spaceSdev': spaceSdev})
        df_meta[day] = df_save_meta
    
    
    np.save(rawDataPath + "/summarizedData/summarizedDataTill_" + rawDataDays[-1] + ".npy", df_dict) 
    np.save(rawDataPath + "/summarizedData/summarizedMetaDataTill_" + rawDataDays[-1] + ".npy", df_meta)
    print('Data read and saved')
