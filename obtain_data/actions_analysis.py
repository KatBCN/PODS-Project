import pandas as pd
import os


os.chdir('/home/irene/PycharmProjects/PODS_Bills')
df = pd.read_csv("data/117Congress_BillActions.csv")
print(df)
print(df.shape)  #(44592, 10)
# Duplicated actions?
df2 = df.drop_duplicates()
print(df2.shape)  #(41801, 10)

# Unique actionCode
actionCodes = df2['actionCode'].unique()
print(actionCodes.shape)  #(72,)

# nan actionCode
print(df2[df2['actionCode'].isnull()]['text'].shape)  #(11089,)
print(df2[df2['actionCode'].isnull()]['text'].unique().shape)  #(1684,)

dict_actionCode = {}
for code in actionCodes:
    if code != code:  #to identify actionCode with no value
        code_text = df2[df2['actionCode'].isnull()]['text'].unique()
    else:
        code_text = df2.loc[df2['actionCode'] == code]['text'].unique()
    dict_actionCode[code] = code_text
print(dict_actionCode)
df_actionCode = pd.DataFrame({key: pd.Series(value) for key, value in dict_actionCode.items()})
df_actionCode.to_csv('actionCode_text.csv', index=False)
