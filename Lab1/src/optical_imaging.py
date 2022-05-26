#!/usr/bin/python3

"""
This module contains the OpticalImaging Class
"""

from typing import overload
from img_proc_util import *


class OpticalImaging:
    
    """
    This class contains and displays the color and fluorescence images.
    """

    def __init__(self):
        self.color_data, self.fluo_data = [], []
        self.color_images_time_list, self.fluo_images_time_list = [], []
        self.fluo_trans_3x3matrix = []
        self.all_times = []

    def run(self):
        """
        The run method start the pipeline of the Optical Imaging Class and complete the lab task.
        """

        try:
            self.color_data = fits.open('../res/Mice2_cetu2_131213_210250_color.fits')
            self.fluo_data =  fits.open('../res/Mice2_cetu2_131213_210250_fluo.fits')

            print("READING COLOR FITS FILE")
            print("READING FLUO FITS FILE")

        except FileNotFoundError:
            print("Error while trying to read color image fits file!")

        # contains list: [[timestamp1, image_data1], [timestamp2, image_data2], ... ]
        self.color_images_time_list = image_timestamp_list(self.color_data)
        self.fluo_images_time_list = image_timestamp_list(self.fluo_data)

        # contains 3x3 transformations matrix
        self.fluo_trans_3x3matrix = trans_parameter(self.fluo_data[0])
        #print(self.fluo_trans_3x3matrix)

        self.color_data.close()
        self.fluo_data.close()

        #find corresponding images depending on timestamps
        self.all_times = find_matching(self.color_images_time_list, self.fluo_images_time_list)

        self.color_images_time_list = prepare_color_data(self.color_images_time_list)
        self.fluo_images_time_list = prepare_fluo_data(self.fluo_images_time_list, self.fluo_trans_3x3matrix)

        #display_images(self.color_images_time_list[self.all_times[0][0]][1], self.fluo_images_time_list[self.all_times[0][1]][1])

        #overlapping = cv2.addWeighted(self.color_images_time_list[0][1], 1.0, self.fluo_images_time_list[6][1], 0.3, 0)
        #display_image(overlapping)

        overlapped_images = []
        overlapped_images = overlap(self.color_images_time_list, self.fluo_images_time_list, self.all_times)

        generate_video(overlapped_images)
        


def main():
    """
    Main function of the application.
    """
    opt_img = OpticalImaging()
    opt_img.run()

    print("Progam finished...")


if __name__ == '__main__':
    main()
