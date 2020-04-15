import json
import numpy as np
import os
import glob
import matplotlib.pyplot as plt

# define folder path
video_name = "E_vonHinten_ohneSchulterstütze_registered/"
json_path = "JsonFiles/" + video_name + "*.json"

# open and sort the data in the path by the datum
json_files = list(filter(os.path.isfile, glob.glob(json_path)))
json_files.sort(key=lambda x: os.path.getmtime(x))

# define blender video parameters
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
