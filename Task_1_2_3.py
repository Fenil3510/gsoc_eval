import h5py
import re
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.signal
from datetime import datetime
import pytz
import os
import sys

def print_time_for_timezone(timezone, time_sec):
    datetimeob_utc = datetime.utcfromtimestamp(time_sec)
    print("TIME-UTC",datetimeob_utc)

    timezone_cern = pytz.timezone(timezone)
    datetimeob_cern = pytz.utc.localize(datetimeob_utc, is_dst=None).astimezone(timezone_cern)
    print("TIME",timezone, datetimeob_cern)

def check_function(name, node):
    if isinstance(node, h5py.Dataset):
        try:
            temp = [str(node.name), 'Dataset', node.shape, node.size, str(node.dtype)]
            info_list.append(temp)
        except TypeError:
             temp = [str(node.name),'Dataset', node.shape, node.size, "Error"]
             info_list.append(temp)
    else:
        temp = [str(node.name),'Group', np.nan, np.nan, np.nan]
        info_list.append(temp)

def make_dataframe_from_hdf5(file_main):
    file_main.visititems(check_function)
    info_dataframe_copy = info_dataframe.append(info_list)
    info_dataframe_copy.rename(columns = {0: 'Name',1: 'Type',2: 'Shape' ,3: 'Size', 4:'DataType'}, inplace = True)
    print("DataFrame Created Successfully and saved as Task2.csv")
    info_dataframe_copy.to_csv('Task2.csv', index = False)

def reshape_process_and_save(imagedata_dataset, imageheight_dataset, imagewidth_dataset,file_main):
    image_1d = np.array(file_main.get(imagedata_dataset))
    height = list(file_main.get(imageheight_dataset))[0]
    width = list(file_main.get(imagewidth_dataset))[0]
    image_final = np.reshape(image_1d, (height,width))
    image_final_processed = scipy.signal.medfilt(image_final)
    print("Image Created Successfully and saved as Task3.png")
    plt.imsave('Task3.png', image_final_processed)

def main():
    global info_list, info_dataframe
    files = os.listdir()
    try:
        fname = [x for x in files if '.h5' in x][0]
    except:
        print("No hdf5 file found, Terminating")
        sys.exit()
    time_nano = fname.split('_')[0]
    time_sec = float(time_nano)/(10**9)
    file_main = h5py.File(fname, 'r')
    info_dataframe = pd.DataFrame()
    info_list = []
    path_to_data = '/AwakeEventData/XMPP-STREAK/StreakImage/streakImageData'
    path_to_width = '/AwakeEventData/XMPP-STREAK/StreakImage/streakImageWidth'
    path_to_height = '/AwakeEventData/XMPP-STREAK/StreakImage/streakImageHeight'
    time_zone = "Europe/Zurich"
    print_time_for_timezone(time_zone,time_sec) #Task1
    make_dataframe_from_hdf5(file_main) #Task2
    reshape_process_and_save(path_to_data,path_to_height,path_to_width,file_main) #Task3
    file_main.close()

if __name__ == '__main__':
    main()




