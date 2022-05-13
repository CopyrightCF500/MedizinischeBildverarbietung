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
        self.color_images_data, self.fluo_images_data = [], []
        self.color_images_rgb, self.fluo_images_rgb = [], []

    def run(self):
        """
        The run method start the pipeline of the Optical Imaging Class and complete the lab task.
        """
        self.color_images_data = img_proc_util.ImgProcUtil. \
            read_fits_file('../res/Mice2_cetu2_131213_210250_color.fits')
        # img_proc_util.ImgProcUtil.print_hdul(self.color_images_data[1]) #prints info

        self.fluo_images_data = img_proc_util.ImgProcUtil. \
            read_fits_file('../res/Mice2_cetu2_131213_210250_fluo.fits')
        # img_proc_util.ImgProcUtil.print_hdul(self.fluo_images_data[1]) #prints info

        self.prepare_color_data()
        self.prepare_fluo_data()

        # The cameras have different resolution, size and format. Co-Registrate the images!
        self.coregistration_images()

        self.display_color_images()
        self.display_fluo_images()

    def prepare_color_data(self):
        """
        This method takes the color images, change the data type and transform the images into rgb images.
        """
        # data type has to be uint16 for every image
        for image in self.color_images_data:
            image = np.uint16(image)
            # Convert
            self.color_images_rgb.append(cv2.cvtColor(image, cv2.COLOR_BAYER_BG2RGB))

        print("1. Color Image Data: nDim >>> ", self.color_images_data[0].ndim)
        print("1. Color Image Data: shape >>> ", self.color_images_data[0].shape)
        print("1. Color Image Data: size >>> ", self.color_images_data[0].size)
        print("1. Color Image Data: 1. pixel >>> ", self.color_images_data[0][0][0])
        print(self.color_images_data[0])

    def prepare_fluo_data(self):
        """
        This method takes the fluo images, ...
        """
        for image in self.fluo_images_data:  # TODO
            image = np.uint16(image)
            # Convert
            # cv2.demosaicing(image, None, image, None)
            # self.fluo_images_rgb.append(image)
            # (width, height) = self.color_images_rgb
            image = cv2.resize(image, (1392, 1024))
            # image = cv2.rotate(image, cv2.ROTATE_180)
            rgb_weights = [0.2989, 0.5870, 0.1140]
            # np.dot(image[:, :, 3], rgb_weights)
            self.fluo_images_rgb.append(image)
            # self.fluo_images_rgb.append(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

    def display_color_images(self):
        """
        This method plots the color images.
        """

        print("1. Color Image: nDim >>> ", self.color_images_rgb[0].ndim)
        print("1. Color Image: shape >>> ", self.color_images_rgb[0].shape)
        print("1. Color Image: size >>> ", self.color_images_rgb[0].size)
        print("1. Color Image: 1. pixel >>> ", self.color_images_rgb[0][0][0])
        print(self.color_images_rgb[0])

        plt.imshow(self.color_images_rgb[0])
        plt.show()

    def display_fluo_images(self):
        """
        This method plots the color images.
        """
        print("1. Fluo Image: nDim >>> ", self.fluo_images_rgb[0].ndim)
        print("1. Fluo Image: shape >>> ", self.fluo_images_rgb[0].shape)
        print("1. Fluo Image: size >>> ", self.fluo_images_rgb[0].size)
        print("1. Fluo Fluo Image: 1. pixel >>> ", self.fluo_images_rgb[0][0][0])
        print(self.fluo_images_rgb[0])
        # print("1. Image: size >>> ", self.fluo_images_rgb[0].size)

        # Wenn man sich das Bild unten auf der PDF anschaut, ist blau grün iwie aber schon richtig :D
        plt.imshow(self.fluo_images_rgb[0], cmap="Greys")
        plt.show()

    def coregistration_images(self):
        pass
        # print(self.color_images_rgb[0].shape)
        # print(self.fluo_images_rgb[0].shape)


def main():
    """
    Main function of the application.
    """
    opt_img = OpticalImaging()
    opt_img.run()

    print("Progam finished...")


if __name__ == '__main__':
    main()
