import h5py as h5
import os
import numpy as np
import cv2


def Open_hdf_get_video(folder_name, saveToPath):
    path, dirs, files = next(os.walk(folder_name))
    file_count = len(files)

    depth_array = []
    ir_array = []
    registered_array = []

    blank_image = np.zeros((512, 424, 3), np.uint8)  # blank im ge if the frame don#t exists

    for i in range(1, file_count):
        file_name = folder_name + "/1_" + str(i) + ".hdf"
        print("open file" + "/1_" + str(i))
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
            except:  # if the image don't exists put a blankImage to have the wright number of frames
                print("jumped frame", i)
                registered_array.append(blank_image)
        except:
            print("file cant be opened", file_name)
            registered_array.append(blank_image)

    out_registered = cv2.VideoWriter(saveToPath, cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    for i in range(len(registered_array)):
        image = cv2.cvtColor(registered_array[i], cv2.COLOR_BGR2RGB)
        out_registered.write(image)

    out_registered.release()


if __name__ == "__main__":
    folder_name = "E_vonHinten_mitSchulterstütze"
    saveToPath = str("extractedVideos/" + folder_name + '_registered.avi')
    Open_hdf_get_video(folder_name, saveToPath)
