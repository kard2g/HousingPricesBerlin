import bs4 as bs
import urllib.request
import time
from datetime import datetime
import pandas as pd
import json
import os
from os import listdir
from os.path import isfile, join
import sys

startScraper = False 

## make rawData folder
today = str(datetime.now())[0:10]
if not os.path.isdir("rawData/" + today): 
    os.mkdir("rawData/" + today)
    print("folder: rawData/" + today + "  created.")
    print("Scraper startet.")
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
            currentURL = 'https://www.immobilienscout24.de/Suche/de/berlin/berlin/wohnung-kaufen?sorting=2' + suffix
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
    
        df.to_csv("rawData/" + today + "/"+str(datetime.now())[:19].replace(":","").replace(".","")+".csv",sep=";",decimal=",",encoding = "utf-8",index_label="timestamp")
        
        idxPage += 1
    
    print('Data scraping complete')
    
    ## join data
    SavePath = 'rawData/' + today
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
        
    df_allFiles.to_csv(SavePath + "/ScrapedData.csv",sep=";",decimal=",",encoding = "utf-8",index_label="timestamp")
    
    print('\nData joining complete')
