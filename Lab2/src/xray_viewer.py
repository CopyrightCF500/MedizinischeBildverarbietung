#!/usr/bin/python3

import SimpleITK as sitk
import itkwidgets
import xray_util
import typing
import pydicom
import numpy as np
import matplotlib
import scipy
import plotly

class XRayViewer:

    def __init__(self, folder_path: str):
        self.dicom_files_folder_path = folder_path
        # List of all DICOM images
        self.dicom_files_list: typing.List[pydicom.FileDataset] = []
        self.dicom_files_list = xray_util.get_dicom_list(folder_path)
        self.dicom_images: typing.List[np.ndarray] = xray_util.get_images(self.dicom_files_list)

    def run(self):

        #print(type(self.dicom_files_list[0]))
        #print(xray_util.display_slice(self.dicom_images[83]))
        self.display_slice()
        #xray_util.display_wireframe(self.dicom_files_list)
        #print(xray_util.print_header(self.dicom_files_list[150].)))
        # show one slice
        #xray_util.display_slice(self.dicom_images[150])

        # show multiple slices
        xray_util.display_slices(self.dicom_files_list)

        # display wireframe
        #xray_util.display_wireframe(self.dicom_files_list)

        # Oberfläche? (aufgabe 4)
        #xray_util.display_wireframe2(self.dicom_files_list)

        # print header
        #print(xray_util.print_header(self.dicom_files_list[150][2]))

        # coole 3D Darstellung
        xray_util.plot_3d()
