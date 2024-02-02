import pandas as pd 
import glob
import os
from os import listdir
from os.path import isfile, join
import xlsxwriter
path = "C:\\Users\\joshr\\OneDrive - ualberta.ca\\Desktop\\Research\\Projects\\Heating Stage -Optical Setup\\Measurements\\2023\\thermooptic\\sbs-yellow-liam 2a - Copy\\New folder"
files = glob.glob(path + "/*.csv")
data_fram = pd.DataFrame()
content = []
sheetname = "Collected results"
for filename in files: 
    if not("darref" or "darkref" or "lightref") in filename:
    # reading content of csv file 
    # content.append(filename) 
        names=["nm",os.path.splitext(os.path.basename(filename))[0]]
        df = pd.read_csv(filename, header=None, index_col=None) 
        df = df.transpose()
        print(len(df))
        df.columns = names

        if not content:
            content.append(df)

        else:
            content.append(df.columns[1])
  
# converting content to data frame 
data_frame = pd.concat(content) 

print(data_frame) 
new_excel = pd.ExcelWriter('SampleFile.xlsx', enginer='xlsxwriter')

data_frame.to_excel(new_excel,index=False, sheet_name=sheetname)

workbook = new_excel.book
worksheet = new_excel.sheets[sheet_name]
chart = workbook.add_chart({'type': 'line'})


new_excel.save()