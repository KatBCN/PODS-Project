#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 12:40:09 2021

@author: kat
"""
import pandas as pd
import os
from datetime import datetime

os.chdir('/Users/kat/Documents/PODS/project/PODS-Project/obtain_data')


# Read .csv files into pandas data frame objects and name them
df_all = pd.read_csv('data/event_logs/ALLCongress_BillActions_RAW.csv')
df_all.name = 'ALLCongress_BillActions_RAW.csv'
df_filled = pd.read_csv('data/event_logs/ALLCongress_Bill_Actions_RAW_filled.csv')
df_filled.name = 'ALLCongress_Bill_Actions_RAW_filled.csv'
df_removed = pd.read_csv('data/event_logs/ALLCongress_Bill_Actions_removed.csv')
df_removed.name = 'ALLCongress_Bill_Actions_removed.csv'
df = pd.read_csv('data/event_logs/ALLCongress_Bill_Actions_cleaning.csv')
df.name = 'ALLCongress_Bill_Actions_cleaning.csv'

dfList = [df_all, df_filled, df_removed, df]

def printShape(df, f):
    print (df.shape, "are the dimensions of", df.name, file=f)
    
def printSourceCounts(df, f):
    print(file=f)
    print(df.name, file=f)
    print("Count of actions per source system:", file=f)
    print(df['sourceSystem/name'].value_counts(), file=f)
    
def printBillTypeCounts(df, f):
    print(file=f)
    print(df.name, file= f)
    print("Number of actions per bill type:", file=f)
    print(df['billType'].value_counts(), file=f)
    
def printActionTypeCounts(df, f):
    print(file=f)
    print(df.name, file=f)
    print("Percentage of action type in all actions:", file=f)
    print(df['type'].value_counts(normalize=True)*100, file=f)
    
def printActionNameCounts(df, f):
    print(file=f)
    print(df.name, file=f)
    print("Number of Unique Action Names in Data:", file=f)
    print(df['actionName'].nunique(), file=f)
    
def printActionCodeCounts(df, f):
    print(file=f)
    print(df.name, file=f)
    print("Number of Unique Action Codes in Data:", file=f)
    print(df['actionCode'].nunique(), file=f)

def printBillTitleCounts(df, f):
    print(file=f)
    print(df.name, file=f)
    print("Number of Unique Bill Titles in Data:", file=f)
    print(df['billTitle'].nunique(), file=f)
    

f = open("CompareEventLogs.txt", "w")

print("Updated:", datetime.now(), file=f)
print(file=f)

print("Comparing Event Logs:", file=f)
for df in dfList:
    print (df.name, file=f)
print(file=f)


for df in dfList:
    printShape(df, f)
    printSourceCounts(df, f)
    printBillTypeCounts(df, f)
    printActionTypeCounts(df, f)
    printActionNameCounts(df, f)
    printActionCodeCounts(df, f)
    printBillTitleCounts(df, f)
    print(file=f)
    print(file=f)
    
f.close()