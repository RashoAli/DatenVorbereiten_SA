from openHDF import Open_hdf_get_video
from PoseDataFromJsonFile import XYZ_Of_Joints_saveIn_npy
from Prepare_npy_file_to_Blender import FilterPoseData
import os

video_name = "E_vonHinten_ohneSchulterstütze_registered"  # video name

hdf_folder_name = "E_vonHinten_mitSchulterstütze"  # hdf folder path
videoSaveToPath = os.path.join("extractedVideos/", video_name, '.avi')  # video save to path

openPose_Path = 'python run_webcam.py'  # openPose project path

json_path = os.path.join("JsonFiles", video_name, "*.json")  # from openPose jason folder path
npy_dir = os.path.join("npyFiles", video_name)  # npy save to path

npy_saveToPath = os.path.join("npyFilesFiltered", video_name)  # filtered npy save to path

#  open the hdf file from hdf_folder_name -> extract color video (video_name) to save saveToPath
Open_hdf_get_video(hdf_folder_name, videoSaveToPath)

# run openPose from the console
command_line = openPose_Path + ' --model=mobilenet_thin --resize=432x368 --camera=' + video_name
print(command_line)
# os.system("sudo python scale1.py")

# get the json files
XYZ_Of_Joints_saveIn_npy(hdf_folder_name, json_path, npy_dir)

# filter the data and Prepare for Blender
FilterPoseData(npy_dir, npy_saveToPath)
