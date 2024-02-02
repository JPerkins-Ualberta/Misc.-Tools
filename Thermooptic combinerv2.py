import pandas as pd 
import glob
import csv
import os
from os import listdir
from os.path import isfile, join
import xlsxwriter
path = "C:\\Users\\joshr\\OneDrive - ualberta.ca\\Desktop\\Research\\Projects\\Nanoholes\\Measurements\\2024\\WOX-MM-FIBER-REDO\\gas cont\\o2"
os.chdir(path)
files = glob.glob(path + "/*.csv")
data_frame = pd.DataFrame()
content = []
sheetname = "Collected results"
for filename in files: 
    name = os.path.splitext(os.path.basename(filename))[0]
    if not any(map(name.__contains__, ["nir-darref" , "nir-lightref" , "visible-darkref" , "raw" ,"visible-lightref", "settings"])) :
    # reading content of csv file 
    # content.append(filename) 
        names=["nm",name]
        df = pd.read_csv(filename, header=None, index_col=None) 
        df = df.transpose()
        print(names)
        df.columns = names
        df1 = df[names[1]]
        df1.columns = names[1]
        if data_frame.empty:
         data_frame =df
        else:
           data_frame[names[1]] =df1
     
data_frame.set_index("nm", inplace=True)
difference = data_frame.loc[931.753] -data_frame.loc[932.743]

#if adjusting nir use
df = data_frame[data_frame.index >= 932.743]+ difference
#if adjust visible use
df = data_frame[data_frame.index < 932.743] - difference
data_frame[data_frame.index < 932.743] = df
# converting content to data frame 


#reshake the order to fit thermooptic names
data_frame = data_frame.reindex(sorted(data_frame.columns),axis=1)

(max_row, max_col) = data_frame.shape



new_excel = pd.ExcelWriter('CollectedResults.xlsx', engine='xlsxwriter')
data_frame.to_excel(new_excel,index=True, sheet_name=sheetname)


workbook = new_excel.book
worksheet = new_excel.sheets[sheetname]
chart = workbook.add_chart({'type': 'scatter', 'subtype':'smooth'})
x = range(max_col)
color_swatch = ['black','blue','green','yellow','orange','purple','red']
for count, n in enumerate(x):
    chart.add_series({'categories':[sheetname,1,0,max_row,0],'values':[sheetname,1,(1+n),max_row,(1+n)], 'name':[sheetname, 0,(1+n)]} )#add liens cycling through color: ,'color':color_swatch[count]


chart.set_x_axis({'name':'Wavelength, nm', 'major_gridlines':{'visible':False},'name_font': {'size': 14, 'bold': True},
    'num_font':  {'size':14,'bold': True },'min': 450, 'max': 1700})
chart.set_y_axis({'name':'Reflection, %', 'major_gridlines':{'visible':False},'name_font': {'size': 14, 'bold': True},
    'num_font':  {'size':14,'bold': True },'min': 0, 'max': 100})
chart.set_legend({'none': True})
chart.set_title({'none': True})
worksheet.insert_chart(1,3,chart)


new_excel.save()
head =data_frame.columns # get columns before editings
data_frame = data_frame / 100 # into 0-1.0
data_frame['new_last'] = data_frame.index

#now export as VASE compatible DAT file
data_frame['ang'] = 20.000000
data_frame['error'] = 0.0010000
data_frame['pol'] = 'uR'
line2 = "RTmethod[PolRT=45.00, RevsRT=10.0, SlitRT=1700, AutoSlitMin=100, Interleave=Off, WVASE=3.942, HardVer=6.291, Fri Dec  8 16:36:33 2023]"
line3 = "Original[C:\\Users\\nf-user\\Documents\\jperkins\\test rt-si.dat]"
os.mkdir("Vase Ready")
for x in head:
#   df = pd.DataFrame()
 #  df = data_frame[['pol','ang',x,'error']].copy
   VaseFile = x + '.dat'
   header = [x,line2,line3, 'nm']
   with open("Vase Ready\\"+VaseFile, 'w+') as ict:
    # Write the header lines, including the index variable for
    # the last one if you're letting Pandas produce that for you.
    # (see above).
    for line in header:
        ict.write(line+'\n')

    # Just write the data frame to the file object instead of
    # to a filename. Pandas will do the right thing and realize
    # it's already been opened.
   data_frame.to_csv("Vase Ready\\"+VaseFile, mode='a', encoding='utf-8',float_format='%.6f', index=False, header=False, sep ='\t', columns = ['pol','new_last','ang',x,'error'])

   
  
   
