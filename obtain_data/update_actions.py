#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 22 09:49:57 2021

@author: kat
"""

import pandas as pd
import os
import re


#Get dir
# os.chdir('/home/irene/PycharmProjects/PODS_Bills')
# os.chdir('C:/Users/mateo/PycharmProjects/PODS-Project/obtain_data/')
os.chdir('/Users/kat/Documents/PODS/project/PODS-Project/obtain_data')

# create actionCode_dict reading the most recent updatedCodes file
actionCode_df = pd.read_csv('data/updatedCodes_dict.csv', sep = ',', )
actionCode_df.columns = ['actionCode','actionName']
# convert pandas df of action codes to python dictionary
actionCode_dict = dict(zip(actionCode_df.actionCode, actionCode_df.actionName))


def fillCode (row): 
  # Updated by Mateo for senate discharge type
  # Updated by Kat for senate veto type
  """
  A function to fill missing actionCodes. This can be used with
  df['actionCode'] = df.apply (lambda row: fillCode(row) if pd.isnull(row['actionCode']) else row['actionCode'], axis=1)
  This has only been tested on rows with null actionCodes.
  If rows with non-null actionCodes are used, this will not work as intended.
  After filling the actionCodes, it is recommended to apply a dictionary
  of actionCodes and actionNames to complete the data for missing names.
  """
  # Setting rules for actionCodes related to the House Committees:
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
        return '14500'
      if re.match('Motion to discharge Senate Committee*', row['text']) is not None:
        return 'SenateMotionDischarge'
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

# Read raw data to fill missing actionCodes
df_all = pd.read_csv('data/event_logs/ALLCongress_BillActions_RAW.csv')
df = df_all.copy()

# Use df.apply with a lambda function to fill the missing actionCodes
# It is very important only to pass rows to the function which have a null
# actionCode in order to avoid overwriting the original code.
df['actionCode'] = df.apply(lambda row: fillCode(row) if pd.isnull(row['actionCode']) else row['actionCode'], axis=1)

# Number of null actionCodes in data
print(df_all.actionCode.isna().sum(), "actions with null codes before calling fillCode()")
print(df.actionCode.isna().sum(), "actions with null codes after calling fillCode()\n")

# Number of null actionNames in data
# Since we didn't edit actionNames as part of fillCode(), these values should match.
print(df_all.actionCode.isna().sum(), "actions with null names before calling fillCode()")
print(df.actionName.isna().sum(), "actions with null names after calling fillCode()")

# Fill actionNames by merging pandas df of actionCodes with the df of
# all actions with filled actionCodes.
df = pd.merge(df.drop('actionName', axis = 1), actionCode_df, how='left', on='actionCode')

print(df.actionName.isna().sum(), "actions with null names after merging\n")
print("\nTop 5 codes without name and their counts:")
print(df[df.actionName.isna()]['actionCode'].value_counts()[:5])


# # Uncomment the section below when you are ready to update the dictionary.

# # Create copy of dictionary to use for updating
# updatedCode_dict = actionCode_dict.copy()

# # Add new code:name mappings after evaluation of top codes that are missing names.
# updatedCode_dict.update( {'SenateMotionDischarge' : 'Motion to Discharge Senate Committee'})  

# # Save updated dictionary to files
# updatedCode_dict_df = pd.DataFrame.from_dict(updatedCode_dict, orient='index') 
# updatedCode_dict_df.index.names = ['Code']
# updatedCode_dict_df.columns = ['Action']
# # Line to write file commented out
# updatedCode_dict_df.to_csv (r'updatedCodes_dict.csv', index = True, header=True)

