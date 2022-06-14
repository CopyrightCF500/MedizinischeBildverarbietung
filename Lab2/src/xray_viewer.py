#!/usr/bin/python3

import xray_util
import typing
import pydicom as dicom


class XRayViewer:

    def __init__(self, folder_path: str):
        self.dicom_files_folder_path = folder_path
        # List of all DICOM images
        self.dicom_files_list: typing.List[dicom.FileDataset] = []
        self.dicom_files_list = xray_util.get_dicom_list(folder_path)
        self.dicom_images = xray_util.get_images(self.dicom_files_list)

    def run(self):
        #print(type(self.dicom_files_list[0]))
        print(xray_util.display_slice(self.dicom_images[150]))
        #xray_util.display_wireframe(self.dicom_files_list)
        #print(xray_util.print_header(self.dicom_files_list[150].)))
