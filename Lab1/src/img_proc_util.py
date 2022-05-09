#!/usr/bin/python3

"""
This module contains the ImgProcUtil Class
"""

import numpy as np
from astropy.io import fits


class ImgProcUtil:
    """
    This utility class read the fits files and contains some
    other usefully methods for image processing.
    """

    def __init__(self):
        pass

    @staticmethod
    def read_fits_color_file(path: str) -> np.ndarray:
        """
        This method gets a path of the FITS color images and returns
        all the containing images in a list.
        :param path: path of fits color image file
        :type path: str
        :return: One image of the fits file
        :rtype: numpy.ndarray
        """

        img_list = []
        try:
            color_image_hdul = fits.open(path)

            for image in color_image_hdul[1:]:
                img_list.append(image.data)

            color_image_hdul.close()

            return img_list

        except FileNotFoundError:
            print("Error while trying to read color image fits file!")

    @staticmethod
    def print_hdul(hdul: fits.HDUList):
        """
        This method prints the info and an example of the given HDUList.
        :param hdul: HDUList to inspect
        :type hdul: fits.HDUList
        """
        print(hdul.info())
        print(hdul[30:40, 10:20])
