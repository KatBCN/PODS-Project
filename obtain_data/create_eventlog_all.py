import xml.etree.ElementTree as ET
import pandas as pd
import os
import re
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


def sort_and_deduplicate_rows(billactions):
    billactions = billactions.sort_values(by=['fullDate', 'actionCode'], ascending=True)
    billactions = billactions.drop_duplicates() #remove dup rows
    return billactions


def get_actionName_and_project(billactions):
    billactions = pd.merge(billactions, actionCode_dict, how='left', on='actionCode')
    billactions = billactions[['billTitle', 'billNumber', 'billType', 'congress', 'fullDate', 'actionCode',
                               'actionName', 'type', 'sourceSystem/name', 'text', 'billOriginalTitle']]
    return billactions


# def deduplicate_consecutive_actions(billactions):
#     last_action = 'null'
#     last_day = 'null'
#     for idx, row in billactions.iterrows():
#         if last_action is None and row['actionCode'] is None:
#             continue
#         if row['actionCode'] == last_action and row['actionDate'] == last_day:
#             billactions = billactions.drop(idx)
#         last_action = row['actionCode']
#         last_day = row['actionDate']
#     return billactions


#Get dir
# os.chdir('/home/irene/PycharmProjects/PODS_Bills')
# os.chdir('C:/Users/mateo/PycharmProjects/PODS-Project/obtain_data/')
os.chdir('/Users/kat/Documents/PODS/project/PODS-Project/obtain_data')
# #read actionCode_dict
actionCode_df = pd.read_csv('data/updatedCodes_dict.csv', sep = ',', )
actionCode_dict = actionCode_df[['Code','Action']]
actionCode_dict.columns = ['actionCode','actionName']
#read XMLs and output raw dataframe to csv
startime = datetime.now()
print('Starting process', startime)
df_all = pd.DataFrame()
listdir = os.listdir('data')
for congress in listdir:
    if os.path.isdir('data/'+congress) and congress[1] == '1':
        print(congress)
        df_congress = pd.DataFrame()
        files = os.listdir('data/'+congress)
        for file_zip in files:
            if file_zip.endswith('.zip'):
                unzipped_file = zipfile.ZipFile(os.getcwd() + '/data/' + congress + '/' + file_zip, "r")
                started = datetime.now()
                print('Started', unzipped_file.filename[72:], started)
                for file_xml in sorted(zipfile.ZipFile.namelist(unzipped_file)):
                    if file_xml.endswith('.xml'):
                        root = ET.fromstring(unzipped_file.read(file_xml))
                        billactions = get_actions(root)
                        billactions = pd.DataFrame.from_dict(billactions, orient='index')
                        billactions = create_fullDate(billactions)
                        billactions = sort_and_deduplicate_rows(billactions)
                        billactions = get_actionName_and_project(billactions)
                        df_all = df_all.append(billactions)
                print('Finished', unzipped_file.filename[72:], datetime.now(), 'took', datetime.now() - started)
        print('Finished process', datetime.now(), 'took', datetime.now() - startime)
        df_congress.to_csv('data/event_logs/%sCongress_BillActions_RAW.csv' % congress, index=False)
df_all.to_csv('data/event_logs/ALLCongress_BillActions_RAW.csv', index=False)
print(df_all.shape)



### ADD MISSING actionCode AND actionName

# Import action code dictionary from Github link
# dfRaw = df
dfRaw = pd.read_csv('data/event_logs/ALLCongress_BillActions_RAW.csv')
dfRaw = dfRaw.astype({'billNumber': object, 'congress': object, 'fullDate': 'datetime64'})
print('duplicated rows', sum(dfRaw.duplicated()))

actionCode_df = pd.read_csv('data/updatedCodes_dict.csv')
actionCode_df.columns = ['actionCode','actionName']
actionCode_dict = dict(zip(actionCode_df.actionCode, actionCode_df.actionName))
len(actionCode_dict)

# Create function to view summary statistics of each variable.
def mySummary(df):
    for v in df.columns:
            print ("\n" + v)
            print(df[v].describe())

# Create variable of unique actionCodes
actionCodes = dfRaw['actionCode'].unique()
dfRaw.actionCode.isna().sum()

# Subset data frame per unique source system
dfLOC = dfRaw.loc[dfRaw['sourceSystem/name'] == 'Library of Congress']
dfHF = dfRaw.loc[dfRaw['sourceSystem/name'] == 'House floor actions']
dfHC = dfRaw.loc[dfRaw['sourceSystem/name'] == 'House committee actions']
dfS = dfRaw.loc[dfRaw['sourceSystem/name'] == 'Senate']

# Create subset of data frame where actionCode is missing
df = dfRaw[dfRaw['actionCode'].isnull()]

def fillCode (row): 
  # Updated by Mateo for senate discharge type
  # Updated by Kat for senate veto type
  """
  A function to fill missing actionCodes. This can be used with
  df['actionCode'] = df.apply (lambda row: fillCode(row) if pd.isnull(row['actionCode']) else row['actionCode'], axis=1)
  This has only been tested on rows with null actionCodes.
  If rows with non-null actionCodes are used, this will not work as intended.
  After filling the actionCodes, it is recommended to apply a dictionary
  of actionCodes and actionNames to complete the data.
  """
  if row['sourceSystem/name'] == "House committee actions":
    if "referred to the subcommittee" in str.lower(row['text']):
      return '3000'  # Referred to House subcommittee
    elif "markup" in str.lower(row['text']):
      return '4200'  # House committee/subcommittee markups
    elif "mark-up" in str.lower(row['text']):
      return '4200'  # House committee/subcommittee markups
    elif "hearings" in str.lower(row['text']):
      return '4100'  # House committee/subcommittee hearings
    elif "ordered to be reported" in str.lower(row['text']):
      return '4000'  # House committee/subcommittee actions
    # Generic rule based on type for text not matching earlier rules
    elif row['type'] == "Committee":
      return '4000'  # House committee/subcommittee actions
  # Setting rules for actionCodes related to the Senate
  elif row['sourceSystem/name'] == "Senate":
    if "received in the senate" in str.lower(row['text']):
      return '10000'  # Introduced in Senate
    elif "introduced in the senate" in str.lower(row['text']):
      return '10000'  # Introduced in Senate
    elif "referred to the committee" in str.lower(row['text']):
      return '11000'  # Referred to Senate committee
    elif "passed senate" in str.lower(row['text']):
      return '17000'  # Passed/agreed to in Senate
    elif all(word in str.lower((row['text'])) for word in ["committee", "filed", "report"]):
      return '14900' # Senate committee report filed after reporting
    elif row['type'] == "IntroReferral":
      return '11000'  # Referred to Senate committee
    elif row['type'] == "ResolvingDifferences":
      return '20000' # Resolving differences -- Senate actions
    elif row['type'] == "Discharge":
      if re.match('Senate Committee.*?discharged.*?', row['text']) is not None:
        return 'H12300'
      if re.match('Motion to discharge Senate Committee*', row['text']) is not None:
        return 'H17000'
    # Veto codes added by Kat 21 Dec 2021
    elif row['type'] == "Veto":
      if "failed" in str.lower(row['text']):
        return '35000'  # Failed of passage in Senate over veto
      if "message received" in str.lower(row['text']):
        return 'SenateVetoRcvd'  # Veto received in Senate
      if "message considered" in str.lower(row['text']):
        return 'SenateVetoCon'  # Veto considered in Senate
    # Generic rule based on type for text not matching earlier rules
    elif row['type'] == "Calendars":
      return 'SenateCal' # need to define a code for Senate Calendar and add to dictionary
    elif row['type'] == "Committee":
      if "hearings" in str.lower(row['text']):
        return '13100' # Senate committee/subcommittee hearings
      elif "markup" in str.lower(row['text']):
        return '13200'  # Senate committee/subcommittee markups
      elif "mark-up" in str.lower(row['text']):
        return '13200'  # Senate committee/subcommittee markups
      # Generic rule based on type for text not matching earlier rules
      else:
        return '13000' # Senate committee/subcommittee actions
    elif row['type'] == "Floor":
      if "message on senate action sent to the house" in str.lower(row['text']):
        return '5000'  # Reported to House
      if "message on house action received in senate" in str.lower(row['text']):
        return '14000'  # Reported to Senate
      # Generic rule based on type for text not matching earlier rules
      else:
        return '16000'  # Senate floor action
  else:
    return row['actionCode']  # do nothing if source system doesn't match rules



# Create a copy of original raw data to fill missing actionCodes
df = dfRaw.copy()

# Use df.apply with a lambda function to fill the missing actionCodes
# It is very important only to pass rows to the function which have a null actionCode.
df['actionCode'] = df.apply(lambda row: fillCode(row) if pd.isnull(row['actionCode']) else row['actionCode'], axis=1)

# Number of null actionCodes in original data
print(dfRaw.actionCode.isna().sum(), "null codes before assigning text to code")
print(df.actionCode.isna().sum(), "null codes after assigning text to code\n")


#merge actionNames
print(df.actionName.isna().sum(), "null names before assigning code to name")

df = pd.merge(df.drop('actionName', axis = 1), actionCode_df, how='left', on='actionCode')

print(df.actionName.isna().sum(), "null names after assigning code to name\n\nTop 5 codes without name and their counts:")
print(df[df.actionName.isna()]['actionCode'].value_counts()[:5])

#output to csv
df.to_csv('data/event_logs/ALLCongress_Bill_Actions_RAW_filled.csv', index=False)

