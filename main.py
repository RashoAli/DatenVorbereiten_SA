from openHDF import Open_hdf_get_video
from PoseDataFromJsonFile import XYZ_Of_Joints_saveIn_npy
from Prepare_npy_file_to_Blender import FilterPoseData
import os

video_name = "E_vonHinten_ohneSchulterstütze_registered"

hdf_folder_name = "E_vonHinten_mitSchulterstütze"
videoSaveToPath = str("extractedVideos/" + video_name + '.avi')

json_path = os.path.join("JsonFiles", video_name, "*.json")
npy_dir = os.path.join("npyFiles", video_name)

npy_saveToPath = os.path.join("npyFilesFiltered", video_name)

#  open the hdf file from hdf_folder_name -> extract color video (video_name) to save saveToPath
Open_hdf_get_video(hdf_folder_name, videoSaveToPath)

# run openPose from the console
# os.system("sudo python scale1.py")

# get the json files
XYZ_Of_Joints_saveIn_npy(hdf_folder_name, json_path, npy_dir)

# filter the data and Prepare for Blender
FilterPoseData(npy_dir,npy_saveToPath)