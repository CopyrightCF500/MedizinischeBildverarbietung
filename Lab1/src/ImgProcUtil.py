#!/usr/bin/python3

from astropy.io import fits


class ImgProcUtil:
    def __init__(self):
        pass

    @staticmethod
    def read_fits_color_file(path: str):
        color_image_hdul = fits.open(path)
        color_image_data = color_image_hdul[100].data
        return color_image_data

    @staticmethod
    def print_hdul(hdul):
        # Header Data Unit List
        print(hdul.info())
        print(hdul[30:40, 10:20])
