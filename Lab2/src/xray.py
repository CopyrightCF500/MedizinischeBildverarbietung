#!/usr/bin/python3

import pydicom as dicom
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import axes3d
import numpy as np
import glob
import cv2
import sys

        

def ASReadDICOM2(list_of_paths):
    dict = {}
    for file_name in list_of_paths:
        try:
            ds = dicom.dcmread(str(file_name))
        except:
            sys.exit('Error while trying to read dicom image!')

        dict[ds.AcquisitionNumber] = ([cv2.rotate(ds.pixel_array, cv2.ROTATE_180), ds.PixelSpacing, ds])
    ret = []
    for i in range(len(dict)):
        ret.append(dict[i])
    return ret

def display_slice(image):
    plt.imshow(image, cmap='gray')
    plt.show()

def display_wireframe(dataset):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    X, Y, Z = [], [], []
    for i in range(len(dataset)):
        X.append(dataset[i][1][0])
        Y.append(dataset[i][1][1])
        Z.append(i)
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array([Z])
    X, Y= np.meshgrid(X, Y)
    ax.plot_wireframe(X, Y, Z)
    plt.show()
    

#-------------------------------------------------------------------------------------------------
# main

if __name__ == '__main__':

    # specify path
    try:
        print("READING DICOM FILE...")
        list_of_files = glob.glob('../data/*.dcm')
    except FileNotFoundError:
        sys.exit('Error while trying to read dicom file!')

    data = ASReadDICOM2(list_of_files)

    display_slice(data[150][0])

    #display_wireframe(data)

    #print(data[0][1][0])
