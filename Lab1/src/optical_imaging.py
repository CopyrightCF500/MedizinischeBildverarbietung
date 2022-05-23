#!/usr/bin/python3

"""
This module contains the OpticalImaging Class
"""
import numpy as np
import matplotlib.pyplot as plt
import cv2
from astropy.io import fits

import img_proc_util


class OpticalImaging:
    
    """
    This class contains and displays the color and fluorescence images.
    """

    def __init__(self):
        self.color_data, self.fluo_data = [], []
        self.color_images_time_list, self.fluo_images_time_list = [], []
        self.fluo_trans_3x3matrix = []
        self.color_images_rgb, self.fluo_images_rgb = [], []

    def run(self):
        """
        The run method start the pipeline of the Optical Imaging Class and complete the lab task.
        """

        try:
            self.color_data = fits.open('../res/Mice2_cetu2_131213_210250_color.fits')
            self.fluo_data =  fits.open('../res/Mice2_cetu2_131213_210250_fluo.fits')

            print("READING FLUO FITS FILE")
            print("READING COLOR FITS FILE")

        except FileNotFoundError:
            print("Error while trying to read color image fits file!")

        # contains list: [[timestamp1, image_data1], [timestamp2, image_data2], ... ]
        self.color_images_time_list = img_proc_util.image_timestamp_list(self.color_data)
        self.fluo_images_time_list = img_proc_util.image_timestamp_list(self.fluo_data)

        # contains 3x3 transformations matrix
        self.fluo_trans_3x3matrix = img_proc_util.trans_parameter(self.fluo_data[0])

        self.color_data.close()
        self.fluo_data.close()

        print(self.fluo_trans_3x3matrix)

        #print(self.color_images_time_list)
        #print(self.fluo_images_time_list)
#        self.prepare_color_data()
#        self.prepare_fluo_data()
#
#        # The cameras have different resolution, size and format. Co-Registrate the images!
#        self.coregistration_images()
#
#        self.display_color_images()
#        self.display_fluo_images()
#
#    def prepare_color_data(self):
#        """
#        This method takes the color images, change the data type and transform the images into rgb images.
#        """
#        # data type has to be uint16 for every image
#        for image in self.color_images_data:
#            image = np.uint16(image)
#            # Convert
#            self.color_images_rgb.append(cv2.cvtColor(image, cv2.COLOR_BAYER_BG2RGB))
#
#        print("1. Color Image Data: nDim >>> ", self.color_images_data[0].ndim)
#        print("1. Color Image Data: shape >>> ", self.color_images_data[0].shape)
#        print("1. Color Image Data: size >>> ", self.color_images_data[0].size)
#        print("1. Color Image Data: 1. pixel >>> ", self.color_images_data[0][0][0])
#        #print(self.color_images_data[0])
#
#    def prepare_fluo_data(self):
#        """
#        This method takes the fluo images, ...
#        """
#        for image in self.fluo_images_data:  # TODO
#            image = np.uint16(image)
#            # Convert
#            image = cv2.resize(image, (1392, 1024))
#            #self.fluo_images_rgb.append(cv2.cvtColor(image, cv2.COLOR_BAYER_BG2RGB))
#            # image = cv2.rotate(image, cv2.ROTATE_180)
#            #rgb_weights = [0.2989, 0.5870, 0.1140]
#            # np.dot(image[:, :, 3], rgb_weights)
#            self.fluo_images_rgb.append(image)
#
#    def display_color_images(self):
#        """
#        This method plots the color images.
#        """
#
#        print("1. Color Image: nDim >>> ", self.color_images_rgb[0].ndim)
#        print("1. Color Image: shape >>> ", self.color_images_rgb[0].shape)
#        print("1. Color Image: size >>> ", self.color_images_rgb[0].size)
#        print("1. Color Image: 1. pixel >>> ", self.color_images_rgb[0][0][0])
#        #print(self.color_images_rgb[0])        
#
#        plt.imshow(self.color_images_rgb[0])
#        plt.show()
#
#    def display_fluo_images(self):
#        """
#        This method plots the color images.
#        """
#        print("1. Fluo Image: nDim >>> ", self.fluo_images_rgb[0].ndim)
#        print("1. Fluo Image: shape >>> ", self.fluo_images_rgb[0].shape)
#        print("1. Fluo Image: size >>> ", self.fluo_images_rgb[0].size)
#        print("1. Fluo Fluo Image: 1. pixel >>> ", self.fluo_images_rgb[0][0][0])
#        #print(self.fluo_images_rgb[0])
#        # print("1. Image: size >>> ", self.fluo_images_rgb[0].size)
#
#        #self.fluo_images_rgb[0] -= 300
#
#        # Wenn man sich das Bild unten auf der PDF anschaut, ist blau grün iwie aber schon richtig :D
#        #plt.imshow(self.fluo_images_rgb[0], cmap="Greys")
#        plt.imshow(self.fluo_images_rgb[0])
#        plt.show()
#
#    def coregistration_images(self):
#        pass
#        # print(self.color_images_rgb[0].shape)
#        # print(self.fluo_images_rgb[0].shape)


def main():
    """
    Main function of the application.
    """
    opt_img = OpticalImaging()
    opt_img.run()

    print("Progam finished...")


if __name__ == '__main__':
    main()
