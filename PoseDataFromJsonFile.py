import h5py as h5
import json
import numpy as np
import os
import glob
import matplotlib.pyplot as plt


def XYZ_Of_Joints_saveIn_npy(hdf_path, json_path, npy_dir):
    path, dirs, files = next(os.walk(hdf_path))
    hdf_file_count = len(files)

    # open and sort the data in the path by the datum
    json_files = list(filter(os.path.isfile, glob.glob(json_path)))
    json_files.sort(key=lambda x: os.path.getmtime(x))

    frame_num = len(json_files)

    data_array = np.zeros((36, frame_num))  # there are 18 joints to be detected (x,y) => 18*2 = 36
    print(np.shape(data_array))
    j = 0
    for file in json_files:
        with open(file) as json_file:
            data = json.load(json_file)
            for x in data['people']:
                array = np.asarray(x['pose_keypoints_2d'])
                for i in range(0, 36):
                    data_array[i, j] = array[i]
        j += 1
    print(data)
    XYZ_joints = np.zeros((18 * 3, frame_num))  # 18 joints (x,y,z) => 18*3 points
    for i in range(0, hdf_file_count):
        file_name = os.path.join(hdf_path, "1_" + str(i) + ".hdf")
        try:  # some hdf files don#t open
            f = h5.File(file_name, "r")

            # MetaData = f['LabelData']['MetaData']
            # color = f['SensorData']['color']
            depth = f['SensorData']['depth']
            # ir = f['SensorData']['ir']
            # registered = f['SensorData']['registered']

            depth_array = np.asarray(depth)
            array = np.zeros(18 * 3)
            for j in range(0, 18):
                pixel_x = data_array[2 * j, i]
                pixel_y = data_array[2 * j + 1, i]
                world_Z = depth_array[int(pixel_x), int(pixel_y)]

                focalLength = 200
                world_X = world_Z * pixel_x / focalLength
                world_Y = world_Z * pixel_y / focalLength
                array[j * 3] = int(world_X)
                array[j * 3 + 1] = int(world_Y)
                array[j * 3 + 2] = int(world_Z)

            XYZ_joints[:, i] = array
        except:
            print("file cant be opened", file_name)

    #  save the Numpy array to npy file
    np.save(npy_dir, XYZ_joints)


if __name__ == '__main__':
    # define folder path
    video_name = "E_vonHinten_ohneSchulterstütze_registered"
    hdf_name = "E_vonHinten_ohneSchulterstütze"
    json_path = os.path.join("JsonFiles", video_name, "*.json")
    hdf_path = os.path.join("hdfFiles", hdf_name)
    npy_dir = os.path.join("npyFiles", hdf_name)
    XYZ_Of_Joints_saveIn_npy(hdf_path, json_path, npy_dir)
