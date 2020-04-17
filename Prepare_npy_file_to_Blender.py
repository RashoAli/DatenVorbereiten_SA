import os
import numpy as np
import matplotlib.pyplot as plt


def FilterPoseData(data_name):
    npy_dir = os.path.join("extractedData", data_name, "ir.npy")
    data = np.load(npy_dir)
    plt.imshow(data[0,:,:])
    plt.show()


if __name__ == '__main__':
    data_name = "E_vonHinten_ohneSchulterstütze"
    FilterPoseData(data_name)
