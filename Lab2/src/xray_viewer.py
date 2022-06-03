#!/usr/bin/python3

import xray_util


class XRayViewer:

    def __init__(self, folderPath):
        self.dicom_files_folder_path = folderPath
        # List of all DICOM images
        self.dicom_images: list[dict[any]] = xray_util.GetDicomImagesList(folderPath)

    def run(self):

        xray_util.display_slice(self.dicom_images[150][0])
        # print(data[140][2])
        # print(data[140][2].ImagePositionPatient)

        #xray_util.display_wireframe(self.dicom_images)

        # print(data[0][1][0])