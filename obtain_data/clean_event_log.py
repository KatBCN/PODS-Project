import pandas as pd
import os
import datetime

# os.chdir('PODS-Project/obtain_data')

##Hard-code executive sequence times
df = pd.read_csv('data/event_logs/ALLCongress_Bill_Actions_RAW_filled.csv')
df['fullDate'] = pd.to_datetime(df['fullDate'])

for index, row in df.iterrows():
    if row['actionName'] == 'Became Public Law':
        df.loc[index,'fullDate'] = row['fullDate'] + datetime.timedelta(hours = 23, minutes = 59, seconds = 59)
    if row['actionName'] == 'Signed by President':
        df.loc[index,'fullDate'] = row['fullDate'] + datetime.timedelta(hours = 23, minutes = 59, seconds = 58)
    if row['actionName'] == 'Presented to President':
        df.loc[index,'fullDate'] = row['fullDate'] + datetime.timedelta(hours = 23, minutes = 59, seconds = 57)
    if index % 200 == 0:
        print(index)

##Remove redundant actions. This part is very slow but doesn-t get slower as it goes.

susceptibly_redundant = ['Introduced in House', 'Became Public Law', 'Signed by President', 'Presented to President']
drop_ids = []
dkt = {}
for i in susceptibly_redundant:
    dkt[i] = {}

for index, row in df.iterrows():
    if row['actionName'] in susceptibly_redundant:
        if row['fullDate'] in dkt[row['actionName']].keys():
            if row['billTitle'] in dkt[row['actionName']][row['fullDate']]:
                drop_ids.append(index)
    dkt[row['actionName']] = {row['fullDate']: []}
    dkt[row['actionName']][row['fullDate']].append(row['billTitle'])

    if index%200 == 0:
        print(index)

df_dropped = df.iloc[drop_ids]
df.drop(drop_ids, inplace=True)
print(df.shape)


df_dropped.to_csv('data/event_logs/ALLCongress_Bill_Actions_removed.csv', index=False)
df.to_csv('data/event_logs/ALLCongress_Bill_Actions_cleaning.csv', index=False)


