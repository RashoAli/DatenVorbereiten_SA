import os
import numpy as np
import matplotlib.pyplot as plt
import math
import os
import cv2

folder_name = os.path.join('images', "E_vonVorne_ohneSchulterstuetze")
#path, dirs, files = next(os.walk(folder_name))
file_count = 140#len(files)

image_array = []

for i in range(1, file_count):
    # get image size
    file_name = folder_name + "/frame" + str(i) + ".jpg"
    print(file_name)

    img = cv2.imread(file_name)
    height, width, layers = img.shape
    size = (width, height)

    image_array.append(img)

out_registered = cv2.VideoWriter(str(folder_name + '_PoseEstimation.avi'), cv2.VideoWriter_fourcc(*'DIVX'),
                                 15, size)
print(str(folder_name + '_PoseEstimation.avi'))
for i in range(len(image_array)):
    print(i)
    out_registered.write(image_array[i])

out_registered.release()
