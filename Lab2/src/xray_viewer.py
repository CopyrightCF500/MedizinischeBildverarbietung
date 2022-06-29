#!/usr/bin/python3

import SimpleITK as sitk
import itkwidgets
import xray_util
import typing
import pydicom
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d


class XRayViewer:

    def __init__(self, folder_path: str):
        self.slices: typing.List[pydicom.FileDataset] = []
        self.images: typing.List[np.ndarray] = []

        self.read_dicom_data(folder_path)

    def read_dicom_data(self, folder_path: str):
        self.slices = xray_util.get_dicom_list(folder_path)
        self.images = xray_util.get_images(self.slices)

    def run(self):
        xray_util.print_header(self.slices[0])
        print(self.images[0])
        self.display_slice(0)
        self.display_slice(150)
        # self.display_wireframe()

    def display_slice(self, img_idx: int):
        plt.imshow(self.slices[img_idx].pixel_array, cmap=plt.cm.bone)
        plt.show()
        pass

    def display_multiple_slices(self):
        masked_lung = []

        for img in imgs_after_resamp:
            masked_lung.append(make_lungmask(img))

        self.sample_stack(masked_lung, show_every=10)

    def sample_stack(self, stack, rows=6, cols=6, start_with=0, show_every=10):
        fig, ax = plt.subplots(rows, cols, figsize=[12, 12])
        for i in range(rows * cols):
            ind = start_with + i * show_every
            ax[int(i / rows), int(i % rows)].set_title('slice %d' % ind)
            ax[int(i / rows), int(i % rows)].imshow(stack[ind], cmap='gray')
            ax[int(i / rows), int(i % rows)].axis('off')
        plt.show()

    def display_wireframe(self):
        names = sitk.ImageSeriesReader.GetGDCMSeriesFileNames('../data/')
        reader = sitk.ImageSeriesReader()
        reader.SetFileNames(names)
        img = reader.Execute()

        itkwidgets.view(img)

    def display_interactive_wireframe(self):
        fig = plt.figure()
        ax = fig.add_subplot(projection='3d')

        ax.scatter(1, 1, 1, marker="o", c="red", s=50)

        ax.set_xlabel('X Label')
        ax.set_ylabel('Y Label')
        ax.set_zlabel('Z Label')

        plt.show()

    def remove_cage(self):
        pass
