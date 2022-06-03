#!/usr/bin/python3

import pydicom as dicom
import matplotlib.pylab as plt

from mpl_toolkits.mplot3d import axes3d

import cv2
import sys
import glob
import numpy as np
import typing


def get_dicom_list(path_of_folder: str) -> typing.List[typing.List[typing.Dict[dicom.FileDataset, typing.Any]]]:

    try:
        print("Getting all DICOM file paths...")
        list_of_files: typing.List[str] = glob.glob(path_of_folder + '/*.dcm')
        return read_and_safe_list_of_dicom_paths(list_of_files)
    except FileNotFoundError:
        sys.exit('Error while trying to read dicom file!')


def read_and_safe_list_of_dicom_paths(list_of_file_paths: typing.List[str]) -> typing.List[typing.List[typing.Dict[dicom.FileDataset, typing.Any]]]:
    dict_of_images = {}  # dict[any, list[Union[None, fileDataset, DicomDir]]]
    for file in list_of_file_paths:
        try:
            ds: dicom.FileDataset = dicom.dcmread(str(file))
        except:
            sys.exit('Error while trying to read a DICOM image!')

        dict_of_images[ds.AcquisitionNumber] = ([cv2.rotate(ds.pixel_array, cv2.ROTATE_180), ds.PixelSpacing, ds])
    ret = []

    for i in range(len(dict_of_images)):
        ret.append(dict_of_images[i])
    return ret


def get_images(dicom_list: typing.List[typing.List[typing.Dict[dicom.FileDataset, typing.Any]]]) -> typing.List[np.ndarray]:
    ret = []
    for dicom in dicom_list:
        ret.append(dicom[0])
    return ret


def print_header(image: dicom.FileDataset):
    print(image)


def display_slice(image: np.ndarray):
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
