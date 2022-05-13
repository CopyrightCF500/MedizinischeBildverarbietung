#!/usr/bin/python3
"""
This module contains the OpticalImaging Class
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2

import img_proc_util


class OpticalImaging:
    """
    This class contains and displays the color and fluorescence images.
    """

    def __init__(self):
        self.color_image_data = None
        self.color_image_rgb = np.empty((1024, 1392))
        self.color_images_data = []
        self.color_images_rgb = []
        self.fluo_images_data = []

    def run(self):
        """
        The run method start the pipeline of the Optical Imaging Class and complete the lab task.
        """
        self.color_images_data = img_proc_util.ImgProcUtil. \
            read_fits_file('../res/Mice2_cetu2_131213_210250_color.fits')
        #img_proc_util.ImgProcUtil.print_hdul(self.color_images_data[1]) #prints info

        self.fluo_images_data = img_proc_util.ImgProcUtil. \
            read_fits_file('../res/Mice2_cetu2_131213_210250_fluo.fits')
        #img_proc_util.ImgProcUtil.print_hdul(self.fluo_images_data[1]) #prints info

        self.prepare_color_data()
        self.prepare_fluo_data()

        self.display_color_images()
        self.display_fluo_images()

    def prepare_color_data(self):
        """
        This method takes the color images, change the data type and transform the images into rgb images.
        """
        # data type has to be uint16 for every image
        for image in self.color_images_data[0]:
            image = np.uint16(image)
            # Convert
            self.color_images_rgb.append(cv2.cvtColor(image, cv2.COLOR_BAYER_BG2RGB))
            
    def prepare_fluo_data(self):
        """
        This method takes the fluo images, ...
        """
        for image in self.fluo_images_data[0]: # TODO
            image = np.uint16(image)
            # Convert
            #self.fluo_images_rgb.append(cv2.cvtColor(image, cv2.COLOR_BAYER_BG2RGB))

    def display_color_images(self):
        """
        This method plots the color images.
        """
        plt.imshow(self.color_images_rgb[0], interpolation='nearest')
        plt.show()

    def display_fluo_images(self):
        """
        This method plots the color images.
        """
        plt.imshow(self.fluo_images_data[0][0], interpolation='nearest')
        plt.show()

def main():
    """
    Main function of the application.
    """
    opt_img = OpticalImaging()
    opt_img.run()

    print("Progam finished...")


if __name__ == '__main__':
    main()
