import xml.etree.ElementTree as ET
import pandas as pd
import os

###SET WORKING DIRECTORY
os.chdir('/home/irene/PycharmProjects/PODS_Bills')
print(os.getcwd())
files = os.listdir('data')  #all xml files stored in data

#APPLY READING TO EACH FILE AND MERGE THEM...
#for file in files:
#   x = read_xml(i)
#   df = df + x (rbind)

###CREATE DATAFRAME STRUCTURE:
data = {'billNumber': [],
        'billType': [],
        'congress': [],
        'actionDate': [],
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

#print(root[0].tag)
#print(root[1])
#print(root[0][0])
#print(root[0][1])
#print(root[0][2])
#print(root[0][12])

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
