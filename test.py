import pandas as pd 
import glob
import csv
import os
from os import listdir
from os.path import isfile, join
import xlsxwriter
path = "C:\\Users\\joshr\\OneDrive - ualberta.ca\\Desktop\\Research\\Projects\\Heating Stage -Optical Setup\Measurements\\2023\\thermooptic\\Dynamic Crystalization\\Soln-Process SbS crystaliztion dynamic\\SPECTRA.csv"

data_frame = pd.DataFrame()

data_frame = pd.read_csv(path, header=None, index_col=None) 
Spectra =data_frame.iloc[1::2*60]
Spectra.reset_index(drop=True)
Spectra.to_csv('out.csv',sep='\t')
difference = Spectra.loc[2093] -Spectra.loc[2094]
df = Spectra[data_frame.index < 2094] - difference
Spectra[data_frame.index < 2094] = df
    
print(Spectra)

wave = data_frame.iloc[0] #nm



     

   
