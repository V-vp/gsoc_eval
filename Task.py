'''
Author : Vivek Pawar
E-mail : pawarvivek2705@gmail.com
Link to resume : https://drive.google.com/open?id=1BORMlUsMTnPsUjTtD0p5-f-K7N7aAl2K

'''

###############  Time Zone Task  ################

import os
from datetime import datetime
import pytz

filename = os.listdir('h5_files')
timestamp = filename[0].split('_')
tz = pytz.timezone('CET') ## Central European Time
dt_utc = datetime.utcfromtimestamp(int(timestamp[0]) // 1000000000) ## Convert UNIX timestamp in UTC
utcdate = dt_utc.strftime('UTC Date-Time: %Y-%m-%d %H:%M:%S')  ## UTC in YY-MM-DD and HH-MM-SS
print(utcdate)
dt_cet = pytz.utc.localize(dt_utc).astimezone(tz) ## convert UTC to Central European Time (CET) 

cetdate = dt_cet.strftime('CET Date-Time: %Y-%m-%d %H:%M:%S')  ## CET in YY-MM-DD and HH-MM-SS
print(cetdate)

'''  
Output:
UTC Date-Time: 2018-11-11 18:48:28
CET Date-Time: 2018-11-11 19:48:28
'''




###############  Creating CSV file ################

import h5py
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import csv


datalist = []
data=['Data','Type','data_type','data_shape','data_size'] 
datalist.append(data)
def print_attrs(name):
    f_name = f.get(name) ## full path
    if isinstance(f_name, h5py.Dataset):
        datashape = f_name.shape ## dataset shape
        datasize = f_name.size ## dataset size
        try:   
            
            datatype = f_name.dtype ## dataset type
            data=[name,'Dataset',datatype,datashape,datasize] 
            datalist.append(data)
        except:
            '''
            TypeError: No NumPy equivalent for TypeBitfieldID exists
            while reading dtype of dataset so left with 'TypeError'
            '''
            data=[name,'Dataset','TypeError',datashape,datasize] 
            datalist.append(data)
    else:
        data=[name,'Group','','',''] 
        datalist.append(data)
        

f = h5py.File('h5_files/'+filename[0],'r')
f.visit(print_attrs)
csvfile = open('output.csv', 'w')
csvwriter = csv.writer(csvfile)
for item in datalist:        ## add row to csv file from datalist  
    csvwriter.writerow(item)
csvfile.close()






###############  Image File Task ################

img = f.get('AwakeEventData/XMPP-STREAK/StreakImage/streakImageData')
img = np.array(img) ## store image vector as numpy array
height = f.get('AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight') ## get height
width = f.get('AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth') ## get width

height = np.array(height)
width = np.array(width)
img = img.reshape((height[0],width[0])) ## reshape image 

img = scipy.signal.medfilt(img)
plt.imshow(img) ## show image 
plt.savefig('output.png') ## save image
