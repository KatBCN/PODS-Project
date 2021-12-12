import xml.etree.ElementTree as ET
import pandas as pd
import os
import zipfile


def get_actions(root):
    billactions = {}
    counter = 0
    for action in root.findall("./bill/actions/item"):
        print("-----", counter, "-----")
        billactions[counter] = {}
        billactions[counter]["billNumber"] = root.find("./bill/billNumber").text if root.find("./bill/billNumber") is not None else None
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


df = pd.DataFrame()
os.chdir('/home/irene/PycharmProjects/PODS_Bills')
files = os.listdir('data')
for file_zip in files:
    if file_zip.endswith('.zip'):
        unzipped_file = zipfile.ZipFile(os.getcwd() + '/data/' + file_zip, "r")
        for file_xml in zipfile.ZipFile.namelist(unzipped_file):
            if file_xml.endswith('.xml'):
                root = ET.fromstring(unzipped_file.read(file_xml))
                billactions = get_actions(root)
                billactions = pd.DataFrame.from_dict(billactions, orient='index')
                df = df.append(billactions)
df.to_csv('data/117Congress_BillActions.csv', index=False)