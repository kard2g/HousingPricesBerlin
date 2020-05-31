#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 31 21:05:49 2020

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
import webbrowser

def quickOpen(expose):
    url = 'https://www.immobilienscout24.de' + expose
    try:
        webbrowser.open(url)
    except:
        pass

def writeAllDataToDict(rawDataPath):

    rawDataDays = [f for f in listdir(rawDataPath) if isdir(join(rawDataPath, f))]
    rawDataDays = sorted(rawDataDays)
    try: 
        rawDataDays.remove('personal')
    except ValueError: 
        pass
        
    df_dict = {}
    
    for day in rawDataDays:
        
        df_tmp = pd.read_csv(rawDataPath + "/" + day + "/ScrapedDataClean.csv", error_bad_lines=False, warn_bad_lines=False, sep=";", index_col=0, decimal=",")
    
        df_tmp["livingSpace"] = df_tmp["livingSpace"].astype(float)
        df_tmp["purchasePrice"] = df_tmp["purchasePrice"].astype(float)
        df_tmp["price_per_m2"] = df_tmp["price_per_m2"].astype(float)
        df_tmp["zipCode"] = df_tmp["zipCode"].astype(float)
        df_tmp["floor"] = df_tmp["floor"].astype(float)
            
        df_dict[day] = df_tmp
    
    return df_dict
    