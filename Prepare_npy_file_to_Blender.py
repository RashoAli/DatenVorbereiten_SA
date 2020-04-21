import os
import numpy as np
import matplotlib.pyplot as plt


def FilterPoseData(data_name):
    npy_dir = os.path.join("extractedData", data_name+".npy")
    data = np.load(npy_dir)
    data = np.asarray(data)
    print(data[:,0])
    plt.show()


if __name__ == '__main__':
    data_name = "E_von vorne ohne Schulterstütze"
    FilterPoseData(data_name)
