import xml.etree.ElementTree as ET
import pandas as pd
import os
import zipfile
from datetime import datetime


def get_actions(root):
    billactions = {}
    counter = 0
    for action in root.findall("./bill/actions/item"):
        billactions[counter] = {}
        billactions[counter]["billNumber"] = root.find("./bill/billNumber").text if root.find("./bill/billNumber") is not None else None
        billactions[counter]["billTitle"] = root.find("./bill/title").text if root.find("./bill/title") is not None else None
        billactions[counter]["billOriginalTitle"] = root.find("./bill/titles/item/title").text if root.find(
            "./bill/titles/item/title").text is not None and root.find("./bill/titles/item/titleType").text == 'Official Title as Introduced' else None
        billactions[counter]["billType"] = root.find("./bill/billType").text if root.find("./bill/billType") is not None else None
        billactions[counter]["congress"] = root.find("./bill/congress").text if root.find("./bill/congress") is not None else None
        billactions[counter]["actionDate"] = action.find("actionDate").text if action.find("actionDate") is not None else None
        billactions[counter]["actionTime"] = action.find("actionTime").text if action.find("actionTime") is not None else None
        billactions[counter]["actionCode"] = action.find("actionCode").text if action.find("actionCode") is not None else None
        billactions[counter]["type"] = action.find("type").text if action.find("type") is not None else None
        billactions[counter]["sourceSystem/code"] = action.find("sourceSystem/code").text if action.find("sourceSystem/code") is not None else None
        billactions[counter]["sourceSystem/name"] = action.find("sourceSystem/name").text if action.find("sourceSystem/name") is not None else None
        billactions[counter]["text"] = action.find("text").text if action.find("text") is not None else None
        counter += 1
    return billactions

def create_fullDate(billactions):
    fulldates = []
    for idx, row in billactions.iterrows():
        if row['actionTime'] is None:
            fulldates.append(row['actionDate'] + ' ' + '00:00:00')
        else:
            fulldates.append(row['actionDate'] + ' ' + row['actionTime'])
    billactions['fullDate'] = fulldates
    billactions['fullDate'] = pd.to_datetime(billactions['fullDate'])
    return billactions


def sort_and_deduplicate(billactions):
    billactions = billactions.sort_values(by=['fullDate', 'actionCode'], ascending=True)
    billactions = billactions.drop_duplicates() #remove dup rows
    last = 'null'
    for idx, row in billactions.iterrows():
        if row['actionCode'] == last:
            billactions = billactions.drop(idx)
        last = row['actionCode']
    return billactions


def get_actionName_and_project(billactions):
    billactions = pd.merge(billactions, actionCode_dict, how='left', on='actionCode')
    billactions = billactions[['billTitle', 'billNumber', 'billType', 'congress', 'fullDate', 'actionCode',
                               'actionName', 'type', 'sourceSystem/name', 'text', 'billOriginalTitle']]
    return billactions

os.chdir('PODS-project/obtain_data')

actionCode_dict = pd.read_csv('data/actionCode_dict.csv', sep = '\t', )[['Code','Action']]
actionCode_dict.columns = ['actionCode','actionName']

startime = datetime.now()
print('Starting process', startime)

df = pd.DataFrame()

files = os.listdir('data')
for file_zip in files:
    if file_zip.endswith('.zip'):
        unzipped_file = zipfile.ZipFile(os.getcwd() + '/data/' + file_zip, "r")
        started = datetime.now()
        print('Started', unzipped_file.filename[72:], started)
        for file_xml in sorted(zipfile.ZipFile.namelist(unzipped_file)):
            if file_xml.endswith('.xml'):
                root = ET.fromstring(unzipped_file.read(file_xml))
                billactions = get_actions(root)
                billactions = pd.DataFrame.from_dict(billactions, orient='index')
                billactions = create_fullDate(billactions)
                billactions = sort_and_deduplicate(billactions)
                billactions = get_actionName_and_project(billactions)
                df = df.append(billactions)
        print('Finished', unzipped_file.filename[72:], datetime.now(), 'took', datetime.now() - started)

df.to_csv('data/117Congress_BillActions_RAW_original_file.csv', index=False)

def get_redundant_indexs(x):
    x = x.reset_index()
    actionName= x["actionName"].values
    ind = x['index'].values
    if(len(x["text"])>1):
        for i,val in enumerate(actionName):
            if pd.isnull(val) or pd.isna(val) or val == None or val == 'None':
                redundant_indexs.append(ind[i])
    return id
df = df.reset_index(drop=True)
redundant_indexs = []
redundant_df = df[['billTitle','billNumber','billType','fullDate','text','actionName']].groupby(['billTitle','billNumber','billType','fullDate','text']).apply(lambda x: get_redundant_indexs(x))
df_log = df.loc[redundant_indexs] #Keeps a log of deleted data
df = df.drop(index=redundant_indexs)
df_log.to_csv('data/117Congress_BillActions_RAW_deleted_records.csv')

print('Finished process', datetime.now(), 'took', datetime.now() - startime)

df.to_csv('data/117Congress_BillActions_RAW.csv', index=False)