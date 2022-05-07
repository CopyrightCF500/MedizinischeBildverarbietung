#!/usr/bin/python3
from PIL import Image


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
        self.prepare_data()

    def prepare_data(self):
        # data type has to be uint16
        self.color_image_data = np.uint16(self.color_image_data)
        # Convert
        self.color_image_rgb = cv2.cvtColor(self.color_image_data, cv2.COLOR_BAYER_BG2RGB)

        img = Image.fromarray(self.color_image_rgb, 'RGB')
        img.show()


def main():
    opt_img = OpticalImaging()
    opt_img.run()

    print("Progam finished...")


if __name__ == '__main__':
    main()
