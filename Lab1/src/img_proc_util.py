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
    #for i in range(1, 300):
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
        image = cv2.erode(image, kernel = np.ones((5, 5), np.uint8), iterations=12)
        image = cv2.applyColorMap(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB).astype(np.uint8), cv2.COLORMAP_OCEAN)
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
    i = 0
    while (video_file.isOpened):
        ret, frame_new = video_file.read()
        if ret == True:
            contours = []
            x = 0
            x_temp = 0
            y = 480
            y_temp = 0
            sum = 480+480
            sum_temp = 0
            cnt = 0
            frame_new = frame_new[27:560, 86:718]
            frame_new = cv2.resize(frame_new, (480, 480))
            frame_temp = frame_new.copy()
            for j in range(len(frame_temp)):
                if(j > 170):
                    frame_temp[j] = frame_temp[j]-frame_temp[j]
                if(i>140 and i<1400):
                    frame_temp[j][120:479] = frame_temp[j][120:479]-frame_temp[j][120:479]
            while(len(contours)==0):
                frame2 = cv2.threshold(frame_temp, 160, 190, cv2.THRESH_BINARY)[1]
                frame2 = cv2.erode(frame2, kernel=np.ones((5, 5)), iterations=4)
                frame2 = cv2.dilate(frame2, kernel=np.ones((5, 5)), iterations=4)
                frame3 = cv2.cvtColor(frame2, cv2.COLOR_RGB2GRAY)
                contours, hierarchy = cv2.findContours(frame3, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
                if (len(contours) > 0):
                    for n in range (len(contours)):
                        cnt = contours[0]
                        M = cv2.moments(cnt)
                        x_temp = int(M['m10'] / M['m00'])
                        y_temp = int(M['m01'] / M['m00'])
                        sum_temp = x_temp + y_temp
                        if(sum_temp < sum):
                            x = x_temp
                            y = y_temp
                            sum = sum_temp
                frame_temp = frame_temp + 25
            i = i + 1
            images.append([frame_new, (x, y)])
        else:
            break

    video_file.release()
    cv2.destroyAllWindows()
    return images

def prepare_fluo_data_2(image_list):
    ret = []
    for i in range(len(image_list)):
        #'''
        image = cv2.resize(image_list[i], (480, 480))
        image = cv2.threshold(image, 1600, 2500, cv2.THRESH_BINARY)[1]
        image = cv2.erode(image, kernel=np.ones((5, 5)), iterations=4)
        image = cv2.dilate(image, kernel=np.ones((5, 5)), iterations=4)
        image = cv2.applyColorMap(cv2.cvtColor(image, cv2.COLOR_GRAY2RGB).astype(np.uint8), cv2.COLORMAP_OCEAN)
        frame = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        contours, hierarchy = cv2.findContours(frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if(len(contours) > 0):
            cnt = contours[0]
            M = cv2.moments(cnt)
            x = int(M['m10'] / M['m00'])
            y = int(M['m01'] / M['m00'])
        else:
            x,y = 0,0
        if i > (len(image_list)/2 - 300):
            image = cv2.erode(image, kernel=np.ones((5, 5)), iterations=18)
        if (((i > 270) and (i < 440)) or ((i > 900) and (i < 1060))):
            image = image - image
        ret.append([image, (x, y)])
    return ret

def update_size(size_video, size_fluo, fluo_list):
    ret = []
    for i in range(size_video):
        n = int(i / (size_video/size_fluo))
        ret.append(fluo_list[n])
    return ret

def overlap_2(video_data, fluo_data):
    overlapped = []
    for i in range(0,3500):
        image = cv2.addWeighted(video_data[i][0], 1, fluo_data[i], 0.6, 0)
        overlapped.append(image)
    return overlapped

def apply_matrix(video_data_matrix, fluo_data_matrix):
    ret = []
    for i in range(len(fluo_data_matrix)):
        x = video_data_matrix[i][1][0] - fluo_data_matrix[i][1][0]
        y = video_data_matrix[i][1][1] - fluo_data_matrix[i][1][1]
        M = np.float32([[1, 0, x], [0, 1, y]])
        image = cv2.warpAffine(fluo_data_matrix[i][0], M, (480, 480))
        ret.append(image)
    return ret
