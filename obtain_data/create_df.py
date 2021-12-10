import xml.etree.ElementTree as ET
import pandas as pd
import os

###SET WORKING DIRECTORY
os.chdir('PODS-Project/obtain_data')

print(os.getcwd())
files = os.listdir()  #all xml files stored in data

#APPLY READING TO EACH FILE AND MERGE THEM...
#for file in files:
#   x = read_xml(i)
#   df = df + x (rbind)

###CREATE DATAFRAME STRUCTURE:
data = {'billNumber': [],
        'billType': [],
        'congress': [],
        'actionDate': [],
        'actionCode': [],
        'committees': [],
        'links': [],
        'text': [],
        'type': [],
        'sourceSystem_code': [],
        'sourceSystem_name': []}
df = pd.DataFrame(data)
print(df)

###LOAD FILE
etree = ET.parse('data/BILLSTATUS-117hr1.xml')
root = etree.getroot()

print(root[0].text)
print(root[0])
print(root[0][0])
print(root[0][1])
print(root[0][2])
print(root[0][12])

###ADD VALUES TO DATAFRAME
#Default values for bill information:
billNumber = 'NULL'
billType = 'NULL'
congress = 'NULL'
for bill_info in root[0]:
    #Bill information
    if bill_info.tag == 'billNumber':
        billNumber = bill_info.text
    elif bill_info.tag == 'billType':
        billType = bill_info.text
    elif bill_info.tag == 'congress':
        congress = bill_info.text
    elif bill_info.tag == 'actions':
        for action in bill_info:
            #Actions information
            if action.tag == 'item':
                #Default values:
                actionDate = 'NULL'
                committees = 'NULL'
                links = 'NULL'
                sourceSystem_code = 'NULL'
                sourceSystem_name = 'NULL'
                text = 'NULL'
                type = 'NULL'
                for action_info in action:
                    if action_info.tag == 'actionDate':
                        actionDate = action_info.text
                    if action_info.tag == 'committees':
                        committees = action_info.text
                    if action_info.tag == 'links':
                        links = action_info.text
                    if action_info.tag == 'sourceSystem_code':
                        sourceSystem_code = action_info.text
                    if action_info.tag == 'sourceSystem_name':
                        sourceSystem_name = action_info.text
                    if action_info.tag == 'text':
                        text = action_info.text
                    if action_info.tag == 'type':
                        type = action_info.text
                df = df.append({'billNumber': billNumber,
                                'billType': billType,
                                'congress': congress,
                                'actionDate': actionDate,
                                'committees': committees,
                                'links': links,
                                'sourceSystem_code': sourceSystem_code,
                                'sourceSystem_name': sourceSystem_name,
                                'text': text,
                                'type': type}, ignore_index=True)
            else:
                print(action.tag)  #actionTypeCounts & actionByCounts

###SAVE TABLE IN CSV FILE
print(df)
df.to_csv(index=False)
print('saved')

### Mateo's code for a new log.

### Create dataframe with actions for 1 bill
#get actions
billactions = {}
counter = 0
for action in root.findall("./bill/actions/item"):
    print("-----", counter, "-----")
    billactions[counter] = {}
    billactions[counter]["actionDate"] = action.find("actionDate").text if action.find("actionDate") is not None else None
    billactions[counter]["actionTime"] = action.find("actionTime").text if action.find("actionTime") is not None else None
    billactions[counter]["actionCode"] = action.find("actionCode").text if action.find("actionCode") is not None else None
    billactions[counter]["type"] = action.find("type").text if action.find("type") is not None else None
    billactions[counter]["congress"] = action.find("congress").text if action.find("congress") is not None else None
    billactions[counter]["sourceSystem/code"] = action.find("sourceSystem/code").text if action.find("sourceSystem/code") is not None else None
    billactions[counter]["sourceSystem/name"] = action.find("sourceSystem/name").text if action.find("sourceSystem/name") is not None else None
    billactions[counter]["text"] = action.find("text").text if action.find("text") is not None else None
    counter += 1

#convert to df
billactions = pd.DataFrame.from_dict(billactions, orient = 'index')

#create column with date-time. actions with no actionTime are given an arbitrary time '00:00:00' - May create biases.
fulldates = []
for idx, row in billactions.iterrows():
    if row['actionTime'] is None:
        fulldates.append(row['actionDate'] + ' ' + '00:00:00')
    else:
        fulldates.append(row['actionDate'] + ' ' + row['actionTime'])
billactions['fullDate'] = fulldates
billactions['fullDate'] = pd.to_datetime(billactions['fullDate'])

#sort by date, remove previous date,time, congress, and sourceSystem/code columns. Also removing duplicate actions
billactions = billactions.sort_values(by = ['fullDate', 'actionCode'], ascending = True)
billactions = billactions[['fullDate','actionCode', 'type',  'sourceSystem/name', 'text']]
billactions = billactions.drop_duplicates()

#deduplicate consecutive actionCodes that belong to actual, different actions
last = 'null'
for idx, row in billactions.iterrows():
    if row['actionCode'] == last:
        billactions = billactions.drop(idx)
    last = row['actionCode']

#get action code meanings
actionCode_dict = pd.read_csv('../actionCode_dict.csv.txt', sep = '\t', )[['Code','Action']]
actionCode_dict.columns = ['actionCode','actionName']
billactions = pd.merge(billactions, actionCode_dict, how = 'left', on = 'actionCode')
billactions = billactions[['fullDate','actionCode', 'type',  'sourceSystem/name', 'actionName', 'text']]

#save to csv
billactions.to_csv('BillActions.csv', index=False)