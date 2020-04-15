import h5py as h5
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import cv2

folder_name = "E_vonHinten_ohneSchulterstütze"
path, dirs, files = next(os.walk(folder_name))
file_count = len(files)

depth_array = []
ir_array = []
registered_array = []

for i in range(0, file_count):
    file_name = folder_name + "/1_" + str(i) + ".hdf"
    print(file_name)
    # %% open the hdf file and its sup_parts
    try:  # some hdf files don#t open
        f = h5.File(file_name, "r")

        # %% initial the sup_parts
        try:  # depth and ir data have to be int and 0->255
            MetaData = f['LabelData']['MetaData']
            color = f['SensorData']['color']
            depth = f['SensorData']['depth']
            ir = f['SensorData']['ir']
            registered = f['SensorData']['registered']

            # get image size
            height, width, layers = registered.shape
            size = (width, height)

            # convert the data to array so later convert them cv2 format
            array_registered = np.asarray(registered)

            # convert data to cv2 format
            cv2_registered = cv2.cvtColor(array_registered, cv2.COLOR_BGR2RGB)

            # append data to te list
            registered_array.append(cv2_registered)

        except:
            print("jumped frame", i)

    except:
        print("file cant be opened", file_name)
out_registered = cv2.VideoWriter(str("extractedVideos/"+folder_name + '_registered.avi'), cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
for i in range(len(registered_array)):
    print(i)
    image = cv2.cvtColor(registered_array[i], cv2.COLOR_BGR2RGB)
    out_registered.write(image)

out_registered.release()

