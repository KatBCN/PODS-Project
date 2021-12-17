import pandas as pd
import re
import os

#Get dir
os.chdir('PODS-project/obtain_data')

### ADD MISSING actionCode AND actionName

# Import action code dictionary from Github link
dfRaw = pd.read_csv('data/117Congress_BillActions_RAW.csv')
dfRaw = dfRaw.astype({'billNumber':object, 'congress':object, 'fullDate':'datetime64'})
print('duplicated rows', sum(dfRaw.duplicated()))

actionCode_df = pd.read_csv("https://raw.githubusercontent.com/KatBCN/PODS-Project/Irene/obtain_data/data/actionCode_dict.csv", sep = '\t', )[['Code','Action']]
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
df['actionCode'] = df.apply (lambda row: fillCode(row) if pd.isnull(row['actionCode']) else row['actionCode'], axis=1)

# Number of null actionCodes in original data
print(dfRaw.actionCode.isna().sum(), "nulls before assigning text to code")
print(df.actionCode.isna().sum(), "nulls after assigning text to code")




#clean data (remove sequentially repeated actions, remove redundant actions, hardcode known action sequences, etc)

new_dict = {'Intro-H' : 'Introduced in House', # IntroReferral
            'H30300' : 'Motion to suspend rules and pass bill', # House Floor
            'H37220' : 'Further proceedings postponed', #  House Floor
            'H1B000' : 'Proceedings are considered vacated', #  Senate Calendars
            'SenateCal' : 'Placed on Senate Legislative Calendar',
            'E40000' : 'Became Public Law', # President # Generalization needed
            'H37100' : 'Passed/agreed to in House', # House Floor
            'H36210' : 'Motion to recommit Failed', # House Floor
            'H36200' : 'Motion to recommit to Committee', # House Floor - Should occur prior to H36210
            'H8A000' : "Motion to recommit ordered", # House Floor
            'H38800' : 'Title of measure amended', # House Floor
            'H38900' : 'Clerk technical correction', # House Floor
            '19500' : actionCode_dict['19000'], # House Floor - same as 19000, but possibly after senate amendment
            'H41931' : 'Motion to Reconsider Agreed', # House Resolving Differences
            'H41610' : actionCode_dict['19000'], # House Resolving Differences - same as 19000, but possibly after senate amendment
            'H30200' : 'Motion to Consider', # House Floor
            'H12420' : 'Placed on House Calendar', # House Calendars
            'H11210' : 'House committee time extension', # House Intro Referral - same as 4900
            'H82000' : 'Motion to table Motion to Reconsider', # House Resolving Differences
            'H36610' : 'Motion to table Motion to Reconsider Agreed', # House Floor
            'H36600' : 'Motion to table Motion to Reconsider', # House Floor - same as H82000
            '20500' : actionCode_dict['20000'], # Senate Resolving Differences - same as 20000, but possibly after house amendment
            'H41400' : actionCode_dict['H35000']} # House Resolving Differences - same as H35000

new_dict_df = pd.DataFrame(new_dict.items(), columns=['actionCode', 'actionName'])
action_dict_completer = pd.concat([actionCode_df, new_dict_df])

df = pd.merge(df, action_dict_completer, how='left', on='actionCode')
df.to_csv('117Congress_Bill_Actions_RAW_filled.csv', index=False)

'H12210', 'H12440', 'H30800', 'H38400', 'H38410', 'H40110', 'H40130', 'H40140', 'H40150', 'H41930'