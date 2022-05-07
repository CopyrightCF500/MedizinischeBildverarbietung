#!/usr/bin/python3
"""
This module contains the OpticalImaging Class
"""

from PIL import Image

import numpy as np
# import matplotlib.pyplot as plt
import cv2

import img_proc_util


class OpticalImaging:
    """
    This class contains and displays the color and fluorescence images.
    """

    def __init__(self):
        self.color_image_data = None
        self.color_image_rgb = np.empty((1024, 1392))

    def run(self):
        """
        The run method start the pipeline of the Optical Imaging Class and complete the lab task.
        """
        self.color_image_data = img_proc_util.ImgProcUtil. \
            read_fits_color_file('../res/Mice2_cetu2_131213_210250_color.fits')
        self.prepare_data()

    def prepare_data(self):
        """
        This method takes the color images data and prepare it for further processing.
        """
        # data type has to be uint16
        self.color_image_data = np.uint16(self.color_image_data)
        # Convert
        self.color_image_rgb = cv2.cvtColor(self.color_image_data, cv2.COLOR_BAYER_BG2RGB)

        img = Image.fromarray(self.color_image_rgb, 'RGB')
        img.show()


def main():
    """
    Main function of the application.
    """
    opt_img = OpticalImaging()
    opt_img.run()

    print("Progam finished...")


if __name__ == '__main__':
    main()
