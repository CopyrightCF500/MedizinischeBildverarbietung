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
    def read_fits_file(path: str) -> np.ndarray:
        """
        This method gets a path of the FITS images and returns
        all the containing images in a list.
        :param path: path of fits image file
        :type path: str
        :return: (list of color images, hdul data)
        :rtype: numpy.ndarray
        """

        img_list = []
        try:
            image_hdul = fits.open(path)
            if "fluo" in path:
                print("READING FLUO IMAGES")
            else:
                print("READING COLOR IMAGES")

            print(image_hdul[0].header)

            already_printed_one = False

            for image in image_hdul[1:10]:
                if not already_printed_one:
                    print("1. numpy element - SHAPE: ", image.data.shape)
                    print("1. numpy element - ndim: ", image.data.ndim)
                    already_printed_one = True
                img_list.append(image.data)

            print("\n")
            image_hdul.close()

            #print(image_hdul[0].header)
            #print(image_hdul[0].header['TRANSC0'])


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
        #print(hdul[30:40, 10:20])
