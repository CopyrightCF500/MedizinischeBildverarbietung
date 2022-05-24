#!/usr/bin/python3

"""
This module contains custom fits functions
"""

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
        timestamp = int(hdul[i].header.cards["TIMESTMP"].value)
        list.append([timestamp, hdul[i].data])  
    return list


def prepare_color_data(image_time_list):
    list = []
    for i in range(len(image_time_list)):
        image = cv2.cvtColor(image_time_list[i][1].astype(np.uint8), cv2.COLOR_BAYER_BG2RGB)
        list.append([image_time_list[i][0], image])
    return list

def prepare_fluo_data(image_time_list):
    list = []
    for i in range(len(image_time_list)):
        image = cv2.resize(image_time_list[i][1], (1392, 1024))
        list.append([image_time_list[i][0], image])
    return list

def display_image(image):
    #plt.subplot()
    plt.imshow(image)
    plt.show()



