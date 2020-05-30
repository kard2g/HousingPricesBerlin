import bs4 as bs
import urllib.request
import time
from datetime import datetime
import pandas as pd
import numpy as np
import json
import os
from os import listdir
from os.path import isfile, join
import sys

startScraper = False 

## make rawData folder
today = str(datetime.now())[0:10]
SavePath = 'rawData/personal/' + today
if not os.path.isdir(SavePath): 
    os.mkdir(SavePath)
    print("folder: rawData/personal/" + today + " created.")
    print("Start scraping.")
    startScraper = True
else:
    print("Todays folder already exists. Scraper wont start until you have verified.")

## scrape data
if startScraper:
    idxPage = 1
    while True:
    
        print('scraping page: ' + str(idxPage))
        
        df = pd.DataFrame()
        ExposeList = []
        
        try:
            suffix = '&pagenumber=' + str(idxPage)
            currentURL = 'https://www.immobilienscout24.de/Suche/shape/wohnung-kaufen-mit-balkon?rented=false&shape=e3dpX0lffXtvQWhkQXVIbHpAcWRAeFt1dUBsWGNxRGZEa3pCd0x7bURrXmNtQG9nQGZRe2ZAdGZAZ1NrUz9nbkByUHFzQHtkQHVmQHdKa2JAaUBnfUBpYEBiQWliQH5bbVxiQXNuQGRQY1lqU3VOfGlAYXtAenJCcVBseUN6Y0B2Y0dyb0F2WHhmQG5_QXB2QGpxQHpCPw..&numberofrooms=3.5-&price=0.0-850000.0&livingspace=100.0-&sorting=2' + suffix
            
            soup = bs.BeautifulSoup(urllib.request.urlopen(currentURL).read(),'lxml')
    
            for paragraph in soup.find_all("a"):
                if r"/expose/" in str(paragraph.get("href")):
                    ExposeList.append(paragraph.get("href").split("#")[0])
                ExposeList = list(set(ExposeList))
                
        except Exception as e: 
            print(str(datetime.now())+": " + str(e))
            time.sleep(1)    
        
        if not ExposeList:
            break
        
        for item in ExposeList:
            
            try:
    
                soup = bs.BeautifulSoup(urllib.request.urlopen('https://www.immobilienscout24.de'+item).read(),'lxml')
                data = pd.DataFrame(json.loads(str(soup.find_all("script")).split("keyValues = ")[1].split("}")[0]+str("}")),index=[str(datetime.now())])
                data["URL"] = str(item)
                
                beschreibung = []
                for i in soup.find_all("pre"):
                    beschreibung.append(i.text)
                data["beschreibung"] = str(beschreibung)
                df = df.append(data, sort=False)
    
            except Exception as e: 
                print(str(datetime.now())+": " + str(e))
                ExposeList = list(filter(lambda x: x != item, ExposeList))
                print("ID " + str(item) + " entfernt.")
    
        df.to_csv(SavePath + "/"+str(datetime.now())[:19].replace(":","").replace(".","")+".csv",sep=";",decimal=",",encoding = "utf-8",index_label="timestamp")
        
        idxPage += 1
    
    print('Data scraping complete')
    
    ## join data
    RohdatenFiles = [f for f in listdir(SavePath) if isfile(join(SavePath, f))]
    
    df_allFiles = pd.DataFrame()
    
    
    k = 1
    for file in RohdatenFiles:
        
        df_tmp = pd.read_csv(SavePath + "/" + file, error_bad_lines=False, warn_bad_lines=False, sep=";")
        
        df_allFiles = df_allFiles.append(df_tmp, sort=False)
        
        foo = k/len(RohdatenFiles)*100
        k += 1
        sys.stdout.write("\r %1.1f percent" %(foo))
        sys.stdout.flush()
        
    print('\nData joining complete')

    print('Cleaning Data')
    
    importantColmuns = ['obj_scoutId', 'obj_livingSpace', 'obj_purchasePrice', 'obj_streetPlain', 'obj_balcony', 'obj_hasKitchen', 'obj_courtage' , 'obj_cellar', 'obj_houseNumber', 'obj_zipCode', 'obj_condition', 'obj_parkingSpace', 'obj_lift', 'obj_typeOfFlat', 'geo_plz', 'obj_noRooms', 'obj_rented', 'obj_floor', 'obj_numberOfFloors', 'obj_regio3', 'obj_yearConstructed', 'beschreibung', 'obj_lastRefurbished', 'obj_newlyConst', 'URL', 'obj_lastRefurbish']
    
    for nameCol in df_allFiles.columns:
        
        if not nameCol in importantColmuns:
            df_allFiles = df_allFiles.drop(nameCol, 1)
    
    for nameCol in importantColmuns:
        
        if "obj_" in nameCol:
            newNameCol = nameCol[4:]
            df_allFiles.columns
            df_allFiles.rename(columns={nameCol: newNameCol}, inplace=True)
    
    try:
        df_allFiles["purchasePrice"] = df_allFiles["purchasePrice"].str.replace(",",".").astype(float)
    except:
        df_allFiles["purchasePrice"] = df_allFiles["purchasePrice"].astype(float)
        
    try:
        df_allFiles["livingSpace"] = df_allFiles["livingSpace"].str.replace(",",".").astype(float)
    except:
        df_allFiles["livingSpace"] = df_allFiles["livingSpace"].astype(float)
    
    
    df_allFiles["livingSpace"].replace(0,np.nan, inplace=True)
    df_allFiles["purchasePrice"].replace(0,np.nan, inplace=True)
    
    df_allFiles["price_per_m2"] = df_allFiles["purchasePrice"]/df_allFiles["livingSpace"]
    df_allFiles["price_per_m2"] = df_allFiles["price_per_m2"].apply(np.ceil)
    
    df_allFiles.sort_values("price_per_m2", axis=0, ascending=False, inplace=True, kind='quicksort', na_position='last')
    df_allFiles = df_allFiles.reset_index(drop=True)
    
    df_allFiles["useless"] = df_allFiles["beschreibung"].str.contains("Dachgeschossrohlinge") | df_allFiles["beschreibung"].str.contains("Dachgeschossrohling") | df_allFiles["beschreibung"].str.contains("Rohling") | df_allFiles["beschreibung"].str.contains("Genossenschaft") | df_allFiles["beschreibung"].str.contains("Dachrohling") | df_allFiles["condition"].str.contains("need_of_renovation") | df_allFiles["beschreibung"].str.contains("Zwangsversteigerung") 
    notUselessFilter = df_allFiles["useless"]==False
    df_allFiles[["price_per_m2", "useless", "URL"]].loc[notUselessFilter].tail(20)
    
    #### convert objects to float or bool
    CATEGORICAL_COLUMNS = ['streetPlain', 'condition', 'parkingSpace', 'typeOfFlat', 'regio3']
    NUMERICAL_COLUMNS = ['purchasePrice', 'livingSpace', 'zipCode', 'noRooms', 'floor', 'numberOfFloors', 'yearConstructed', 'lastRefurbish']
    BINARY_COLUMNS = ['balcony', 'hasKitchen', 'courtage', 'cellar', 'lift', 'rented', 'newlyConst']
    
    ## convert to numerical or binary
    df_allFiles.loc[:,NUMERICAL_COLUMNS] = df_allFiles.loc[:,NUMERICAL_COLUMNS].astype(str).applymap(lambda x: x.replace(",", ".")).astype(float)
    df_allFiles.loc[:,BINARY_COLUMNS] = df_allFiles.loc[:,BINARY_COLUMNS].astype(str).apply(lambda x: x.replace(["y", "n"], [True, False])).astype(bool)
    
    df_allFiles.to_csv(SavePath + "/ScrapedDataClean.csv",sep=";",decimal=".",encoding = "utf-8")