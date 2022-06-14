#!/usr/bin/python3

"""
This module contains custom fits functions
"""

from turtle import color
import numpy as np
import cv2
from astropy.io import fits
import matplotlib.pyplot as plt


# returns 3x3 transformation matrix
def trans_parameter(hdu_primary: fits.PrimaryHDU) -> np.ndarray:
    val0 = hdu_primary.header.cards['TRANSC0'].value
    val1 = hdu_primary.header.cards['TRANSC1'].value
    val2 = hdu_primary.header.cards['TRANSC2'].value
    val3 = hdu_primary.header.cards['TRANSC3'].value
    val4 = hdu_primary.header.cards['TRANSC4'].value
    val5 = hdu_primary.header.cards['TRANSC5'].value
    val6 = hdu_primary.header.cards['TRANSC6'].value
    val7 = hdu_primary.header.cards['TRANSC7'].value
    val8 = hdu_primary.header.cards['TRANSC8'].value

    return np.array([
            [val0, val1, val2],
            [val3, val4, val5],
            [val6, val7, val8]  ])


def image_timestamp_list(hdul: fits.HDUList):
    list = []
    for i in range(1, len(hdul)):
    #for i in range(1, 100):
        timestamp = int(hdul[i].header.cards["TIMESTMP"].value)
        list.append([timestamp, hdul[i].data])
    return list

def find_matching(color_time_list: 'list[list[int]]', fluo_time_list: 'list[list[int]]'):
    color_times, fluo_times = [], []
    for i in range(len(color_time_list)):
        color_times.append(color_time_list[i][0])
    for i in range(len(fluo_time_list)):
        fluo_times.append(fluo_time_list[i][0])
    
    N_iterations = min(len(color_times), len(fluo_times))

    matching_timestamps = []

    for i in range(N_iterations):
        matching_timestamps.append([i, 0])
        timestamp_color = color_times[i]
        min_diff = timestamp_color
        for j in range(N_iterations):
            if abs(timestamp_color - fluo_times[j]) < min_diff:
                min_diff = abs(timestamp_color - fluo_times[j])
                matching_timestamps[i][1] = j
    return matching_timestamps

def prepare_color_data(image_time_list: 'list[list[int]]'):
    list = []
    for i in range(len(image_time_list)):
        image = cv2.cvtColor(image_time_list[i][1].astype(np.uint8), cv2.COLOR_BAYER_BG2RGB)
        image = cv2.flip(image, 1) #flips around y-axis
        list.append([image_time_list[i][0], image])
    return list

def prepare_fluo_data(image_time_list: 'list[list[int]]', trans_matrix: np.ndarray):
    list = []
    for i in range(len(image_time_list)):
        image = cv2.resize(image_time_list[i][1], (1392, 1024))
        image = cv2.warpPerspective(image, trans_matrix, (1392, 1024))
        image = cv2.threshold(image, 2200, 2500, cv2.THRESH_BINARY)[1]
        image = cv2.erode(image, kernel = np.ones((5, 5), np.uint8), iterations=4)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.uint8)
        image = cv2.applyColorMap(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB).astype(np.uint8), cv2.COLORMAP_OCEAN)
        #image = cv2.convertScaleAbs(image, alpha=(255.0/65535.0)) # -> converts to uint8
        #image = cv2.threshold(image, 11, 15, cv2.THRESH_BINARY)[1]
        #image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        #image = cv2.bitwise_not(image+255)
        #image = cv2.erode(image, kernel = np.ones((5, 5), np.uint8), iterations=2)
        #image = cv2.dilate(image, kernel = np.ones((5, 5), np.uint8), iterations=2)
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        list.append([image_time_list[i][0], image])
    return list

def display_images(color_image: np.ndarray, fluo_image: np.ndarray):
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(color_image)
    ax[0].title.set_text('Color')
    ax[1].imshow(fluo_image)
    ax[1].title.set_text('Fluo')
    plt.show()

def display_image(color_image: np.ndarray):
    plt.imshow(color_image)
    plt.show()

def generate_video(overlapped_list: 'list[np.ndarray]', name, shape):
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter(name, fourcc, 20, shape)
    for i in overlapped_list:
        video.write(i)  
    video.release()

def overlap(color_list: 'list[list[int]]', fluo_list: 'list[list[int]]', all_times: 'list[list[int]]'):
    N_iterations = len(all_times)
    overlapped = []
    for i in range(800):
    #for i in range(N_iterations):
        image = cv2.addWeighted(cv2.cvtColor(color_list[all_times[i][0]][1], cv2.COLOR_BGR2RGB), 1, fluo_list[all_times[i][1]][1], 0.3, 0)
        overlapped.append(image)
    return overlapped


#------------------------------------------------------------------------------------------------------------------
# Aufgabe 4: hochaufgeloestes ueberlagertes Falschfarbenfilb

def capture_video(video_path):
    images = []
    video_file = cv2.VideoCapture(video_path)

    if (video_file.isOpened() == False):
        print("Error opening video stream or file")

    while (video_file.isOpened()):
        ret, frame = video_file.read()
        if ret == True:
            images.append(frame)
        else:
            break

    video_file.release()
    cv2.destroyAllWindows()
    return images

def prepare_fluo_data_2(image_list):
    list = []
    for i in range(len(image_list)):
        image = cv2.resize(image_list[i], (768, 576))
        image = cv2.flip(image, 1)
        image = cv2.threshold(image, 2200, 2500, cv2.THRESH_BINARY)[1]
        image = cv2.erode(image, kernel=np.ones((5, 5)), iterations=4)
        image = cv2.dilate(image, kernel=np.ones((5, 5)), iterations=4)
        image = cv2.applyColorMap(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB).astype(np.uint8), cv2.COLORMAP_OCEAN)
        list.append(image)
    return list

def compare_sizes(size_video, size_fluo, fluo_list):
    ret = []
    for i in range(size_video):
        n = int(i / (size_video/size_fluo))
        ret.append(fluo_list[n])
    return ret

def overlap_2(video_data, fluo_data):
    overlapped = []
    for i in range(1800):
    #for i in range(N_iterations):
        image = cv2.addWeighted(video_data[i], 1, fluo_data[i], 0.7, 0)
        overlapped.append(image)
    return overlapped

def find_contour(img, lower, upper):
    # create NumPy arrays from the boundaries
    lower = np.array(lower, dtype="uint8")
    upper = np.array(upper, dtype="uint8")

    # # find the colors within the specified boundaries and apply
    # # the mask
    mask = cv2.inRange(img, lower, upper)
    output = cv2.bitwise_and(img, img, mask=mask)

    ret, thresh = cv2.threshold(mask, 40, 255, 0)
    if (int(cv2.__version__[0]) > 3):
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    else:
        im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if len(contours) != 0:
        # draw in blue the contours that were founded
        cv2.drawContours(output, contours, -1, 255, 3)

        # find the biggest countour (c) by the area
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        # draw the biggest contour (c) in green
        cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 2)
        return x + 0.5 * w, y + 0.5 * h
    return 0, 0


def calculate_transform_matrix(source, destination):
    src_middle = find_contour(source, [190, 160, 70], [210, 190, 130])  # fluo
    dst_middle = find_contour(destination, [20, 50, 80], [70, 140, 230])  # video
    if src_middle == (0, 0) or dst_middle == (0, 0):
        return np.float32([[1, 0, 0], [0, 1, 0]])
    x = dst_middle[0] - src_middle[0]
    y = dst_middle[1] - src_middle[1]
    return np.float32([[1, 0, x], [0, 1, y]])
