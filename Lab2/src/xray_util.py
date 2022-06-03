#!/usr/bin/python3

import pydicom as dicom
import matplotlib.pylab as plt

from mpl_toolkits.mplot3d import axes3d

import cv2
import sys
import glob
import numpy as np


def GetDicomImagesList(pathOfFolder: str):

    try:
        print("Getting all DICOM file paths...")
        list_of_files: list[str] = glob.glob(pathOfFolder +'/*.dcm')
        return readAndSafeListOfDicomPaths(list_of_files)
    except FileNotFoundError:
        sys.exit('Error while trying to read dicom file!')

def readAndSafeListOfDicomPaths(list_of_paths):
    dict = {}  # dict[any, list[Union[None, fileDataset, DicomDir]]]
    for file_name in list_of_paths:
        try:
            ds = dicom.dcmread(str(file_name))
        except:
            sys.exit('Error while trying to read a DICOM image!')

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
        X.append(dataset[i][2].ImagePositionPatient[0])
        Y.append(dataset[i][2].ImagePositionPatient[1])
        Z.append(dataset[i][1])
    X = np.array(X)
    Y = np.array(Y)
    Z = np.array(Z)
    #X, Y, Z = np.meshgrid(X, Y, Z)
    ax.plot_wireframe(X, Y, Z)
    plt.show()
