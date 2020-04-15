# -*- coding: utf-8 -*-
"""
Created on Thu Oct 13 09:54:30 2016

@author: dietz
"""

# %%   Set File Structure
import os
import sys

sys.path.insert(0, '..')
# from Preprocessing import preprocess_data as pre
# from Hand_Tracker import segment_color
current_dir = os.path.dirname(__file__)
# data_dir = os.path.join(current_dir,"../../../Data_Files/prepared_data")
# weights_dir = os.path.join(current_dir,'Weights')
# visualisation_dir = os.path.join(current_dir,"Visualisation")


import numpy as np
import cv2
from copy import copy

import time
import tables
import glob
from natsort import natsorted


# %% Settings
CONSTANT_FPS = True
if CONSTANT_FPS: FPS = 60
SHOW_FPS = False
MANUAL = False
PLAY_IN_LOOP = True
DISPLAY_SEGMENTATION = False
DISPLAY_KINECTSTREAMS = True
DISPLAY_COLOR_SEGMENTATION = False
SAVE_COLOR_SEGMENTATION = False

PERSON = "Armin"
ID = 1

record_path = os.path.join('/home/ali/Dokumente/Recordings/Armin',
                           (str(ID) + "_" + PERSON))

if os.path.isdir(record_path):
    pass
else:
    print("\nRecord folder does not exist\n")
    sys.exit(0)

filepaths = None
filepaths = natsorted(glob.glob(os.path.join(record_path, "*.hdf")))

wait_time = 0

if SAVE_COLOR_SEGMENTATION:
    color_seg_path = os.path.join(record_path, "color_segmentation")
    try:
        os.makedirs(color_seg_path, exist_ok=True)
    except Exception as e:
        print(e)
        sys.exit(0)

    PLAY_IN_LOOP = False
    CONSTANT_FPS = True
    if CONSTANT_FPS: FPS = 20
    DISPLAY_SEGMENTATION = False
    DISPLAY_KINECTSTREAMS = False

    X_depth = []
    X_ir = []
    X_registered = []
    y_hands = []
    frame_counter = []

if DISPLAY_KINECTSTREAMS:
    cv2.namedWindow("depth", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("depth", 512, 424)
    cv2.moveWindow("depth", 0, 0)
    cv2.namedWindow("ir", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("ir", 512, 424)
    cv2.moveWindow("ir", 0, 476)
    # cv2.namedWindow("registered", cv2.WINDOW_NORMAL)
    # cv2.resizeWindow("registered", 512,424)
    # cv2.moveWindow("registered", 576, 0)
    cv2.namedWindow("color", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("color", 640, 360)
    cv2.moveWindow("color", 576, 476)


def run(wait_time, PLAY_IN_LOOP, frame_number=0):
    # filepaths = filepaths[10:11]
    for filepath in filepaths:
        t0 = time.time()

        h5file = tables.open_file(filepath, "r")

        # print(h5file) to display structure of table
        depth = h5file.root.SensorData.depth.read()
        ir = h5file.root.SensorData.ir.read()
        registered = h5file.root.SensorData.registered.read()
        color = h5file.root.SensorData.color.read()

        metadata = h5file.root.LabelData.MetaData

        person = metadata.col('person')[0].decode('UTF-8')
        idnumber = metadata.col('idnumber')[0]
        timestamp = metadata.col('idnumber')[0]
        depth_sequence = metadata.col('depth_sequence')[0]
        color_sequence = metadata.col('color_sequence')[0]
        g_label = metadata.col('g_label')[0]
        g_pred = metadata.col('g_pred')[0]
        g_est = metadata.col('g_est')[0]
        g_shown = metadata.col('g_shown')[0]

        h5file.close()


        # %%
        if DISPLAY_KINECTSTREAMS:
            cv2.imshow("depth", depth / 2500.)
            cv2.imshow("ir", ir / 65535.)
            # cv2.imshow("registered", registered)
            # cv2.imshow("color", color)

            # color frame is very slow to display
            cv2.imshow("color", cv2.resize(color, (np.int(1920 / 3),
                                                   np.int(1080 / 3))))
        print(frame_number)
        frame_number += 1

        # %% calculate Frames Per Second (FPS) and offer exit conditions:
        # keystroke 'b' pause / continue
        # keystroke 'q' quit
        # keystroke 'n' next frame (if MANUAL == TRUE)
        # keystroke 'c' back to contiuous playback (if MANUAL == TRUE)

        if MANUAL:
            print("Sequence %i %i" % (depth_sequence, color_sequence))
            key = cv2.waitKey(wait_time) & 0xFF
            if key == ord('n'):
                wait_time = 0
                continue
            elif key == ord('c'):
                pass

        if CONSTANT_FPS:
            t1 = time.time() - t0
            wait_time = np.int((1 / FPS - t1) * 1000)
            if wait_time > 0:
                wait_time = wait_time
            else:
                wait_time = 1

            key = cv2.waitKey(wait_time) & 0xFF
            if key == ord('b'):
                key = cv2.waitKey(0) & 0xFF
                if key == ord('b'):
                    key = cv2.waitKey(wait_time) & 0xFF
            elif key == ord('q'):
                PLAY_IN_LOOP = False
                for i in range(10):
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)
                break

        else:
            key = cv2.waitKey(1) & 0xFF
            if key == ord('b'):
                key = cv2.waitKey(0) & 0xFF
                if key == ord('b'):
                    key = cv2.waitKey(1) & 0xFF
            elif key == ord('q'):
                PLAY_IN_LOOP = False
                for i in range(10):
                    cv2.destroyAllWindows()
                    cv2.waitKey(1)

        t2 = time.time() - t0
        if SHOW_FPS:
            print("fps: %i" % (1 / t2))

    if PLAY_IN_LOOP:
        print("NEW LOOP")
        run(wait_time, PLAY_IN_LOOP)

run(wait_time, PLAY_IN_LOOP)
