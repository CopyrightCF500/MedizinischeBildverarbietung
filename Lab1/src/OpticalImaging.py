#!/usr/bin/python3

from astropy.io import fits
from astropy.table import Table

import numpy as np
import matplotlib.pyplot as plt
import cv2

import ImgProcUtil


class OpticalImaging:
    def __init__(self):
        self.color_image_data = None
        self.color_image_rgb = np.empty((1024, 1392))

    def run(self):
        self.color_image_data = ImgProcUtil.ImgProcUtil.read_fits_color_file('../res/Mice2_cetu2_131213_210250_color.fits')
        print("test")
        self.prepare_data()

    def prepare_data(self):
        self.color_image_data = np.uint16(self.color_image_data)
        self.color_image_rgb = cv2.cvtColor(self.color_image_data, cv2.COLOR_BAYER_BG2RGB)
        normalized_color_image = cv2.normalize(self.color_image_rgb, None, alpha=0.5, beta=1, norm_type=cv2.NORM_MINMAX,
                                               dtype=cv2.CV_16U)
        # plt.imshow(self.color_image_rgb)
        cv2.imshow('TestImage', self.color_image_rgb)
        cv2.waitKey(0)


def main():
    opt_img = OpticalImaging()
    opt_img.run()

    print("Progam finished...")


if __name__ == '__main__':
    main()
