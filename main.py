from openHDF import ExtractDataFrom_hdf
from PoseDataFromJsonFile import XYZ_Of_Joints_saveIn_npy
from Prepare_npy_file_to_Blender import FilterPoseData
import os

data_name = "E_vonHinten_ohneSchulterstütze"  # video name

openPose_Path = 'python run_webcam.py'  # openPose project path

json_path = os.path.join("JsonFiles", data_name, "*.json")  # from openPose jason folder path

#  Extract data from hdf to extractedData folder
ExtractDataFrom_hdf(data_name)

# run openPose from the console
command_line = openPose_Path + ' --model=mobilenet_thin --resize=432x368 --camera=' + data_name
print(command_line)
# os.system("sudo python scale1.py")

# get the json files
# XYZ_Of_Joints_saveIn_npy(hdf_folder_name, json_path, npy_dir)

# filter the data and Prepare for Blender
# FilterPoseData(data_name)
