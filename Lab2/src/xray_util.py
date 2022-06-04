#!/usr/bin/python3

import pydicom as dicom
import matplotlib.pylab as plt

from mpl_toolkits.mplot3d import axes3d

import cv2
import sys
import glob
import numpy as np
import typing


def get_dicom_list(path_of_folder: str) -> typing.List[dicom.FileDataset]:

    try:
        print("Getting all DICOM file paths...")
        list_of_files: typing.List[str] = glob.glob(path_of_folder + '/*.dcm')
        return read_and_save_list_of_dicom_paths(list_of_files)
    except FileNotFoundError:
        sys.exit('Error while trying to read dicom file!')


def read_and_save_list_of_dicom_paths(list_of_file_paths: typing.List[str]) -> typing.List[dicom.FileDataset]:
    dict_of_ds: typing.Dict[typing.Union[str, int], dicom.FileDataset] = {}  # typing.Union[dicom.FileDataset, typing.List]
    for file in list_of_file_paths:
        try:
            ds: dicom.FileDataset = dicom.dcmread(str(file))
        except:
            sys.exit('Error while trying to read a DICOM image!')

        #print(type(([cv2.rotate(ds.pixel_array, cv2.ROTATE_180), ds.PixelSpacing, ds])))
        dict_of_ds[ds.AcquisitionNumber] = ds #([cv2.rotate(ds.pixel_array, cv2.ROTATE_180), ds.PixelSpacing, ds])
    ret = []

    for i in range(len(dict_of_ds)):
        ret.append(dict_of_ds[i])
    return ret


def get_images(dicom_list: typing.List[dicom.FileDataset]) -> typing.List[np.ndarray]:
    ret: typing.List[np.ndarray] = []
    for ds in dicom_list:
        cv2.rotate(ds.pixel_array, cv2.ROTATE_180, ds.pixel_array)
        ret.append(ds.pixel_array)
    return ret


def print_header(image: dicom.FileDataset):
    print(image)


def display_slice(image: np.ndarray):
    plt.imshow(image, cmap='gray')
    plt.show()


def display_wireframe(dataset: typing.List[dicom.FileDataset]):
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    x_pos, y_pos, z_pos = [], [], []

    for i in range(len(dataset)):
        x_pos.append(dataset[i].pixel_array)
        y_pos.append(dataset[i].pixel_array)
        z_pos.append(dataset[i].PixelSpacing)

    print(x_pos[200])
    print(y_pos[200])
    print(z_pos[200])
    x_pos = np.array(x_pos)
    y_pos = np.array(y_pos)
    z_pos = np.array(z_pos)
    #X, Y, Z = np.meshgrid(X, Y, Z)
    ax.plot_wireframe(x_pos, y_pos, z_pos)
    plt.show()
