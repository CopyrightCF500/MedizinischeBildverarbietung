#!/usr/bin/python3

import pydicom as dicom
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import axes3d
from vedo import *
import cv2
import sys
import glob
import numpy as np
import typing

from skimage import morphology
from skimage import measure
from skimage.transform import resize


def get_dicom_list(path_of_folder: str) -> typing.List[dicom.FileDataset]:

    try:
        print("Getting all DICOM file paths...")
        list_of_files: typing.List[str] = glob.glob(path_of_folder + '/*.dcm')
        return read_and_save_list_of_dicom_paths(list_of_files)
    except FileNotFoundError:
        sys.exit('Error while trying to read dicom file!')


def read_and_save_list_of_dicom_paths(list_of_file_paths: typing.List[str]) -> typing.List[dicom.FileDataset]:
    dict_of_ds: typing.Dict[typing.Union[str, int], dicom.FileDataset] = {}
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


def print_header(ds: dicom.FileDataset):
    print(ds)


def print_meta(ds: dicom.FileDataset):
    pass

def display_slice(image: np.ndarray):
    plt.imshow(image, cmap='gray')
    plt.show()

def display_slices(stack, rows=5, cols=5, start_with=10, show_every=3):
    fig, ax = plt.subplots(rows, cols, figsize=[12, 8])
    for i in range(rows * cols):
        ind = start_with + i * show_every
        ax[int(i / rows), int(i % rows)].set_title('slice %d' % ind)
        ax[int(i / rows), int(i % rows)].imshow(stack[ind][0], cmap='gray')
        ax[int(i / rows), int(i % rows)].axis('off')
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


def display_wireframe2(slices):
    # pixel aspects, assuming all slices are the same
    ps = slices[0][2].PixelSpacing
    ss = slices[0][2].SliceThickness
    ax_aspect = ps[1] / ps[0]
    sag_aspect = ps[1] / ss
    cor_aspect = ss / ps[0]

    # create 3D array
    img_shape = list(slices[0][2].pixel_array.shape)
    img_shape.append(len(slices))
    img3d = np.zeros(img_shape)

    # fill 3D array with the images from the files
    for i, s in enumerate(slices):
        img2d = s[2].pixel_array
        img3d[:, :, i] = img2d

    # plot 3 orthogonal slices
    a1 = plt.subplot(2, 2, 1)
    plt.imshow(img3d[:, :, img_shape[2] // 2])
    a1.set_aspect(ax_aspect)

    a2 = plt.subplot(2, 2, 2)
    plt.imshow(img3d[:, img_shape[1] // 2, :])
    a2.set_aspect(sag_aspect)

    a3 = plt.subplot(2, 2, 3)
    plt.imshow(img3d[img_shape[0] // 2, :, :].T)
    a3.set_aspect(cor_aspect)

    plt.show()


def plot_3d():
    volume = load('../data')  # returns a vedo-Volume object
    show(volume, bg='white', mode=10)

