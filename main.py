from openHDF import Open_hdf_get_video
from PoseDataFromJsonFile import XYZ_Of_Joints_saveIn_npy
from Prepare_npy_file_to_Blender import FilterPoseData
import os

video_name = "E_vonVorne_ohneSchulterstuetze"  # video name

python_script_path = '/home/rasho/PycharmProjects/DatenVorbereiten_SA'
hdf_folder_name = "E_vonVorne_ohneSchulterstuetze"  # hdf folder path
hdf_path = os.path.join(python_script_path, hdf_folder_name)
videoSaveToPath = os.path.join(python_script_path, "extractedVideos", video_name + '.avi')  # video save to path
openPose_Path = '/home/rasho/Desktop/Pose_open/tf-pose-estimation/run_webcam.py'  # openPose project path

# json_path = os.path.join(python_script_path, "JsonFiles", video_name, "*.json")  # from openPose jason folder path
json_path = os.path.join("/home/rasho/Desktop/Pose_open/Data_folder/JSON_Data", video_name, "*.json")
npy_dir = os.path.join(python_script_path, "npyFiles", video_name)  # npy save to path

npy_saveToPath = os.path.join(python_script_path, "npyFilesFiltered", video_name)  # filtered npy save to path

#  open the hdf file from hdf_folder_name -> extract color video (video_name) to save saveToPath
print(" 1___________________________________1 ")
print(" open the hdf file from hdf_folder_name -> extract color video (video_name) to save saveToPath ")
# Open_hdf_get_video(hdf_path, videoSaveToPath)

# run openPose from the console
print(" 2___________________________________2 ")
print(" run openPose from the console ")
command_line = 'python ' + openPose_Path + ' --model=mobilenet_thin --resize=432x368 --camera=' + videoSaveToPath
print(command_line)
# os.system(command_line)

# get the json files
print(" 3___________________________________3 ")
print(" get the json files ")
XYZ_Of_Joints_saveIn_npy(hdf_path, json_path, npy_dir)

# filter the data and Prepare for Blender
print(" filter the data and Prepare for Blender ")
print(" 4___________________________________4 ")
FilterPoseData(npy_dir, npy_saveToPath)
