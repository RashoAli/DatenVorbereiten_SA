import os
import numpy as np

npy_data = "E_vonHinten_ohneSchulterstütze"
npy_dir = os.path.join("npyFiles", npy_data)
print(npy_dir)
data = np.load(str(npy_dir + ".npy"))
print(data)
