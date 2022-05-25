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
    #for i in range(1, 60):
        timestamp = int(hdul[i].header.cards["TIMESTMP"].value)
        list.append([timestamp, hdul[i].data])  
    return list

def corresponding(color_time_list, fluo_time_list):
    color_times, fluo_times, all_times = [], [], []
    for i in range(len(color_time_list)):
        color_times.append(color_time_list[i][0])
    for i in range(len(fluo_time_list)):
        fluo_times.append(fluo_time_list[i][0])
    all_times.extend(color_times)
    all_times.extend(fluo_times)
    latest_color = min(color_times)
    latest_fluo = min(fluo_times)
    colors = sorted(color_times)
    fluos = sorted(fluo_times)
    corresponding_images = {}
    for t in all_times:
        latest_color = t if t in color_times else latest_color
        latest_fluo = t if t in fluo_times else latest_fluo
        corresponding_images[t] = [latest_color, latest_fluo]
    return all_times, corresponding_images

def prepare_color_data(image_time_list):
    list = []
    for i in range(len(image_time_list)):
        image = cv2.cvtColor(image_time_list[i][1].astype(np.uint8), cv2.COLOR_BAYER_BG2RGB)
        list.append([image_time_list[i][0], image])
    return list

def prepare_fluo_data(image_time_list, trans_matrix):
    list = []
    for i in range(len(image_time_list)):
        image = cv2.resize(image_time_list[i][1], (1392, 1024))
        image = cv2.flip(image, 1) #flips around y-axis
        image = cv2.warpPerspective(image, trans_matrix, (1392, 1024))
        #image = cv2.convertScaleAbs(image, alpha=(255.0/65535.0)) # -> converts to uint8
        #image = cv2.threshold(image, 10, 25, cv2.THRESH_BINARY)[1]
        #image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        #image = cv2.bitwise_not(image+255)
        image= cv2.threshold(image, 2000, 2500, cv2.THRESH_BINARY)[1]
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB).astype(np.uint8)
        list.append([image_time_list[i][0], image])
    return list

def display_images(color_image, fluo_image):
    fig, ax = plt.subplots(1, 2)
    ax[0].imshow(color_image)
    ax[0].title.set_text('Color')
    ax[1].imshow(fluo_image)
    ax[1].title.set_text('Fluo')
    plt.show()

def display_image(image):
    plt.imshow(image)
    plt.show()

def generate_video(overlapped_list):
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    video = cv2.VideoWriter('video.mp4',fourcc, 20, (1392,1024))
    for i in overlapped_list:
        video.write(i)  
    video.release()

def overlap(color_list, fluo_list):
    overlapped = []
    for i in range(500):
        mixed_img = cv2.addWeighted(color_list[i][1], 1.0, fluo_list[i][1], 0.3, 0)
        overlapped.append(mixed_img)
    return overlapped







