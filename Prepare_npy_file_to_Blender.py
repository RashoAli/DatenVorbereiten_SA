import os
import numpy as np


def FilterPoseData(npy_dir, saveToPath):
    data = np.load(str(npy_dir + ".npy"))
    np.save(saveToPath, data)


if __name__ == '__main__':
    npy_data = "E_vonHinten_ohneSchulterstütze"
    npy_dir = os.path.join("npyFiles", npy_data)
    saveToPath = os.path.join("npyFilesFiltered", npy_data)
    FilterPoseData(npy_dir, saveToPath)
