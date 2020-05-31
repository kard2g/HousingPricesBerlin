import pandas as pd
import numpy as np
from os.path import isfile, join, isdir
from os import listdir

rawDataPath = 'rawData'
rawDataDays = [f for f in listdir(rawDataPath) if isdir(join(rawDataPath, f))]
rawDataDays = sorted(rawDataDays)
try: 
    rawDataDays.remove('personal')
except ValueError: 
    pass

for day in rawDataDays:

    savePath = "rawData/" + day
    df = pd.read_csv(savePath + "/ScrapedData.csv", error_bad_lines=False, warn_bad_lines=False, sep=";")
    
    importantColmuns = ['obj_scoutId', 'obj_livingSpace', 'obj_purchasePrice', 'obj_streetPlain', 'obj_balcony', 'obj_hasKitchen', 'obj_courtage' , 'obj_cellar', 'obj_houseNumber', 'obj_zipCode', 'obj_condition', 'obj_parkingSpace', 'obj_lift', 'obj_typeOfFlat', 'geo_plz', 'obj_noRooms', 'obj_rented', 'obj_floor', 'obj_numberOfFloors', 'obj_regio3', 'obj_yearConstructed', 'beschreibung', 'obj_lastRefurbished', 'obj_newlyConst', 'URL', 'obj_lastRefurbish', 'obj_yearConstructed', 'obj_regio3']
    
    for nameCol in df.columns:
        
        if not nameCol in importantColmuns:
            df = df.drop(nameCol, 1)
    
    for nameCol in importantColmuns:
        
        if "obj_" in nameCol:
            newNameCol = nameCol[4:]
            df.columns
            df.rename(columns={nameCol: newNameCol}, inplace=True)
    
    try:
        df["purchasePrice"] = df["purchasePrice"].str.replace(",",".").astype(float)
    except:
        df["purchasePrice"] = df["purchasePrice"].astype(float)
        
    try:
        df["livingSpace"] = df["livingSpace"].str.replace(",",".").astype(float)
    except:
        df["livingSpace"] = df["livingSpace"].astype(float)
    
    
    df["livingSpace"].replace(0,np.nan, inplace=True)
    df["purchasePrice"].replace(0,np.nan, inplace=True)
    
    df["price_per_m2"] = df["purchasePrice"]/df["livingSpace"]
    df["price_per_m2"] = df["price_per_m2"].apply(np.ceil)
    
    df.sort_values("price_per_m2", axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last')
    df = df.reset_index(drop=True)
    
    df["useless"] = df["beschreibung"].str.contains("Dachgeschossrohlinge") | df["beschreibung"].str.contains("Dachgeschossrohling") | df["beschreibung"].str.contains("Rohling") | df["beschreibung"].str.contains("Genossenschaft") | df["beschreibung"].str.contains("Dachrohling") | df["condition"].str.contains("need_of_renovation") | df["beschreibung"].str.contains("Zwangsversteigerung") 
    notUselessFilter = df["useless"]==False
    df[["price_per_m2", "useless", "URL"]].loc[notUselessFilter].tail(20)
    
    #### convert objects to float or bool
    CATEGORICAL_COLUMNS = ['streetPlain', 'condition', 'parkingSpace', 'typeOfFlat', 'regio3']
    NUMERICAL_COLUMNS = ['purchasePrice', 'livingSpace', 'zipCode', 'noRooms', 'floor', 'numberOfFloors', 'yearConstructed', 'lastRefurbish']
    BINARY_COLUMNS = ['balcony', 'hasKitchen', 'courtage', 'cellar', 'lift', 'rented', 'newlyConst']
    
    ## convert to numerical or binary
    df.loc[:,NUMERICAL_COLUMNS] = df.loc[:,NUMERICAL_COLUMNS].astype(str).applymap(lambda x: x.replace(",", ".")).astype(float)
    df.loc[:,BINARY_COLUMNS] = df.loc[:,BINARY_COLUMNS].astype(str).apply(lambda x: x.replace(["y", "n"], [True, False])).astype(bool)
    
    df.to_csv(savePath + "/ScrapedDataClean.csv",sep=";",decimal=".",encoding = "utf-8")
