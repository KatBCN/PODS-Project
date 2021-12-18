import pandas as pd
import os


os.chdir('/home/irene/PycharmProjects/PODS_Bills')
df = pd.read_csv("data/117Congress_BillActions_RAW.csv")
print(df)
print(df.shape)  #(38219, 11)

# Unique actionCode
actionCodes = df['actionCode'].unique()
print(actionCodes.shape)  #(72,)

# actionCode without actionName
print(df[df['actionName'].isnull()]['actionCode'].shape) #(16038,)
print(df[df['actionName'].isnull()]['actionCode'].unique().shape) #(41,)
actionCodes_wo_name = df[df['actionName'].isnull()]['actionCode'].unique()

dict_actionCode = {}
wo_actionCode = pd.DataFrame()
for code in actionCodes_wo_name:
    if code != code:  #to identify actionCode with no value
        wo_actionCode = df[df['actionCode'].isnull()]
    else:
        code_text = df.loc[df['actionCode'] == code]['text'].unique()
        dict_actionCode[code] = code_text
print(dict_actionCode)
df_actionCode = pd.DataFrame({key: pd.Series(value) for key, value in dict_actionCode.items()})
df_actionCode.to_csv('actionCode_text.csv', index=False)
wo_actionCode.to_csv('wo_actionCode.csv', index=False)

actionCode_wo_name = pd.read_csv("actionCode_text.csv")
print(actionCode_wo_name.shape)  #(140, 40)
list_codes = list(actionCode_wo_name)

###   0_Intro-H   ###
print(list_codes[0])
len(df[df['actionCode'] == list_codes[0]])  #6990
actionCode_wo_name[list_codes[0]].unique()
# Introduced in House

###   1_H37100   ###
print(list_codes[1])
len(df[df['actionCode'] == list_codes[1]])  #153
actionCode_wo_name[list_codes[1]].unique()
# On agreeing to the resolution Agreed to without objection. (text: CR ...(code)...)/()
# On agreeing to the resolution Agreed to by the Yeas and Nays: .(num). - .(num). (Roll no. .(num).). (text: CR .(code).)/()
# On passage Passed without objection. (text: CR .(code).)/()
# On passage Passed by the Yeas and Nays: .(num). - .(num). (Roll no. .(num).). (text: CR .(code).)/()

###   2_H30200   ###
print(list_codes[2])
len(df[df['actionCode'] == list_codes[2]])  #21
actionCode_wo_name[list_codes[2]].unique()
# Without objection, the Chair laid before the House H. Con. Res. .(num).. (consideration: CR .(code).)/()
# Mr./Ms. .(name). asked unanimous consent to discharge from committee and consider.
# Mr./Ms. .(name). asked unanimous consent to take from the Speaker's table and consider.
# Mr./Ms. .(name). asked unanimous consent to consider as introduced.

###   3_H1B000   ###
print(list_codes[3])
len(df[df['actionCode'] == list_codes[3]])  #125
actionCode_wo_name[list_codes[3]].unique()
# Pursuant to the provisions of H. Res. .(num)., (H. Con. Res.)/(S. Con. Res.)/(H. Res.) .(num). is considered passed House. (consideration: CR .(code).; text: CR .(code).)/(text: CR .(code).)/(consideration: CR .(code).)
# Pursuant to the provisions of H. Res. .(num)., proceedings on (H.R.)/(S.)/(H. Res.) .(num). are considered vacated.
# Pursuant to the provisions of H.Res. 716, House agreed to Senate amendment to House amendment --- unique?

###   4_H30300   ###
print(list_codes[4])
len(df[df['actionCode'] == list_codes[4]])  #292
actionCode_wo_name[list_codes[4]].unique()
# Mr./Ms. .(name). moved to suspend the rules and agree to the resolution(, as amended)/().
# Mr./Ms. .(name) moved to suspend the rules and pass the bill(, as amended)/().

###   5_H36200   ###
print(list_codes[5])
len(df[df['actionCode'] == list_codes[5]])  #28
actionCode_wo_name[list_codes[5]].unique()
# Mr./Ms. .(name). moved to recommit to the Committee on .(committee_name).. (text: CR .(code).)
# Mr. Brady moved to commit to the Committee on Ways and Means. (text: CR H5534) --- unique: commit instead of recommit

###   6_H8A000   ###
print(list_codes[6])
len(df[df['actionCode'] == list_codes[6]])  #26
actionCode_wo_name[list_codes[6]].unique()
# The previous question on the motion to recommit was ordered pursuant to the rule.
# The previous question on the motion (to recommit)/(to commit)/() was ordered pursuant (to)/() clause 2(b) of rule XIX.
# The previous question on the motion (to recommit)/() was ordered without objection.

###   7_H36210   ###
print(list_codes[7])
len(df[df['actionCode'] == list_codes[7]])  #29
actionCode_wo_name[list_codes[7]].unique()
# On motion to recommit Failed by the Yeas and Nays: .(num). - .(num). (Roll no. .(num).).
# On motion to commit Failed by the Yeas and Nays: 211 - 219 (Roll no. 309). --- unique: commit instead of recommit
# On motion to table the motion to refer Agreed to by the Yeas and Nays: 214 - 196 (Roll no. 5). --- unique

###   8_H38900   ###
print(list_codes[8])
len(df[df['actionCode'] == list_codes[8]])  #9
actionCode_wo_name[list_codes[8]].unique()
# The Clerk was authorized to correct section numbers, punctuation, and cross references, and to make other necessary technical and conforming corrections in the engrossment of H.R. .(num)..

###   9_H37220   ###
print(list_codes[9])
len(df[df['actionCode'] == list_codes[9]])  #220
actionCode_wo_name[list_codes[9]].unique()
# At the conclusion of debate, (the Yeas and Nays were)/(a recorded vote was) demanded and ordered. Pursuant to the provisions of clause 8, rule XX, the Chair announced that further proceedings on the motion would be postponed. (text: CR H2360-2361)/()

###   10_H38800   ###
print(list_codes[10])
len(df[df['actionCode'] == list_codes[10]])  #18
actionCode_wo_name[list_codes[10]].unique()
# The title of the measure was amended. Agreed to without objection.

###   11_19500   ###
print(list_codes[11])
len(df[df['actionCode'] == list_codes[11]])  #8
actionCode_wo_name[list_codes[11]].unique()
# Resolving differences -- House actions: On motion that the House (agree to)/(suspend the rules and agree to)/(concur in) the Senate amendment Agreed to (without objection)/(by the Yeas and Nays: ()/((2/3 required):) .(num). - .(num). (Roll no. .(num).)).(text: CR .(code).)/(consideration: CR H6230-6231)/()

###   12_H41610   ###
print(list_codes[12])
len(df[df['actionCode'] == list_codes[12]])  #8
actionCode_wo_name[list_codes[12]].unique()
# On motion that the House (agree to)/(suspend the rules and agree to)/(concur in) the Senate amendment Agreed to (without objection)/(by the Yeas and Nays: .(num). - .(num). (Roll no. .(num).)). (text: CR .(code).)

###   13_H41931   ###
print(list_codes[13])
len(df[df['actionCode'] == list_codes[13]])  #8
actionCode_wo_name[list_codes[13]].unique()
# Motion to reconsider laid on the table Agreed to without objection.
# On motion to table the motion to reconsider Agreed to by the Yeas and Nays: 228 - 205 (Roll no. 370).

###   14_H40150   ###
print(list_codes[14])
len(df[df['actionCode'] == list_codes[14]])  #2
actionCode_wo_name[list_codes[14]].unique()
# Mr./Ms. .(name). moved that the House (agree to)/(concur in) the Senate amendment. (consideration: CR .(code).)/(CR .(code).)

###   15_H41400   ###
print(list_codes[15])
len(df[df['actionCode'] == list_codes[15]])  #3
actionCode_wo_name[list_codes[15]].unique()
# The previous question was ordered pursuant to (the rule)/(a previous order of the House).

###   16_H12440   ###
print(list_codes[16])
len(df[df['actionCode'] == list_codes[16]])  #2
actionCode_wo_name[list_codes[16]].unique()
# Motion to place bill on Consensus Calendar filed by Mr./Ms. .(name)..

###   17_H40110   ###
print(list_codes[17])
len(df[df['actionCode'] == list_codes[17]])  #2
actionCode_wo_name[list_codes[17]].unique()
# Without objection, the Chair laid before the House H.R. 1651  along with the Senate amendment thereto. (consideration: CR H1687)
# Mr. Takano asked unanimous consent that the House agree to the Senate amendment. (consideration: CR H2772-2773)

###   18_H40140   ###
print(list_codes[18])
len(df[df['actionCode'] == list_codes[18]])  #2
actionCode_wo_name[list_codes[18]].unique()
# Mr./Ms. .(name). moved that the House suspend the rules and (agree to)/(concur in) the Senate amendment. (consideration: CR .(code).)

###   19_H11210   ###
print(list_codes[19])
len(df[df['actionCode'] == list_codes[19]])  #5
actionCode_wo_name[list_codes[19]].unique()
# House Committee on .(committee_name). Granted an extension for further consideration ending not later than .(date)..

###   20_H36600   ###
print(list_codes[20])
len(df[df['actionCode'] == list_codes[20]])  #9
actionCode_wo_name[list_codes[20]].unique()
# Mr./Ms. .(name). moved to reconsider.
# Mr./Ms. .(name). moved to table the motion to reconsider ()/(the vote).
# Ms. Cheney moved On agreeing to that portion electing the Chaplain.
# Mr. Jeffries moved On agreeing to the remainder of the resolution.
# Mr. McGovern moved on consideration of the resolution. (CR H6230)
# Mr. Cole moved to postpone consideration to a day certain.

###   21_H36610   ###
print(list_codes[21])
len(df[df['actionCode'] == list_codes[21]])  #9
actionCode_wo_name[list_codes[21]].unique()
# (On motion to )/()table the motion to (reconsider)/(postpone consideration to a day certain) Agreed to by the Yeas and Nays: .(num) - .(num). (Roll no. .(num).).
# On agreeing to (that portion electing the Chaplain)/(the remainder of the resolution) Agreed to by voice vote.
# On Consideration of the Resolution Agreed to by the Yeas and Nays: 215 - 212 (Roll no. 368).

###   22_H12210   ###
print(list_codes[22])
len(df[df['actionCode'] == list_codes[22]])  #5
actionCode_wo_name[list_codes[22]].unique()
# Supplemental report filed by the Committee on .(committee_name)., H. Rept. .(nums)., Part II.

###   23_H12420   ###
print(list_codes[23])
len(df[df['actionCode'] == list_codes[23]])  #43
actionCode_wo_name[list_codes[23]].unique()
# Placed on the House Calendar, Calendar No. .(num)..

###   24_H30800   ###
print(list_codes[24])
len(df[df['actionCode'] == list_codes[24]])  #2
actionCode_wo_name[list_codes[24]].unique()
# Consideration initiated (pursuant to a previous order)/(by the Chair).

###   25_H41930   ###
print(list_codes[25])
len(df[df['actionCode'] == list_codes[25]])  #1
actionCode_wo_name[list_codes[25]].unique()
# Kelly (IL) moved to reconsider the vote. (CR H6231) --- unique

###   26_H82000   ###
print(list_codes[26])
len(df[df['actionCode'] == list_codes[26]])  #6
actionCode_wo_name[list_codes[26]].unique()
# Mr./Ms. .(name). moved to table the motion to (reconsider the vote (CR H6231))/(reconsider)/(postpone consideration to a day certain)/(refer)

###   27_H38400   ###
print(list_codes[27])
len(df[df['actionCode'] == list_codes[27]])  #2
actionCode_wo_name[list_codes[27]].unique()
# Mr. .(name). moved to reconsider the vote.

###   28_H38410   ###
print(list_codes[28])
len(df[df['actionCode'] == list_codes[28]])  #1
actionCode_wo_name[list_codes[28]].unique()
# On motion to table the motion to reconsider Agreed to by the Yeas and Nays: 219 - 209 (Roll no. 248).

###   29_H40130   ###
print(list_codes[29])
len(df[df['actionCode'] == list_codes[29]])  #1
actionCode_wo_name[list_codes[29]].unique()
# Pursuant to a previous special order the House moved to agree to the Senate amendment.

###   30_20500   ###
print(list_codes[30])
len(df[df['actionCode'] == list_codes[30]])  #3
actionCode_wo_name[list_codes[30]].unique()
# Resolving differences -- Senate actions: Senate concurred in the House amendment to S.1301 with an amendment (SA 3847) by Yea-Nay Vote. 50 - 48. Record Vote Number: 412.(text of amendment in the nature of a substitute: CR S6993-6994)
# Resolving differences -- Senate actions: Senate agreed to the House amendment to S. 1511 by Unanimous Consent.(consideration: CR S8054)
# Resolving differences -- Senate actions: Senate agreed to the House amendment to S. 610 by Yea-Nay Vote. 59 - 35. Record Vote Number: 491.(consideration: CR S9081)

###   31_H12700   ###
print(list_codes[31])
len(df[df['actionCode'] == list_codes[31]])  #35
actionCode_wo_name[list_codes[31]].unique()
# Rule provides for consideration of S. Con. Res. 5 with 1 hour of general debate.
# Rule provides for 1 hour of general debate on H.R. 803 and one motion to recommit. Rule provides for 90 minutes of general debate on H.R. 5 and one motion to recommit.
# The resolution provides that the amendment printed in the Rules Committee report shall be considered as adopted and the bill, as amended, shall be considered as read.
# ..............

###   32_80000   ###
print(list_codes[32])
len(df[df['actionCode'] == list_codes[32]])  #1
actionCode_wo_name[list_codes[32]].unique()
# Amendment failed by House: Pursuant to the provisions of H. Res. 179, H. Res. 176 is considered passed House.

###   33_H30230   ###
print(list_codes[33])
len(df[df['actionCode'] == list_codes[33]])  #1
actionCode_wo_name[list_codes[33]].unique()
# An objection was heard to the unanimous consent request to consider the measure.

###   34_H36500   ###
print(list_codes[34])
len(df[df['actionCode'] == list_codes[34]])  #4
actionCode_wo_name[list_codes[34]].unique()
# Mr. Hoyer moved to table the measure.

###   35_H36510   ###
print(list_codes[35])
len(df[df['actionCode'] == list_codes[35]])  #4
actionCode_wo_name[list_codes[35]].unique()
# On motion to table the measure Agreed to by the Yeas and Nays: .(num). - .(num)., (3 Present )/()(Roll no. .(num).). ()/(text: CR .(code).)

###   36_H12490   ###
print(list_codes[36])
len(df[df['actionCode'] == list_codes[36]])  #1
actionCode_wo_name[list_codes[36]].unique()
# Discharged from House Calendar.

###   37_H36700   ###
print(list_codes[37])
len(df[df['actionCode'] == list_codes[37]])  #1
actionCode_wo_name[list_codes[37]].unique()
# Mr. Davis, Rodney moved to refer to a select committee.

###   38_H36100   ###
print(list_codes[38])
len(df[df['actionCode'] == list_codes[38]])  #1
actionCode_wo_name[list_codes[38]].unique()
# Mr. Smith (MO) moved to commit with instructions to a select committee. (text: CR H35)

###   39_H36110   ###
print(list_codes[39])
len(df[df['actionCode'] == list_codes[39]])  #1
actionCode_wo_name[list_codes[39]].unique()
# On motion to commit with instructions Failed by the Yeas and Nays: 203 - 217 (Roll no. 7).





# Similar to other actionCode?

# actionCode with actionName
print(df[df['actionName'].notnull()]['actionCode'].shape)  #(22181,)
print(df[df['actionName'].notnull()]['actionCode'].unique().shape)  #(31,)
actionCodes_with_name = df[df['actionName'].notnull()]['actionCode'].unique()

dict_actionCode_with_name = {}
for code in actionCodes_with_name:
    code_text = df.loc[df['actionCode'] == code]['text'].unique()
    dict_actionCode_with_name[code] = code_text
print(dict_actionCode_with_name)
df_actionCode_with_name = pd.DataFrame({key: pd.Series(value) for key, value in dict_actionCode_with_name.items()})
df_actionCode_with_name.to_csv('actionCode_with_name_text.csv', index=False)

actionCode_with_name = pd.read_csv("actionCode_with_name_text.csv")
print(actionCode_with_name.shape)  #(140, 40)
list_codes = list(actionCode_with_name)


actionCode_dict = pd.read_csv("data/actionCode_dict.csv", sep='\t')
list(actionCode_dict)

###   0_1000   ###
print(list_codes[0])
len(df[df['actionCode'] == list_codes[0]])  #7041
actionCode_with_name[list_codes[0]].unique()
# Introduced in House
actionCode_dict[actionCode_dict['Code'] == list_codes[0]]['Action'].unique()
#Introduced in House

###   1_H30000   ###
print(list_codes[1])
len(df[df['actionCode'] == list_codes[1]])  #611
actionCode_with_name[list_codes[1]].unique()
# Considered under suspension of the rules.
# Considered as unfinished business.
# Considered under the provisions of rule H. Res. 535.
# Considered as privileged matter.
# Considered by unanimous consent.
actionCode_dict[actionCode_dict['Code'] == list_codes[1]]['Action'].unique()
# Consideration by House

###   2_8000   ###
print(list_codes[2])
len(df[df['actionCode'] == list_codes[2]])  #454
actionCode_with_name[list_codes[2]].unique()
# Passed/agreed to in House: On agreeing to the resolution Agreed to by the Yeas and Nays / without objection
# Passed/agreed to in House: Pursuant to the provisions of H. Res. 330, H. Con. Res. 30 is considered passed House.
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[2]]['Action'].unique()
# Passed/agreed to in House

###   3_H38310   ###
print(list_codes[3])
len(df[df['actionCode'] == list_codes[3]])  #331
actionCode_with_name[list_codes[3]].unique()
# Motion to reconsider laid on the table Agreed to without objection.
# Motion to reconsider laid on the table Objection heard.
actionCode_dict[actionCode_dict['Code'] == list_codes[3]]['Action'].unique()
# Motion To Reconsider Results

###   4_17000   ###
print(list_codes[4])
len(df[df['actionCode'] == list_codes[4]])  #397
actionCode_with_name[list_codes[4]].unique()
# Passed/agreed to in Senate: Resolution agreed to in Senate without amendment and with a preamble by Unanimous Consent
# Passed/agreed to in Senate: Submitted in the Senate, considered, and agreed to without amendment and with a preamble by Unanimous Consent.
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[4]]['Action'].unique()
# Passed/agreed to in Senate

###   5_H11100   ###
print(list_codes[5])
len(df[df['actionCode'] == list_codes[5]])  #6938
actionCode_with_name[list_codes[5]].unique()
# Referred to the Committee on Science, Space, and Technology, and in addition to the Committees on Foreign Affairs, and Natural Resources, for a period to be subsequently determined by the Speaker, in each case for consideration of such provisions as fall within the jurisdiction of the committee concerned.
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[5]]['Action'].unique()
# Referred to the Committee

###   6_H1L210   ###
print(list_codes[6])
len(df[df['actionCode'] == list_codes[6]])  #61
actionCode_with_name[list_codes[6]].unique()
# Rules Committee Resolution H. Res. 479 Reported to House. Rule provides for consideration of S. 475 with 1 hour of general debate. The resolution provides for one motion to commit.
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[6]]['Action'].unique()
# Rule provides for consideration of

###   7_H1L220   ###
print(list_codes[7])
len(df[df['actionCode'] == list_codes[7]])  #29
actionCode_with_name[list_codes[7]].unique()
# Rule H. Res. 38 passed House.', 'Rule H. Res. 41 passed House.
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[7]]['Action'].unique()
# Rule passed/agreed in House

###   8_H8D000   ###
print(list_codes[8])
len(df[df['actionCode'] == list_codes[8]])  #460
actionCode_with_name[list_codes[8]].unique()
# DEBATE - The House proceeded with one hour of debate on H. Res. 91.
# POSTPONED PROCEEDINGS - At the conclusion of debate on S.J.Res 13, the Chair put the question on passage of the bill and by voice vote, announced that the ayes had prevailed. Ms. Foxx demanded the yeas and nays and the Chair postponed further proceedings on passage of the bill until a time to be announced.
# Mr. Hoyer sent the privileged resolution H. Res. 8 to the desk and moved for its consideration. (CR H13)
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[8]]['Action'].unique()
# DEBATE

###   9_H35000   ###
print(list_codes[9])
len(df[df['actionCode'] == list_codes[9]])  #93
actionCode_with_name[list_codes[9]].unique()
# The previous question was ordered pursuant to the rule on the resolution and the preamble.',
# On ordering the previous question Agreed to by the Yeas and Nays: 212 - 200 (Roll no. 78).
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[9]]['Action'].unique()
# The previous question was ordered pursuant to the rule

###   10_B00100   ###
print(list_codes[10])
len(df[df['actionCode'] == list_codes[10]])  #294
actionCode_with_name[list_codes[10]].unique()
# Sponsor introductory remarks on measure. (CR E98)
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[10]]['Action'].unique()
# Sponsor introductory remarks on measure

###   11_5500   ###
print(list_codes[11])
len(df[df['actionCode'] == list_codes[11]])  #20
actionCode_with_name[list_codes[11]].unique()
# Committee on the Budget discharged.
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[11]]['Action'].unique()
# House committee discharged

###   12_H12300   ###
print(list_codes[12])
len(df[df['actionCode'] == list_codes[12]])  #20
actionCode_with_name[list_codes[12]].unique()
# Committee on the Budget discharged.
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[12]]['Action'].unique()
# Committee discharged

###   13_H37300   ###
print(list_codes[13])
len(df[df['actionCode'] == list_codes[13]])  #292
actionCode_with_name[list_codes[13]].unique()
# Pursuant to section 11 of H. Res. 486, and the motion offered by Mr. McGovern, the following bills passed under suspension of the rules: H.R. 482; H.R. 704; H.R. 961, as amended; H.R. 1314; H.R. 2571, as amended; H.R. 2679, as amended; H.R. 2694; H.R. 2922, as amended; H.R. 3182; H.R. 3239; H.R. 3241, as amended; H.R. 3723; H.R. 3752; H.R. 3841; S. 409; and S. 1340. (consideration: CR H3026-3052; text: CR H3051)',
# On motion to suspend the rules and pass the bill Agreed to by the Yeas and Nays: (2/3 required): 424 - 3 (Roll no. 337). (text: CR H5944)',
# ...
actionCode_dict[actionCode_dict['Code'] == list_codes[13]]['Action'].unique()
# Final Passage Under Suspension of the Rules Results

###   14_10000   ###
print(list_codes[14])
len(df[df['actionCode'] == list_codes[14]])  #3898
actionCode_with_name[list_codes[14]].unique()
# Introduced in Senate
actionCode_dict[actionCode_dict['Code'] == list_codes[14]]['Action'].unique()
# Introduced in Senate

###   15_H14000   ###
print(list_codes[15])
len(df[df['actionCode'] == list_codes[15]])  #92
actionCode_with_name[list_codes[15]].unique()
# Received in the House.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[15]]['Action'].unique()
# Received in the House

###   16_14500   ###
print(list_codes[16])
len(df[df['actionCode'] == list_codes[16]])  #106
actionCode_with_name[list_codes[16]].unique()
# Senate Committee on the Judiciary discharged by Unanimous Consent.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[16]]['Action'].unique()
# Senate committee discharged

###   17_H15000   ###
print(list_codes[17])
len(df[df['actionCode'] == list_codes[17]])  #89
actionCode_with_name[list_codes[17]].unique()
# Held at the desk.
actionCode_dict[actionCode_dict['Code'] == list_codes[17]]['Action'].unique()
# Held at the desk

###   18_28000   ###
print(list_codes[18])
len(df[df['actionCode'] == list_codes[18]])  #70
actionCode_with_name[list_codes[18]].unique()
# Presented to President.
actionCode_dict[actionCode_dict['Code'] == list_codes[18]]['Action'].unique()
# Presented to President

###   19_E20000   ###
print(list_codes[19])
len(df[df['actionCode'] == list_codes[19]])  #70
actionCode_with_name[list_codes[19]].unique()
# Presented to President.
actionCode_dict[actionCode_dict['Code'] == list_codes[19]]['Action'].unique()
# Presented to President

###   20_36000   ###
print(list_codes[20])
len(df[df['actionCode'] == list_codes[20]])  #68
actionCode_with_name[list_codes[20]].unique()
# Became Public Law No: 117-19.', 'Became Public Law No: 117-22.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[20]]['Action'].unique()
# Became Public Law

###   21_E30000   ###
print(list_codes[21])
len(df[df['actionCode'] == list_codes[21]])  #68
actionCode_with_name[list_codes[21]].unique()
# Signed by President.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[21]]['Action'].unique()
# Signed by President

###   22_E40000   ###
print(list_codes[22])
len(df[df['actionCode'] == list_codes[22]])  #68
actionCode_with_name[list_codes[22]].unique()
# Became Public Law No: 117-23.', 'Became Public Law No: 117-24.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[22]]['Action'].unique()
# Became Public Law No: 114-47

###   23_5000   ###
print(list_codes[23])
len(df[df['actionCode'] == list_codes[23]])  #172
actionCode_with_name[list_codes[23]].unique()
# The House Committee on Rules reported an original measure, H. Rept. 117-3, by Mr. Morelle.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[23]]['Action'].unique()
# Reported to House

###   24_H12200   ###
print(list_codes[24])
len(df[df['actionCode'] == list_codes[24]])  #116
actionCode_with_name[list_codes[24]].unique()
# Reported by the Committee on Veterans' Affairs. H. Rept. 117-30.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[24]]['Action'].unique()
# Committee reported

###   25_H12410   ###
print(list_codes[25])
len(df[df['actionCode'] == list_codes[25]])  #120
actionCode_with_name[list_codes[25]].unique()
# Placed on the Union Calendar, Calendar No. 15.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[25]]['Action'].unique()
# Union Calendar assignment

###   26_9000   ###
print(list_codes[26])
len(df[df['actionCode'] == list_codes[26]])  #4
actionCode_with_name[list_codes[26]].unique()
# Failed of passage/not agreed to in House: On motion to suspend the rules and pass the bill, as amended Failed by the Yeas and Nays: (2/3 required): 248 - 177 (Roll no. 162).
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[26]]['Action'].unique()
# Failed of passage/not agreed to in House

###   27_H12100   ###
print(list_codes[27])
len(df[df['actionCode'] == list_codes[27]])  #51
actionCode_with_name[list_codes[27]].unique()
# The House Committee on Rules reported an original measure, H. Rept. 117-3, by Mr. Morelle.
# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[27]]['Action'].unique()
# Committee report of an original measure

###   28_14000   ###
print(list_codes[28])
len(df[df['actionCode'] == list_codes[28]])  #137
actionCode_with_name[list_codes[28]].unique()
# Special Committee on Aging. Original measure reported to Senate by Senator Casey. Without written report.',
# Committee on the Budget. Original measure reported to Senate by Senator Sanders. Without written report.',# nan
actionCode_dict[actionCode_dict['Code'] == list_codes[28]]['Action'].unique()
# Reported to Senate

###   29_H17000   ###
print(list_codes[29])
len(df[df['actionCode'] == list_codes[29]])  #8
actionCode_with_name[list_codes[29]].unique()
# Motion to Discharge Committee filed by Mr. Roy. Petition No: 117-3. (<a href="https://clerk.house.gov/DischargePetition/20210421?CongressNum=117">Discharge petition</a> text with signatures.)
actionCode_dict[actionCode_dict['Code'] == list_codes[29]]['Action'].unique()
# Motion to Discharge Committee

###   30_14900   ###
print(list_codes[30])
len(df[df['actionCode'] == list_codes[30]])  #3
actionCode_with_name[list_codes[30]].unique()
# By Senator Carper from Committee on Environment and Public Works filed written report. Report No. 117-41.
actionCode_dict[actionCode_dict['Code'] == list_codes[30]]['Action'].unique()
# Senate committee report filed after reporting



