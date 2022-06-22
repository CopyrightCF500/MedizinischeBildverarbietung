#!/usr/bin/python3

"""
This module contains the OpticalImaging Class
"""

from typing import List, overload

import numpy as np
from img_proc_util import *
import sys


class OpticalImaging:
    
    """
    This class contains and displays the color and fluorescence images.
    """

    def __init__(self):
        self.color_data, self.fluo_data  = [], []
        self.color_images_time_list, self.fluo_images_time_list , self.fluo_only_images = [], [], []
        self.fluo_trans_3x3matrix = []
        self.all_times = []
        self.video_data = []

    def run(self):
        """
        The run method start the pipeline of the Optical Imaging Class and complete the lab task.
        """

        try:
            print("READING COLOR FITS FILE...")
            self.color_data: fits.HDUList = fits.open('../res/Mice2_cetu2_131213_210250_color.fits')
            print("READING FLUO FITS FILE...")
            self.fluo_data: fits.HDUList =  fits.open('../res/Mice2_cetu2_131213_210250_fluo.fits')

        except FileNotFoundError:
            sys.exit('Error while trying to read color image fits file!')

        # contains list: [[timestamp1, image_data1], [timestamp2, image_data2], ... ]
        self.color_images_time_list: list[list[int]] = image_timestamp_list(self.color_data)
        self.fluo_images_time_list: list[list[int]] = image_timestamp_list(self.fluo_data)
        for time, image in self.fluo_images_time_list:
            self.fluo_only_images.append((image))

        # contains 3x3 transformation matrix
        self.fluo_trans_3x3matrix: np.ndarray = trans_parameter(self.fluo_data[0])

        self.color_data.close()
        self.fluo_data.close()

        # find corresponding images depending on timestamps
        self.all_times: list[list[int]] = find_matching(self.color_images_time_list, self.fluo_images_time_list)

        self.color_images_time_list = prepare_color_data(self.color_images_time_list)
        self.fluo_images_time_list = prepare_fluo_data(self.fluo_images_time_list, self.fluo_trans_3x3matrix)

        # Aufgabe 2: display corresponding images
        '''
        display_images(self.color_images_time_list[self.all_times[400][0]][1], self.fluo_images_time_list[self.all_times[400][1]][1])
        '''

        # Aufgabe 3: generate video
        '''
        overlapped_images: list[np.ndarray] = []
        overlapped_images = overlap(self.color_images_time_list, self.fluo_images_time_list, self.all_times)
        generate_video(overlapped_images, 'video.mp4', (1392,1024))
        '''

        # Aufgabe 4: hochaufgeloestes Video

        #'''
        video_path = '../res/Movie human colon xenograft 1.mp4'
        print("READING VIDEO FILE...")
        self.video_data = capture_video(video_path)
        #display_image(self.video_data[0][0])

        # compare fluo size with video_data size
        self.fluo_only_images = update_size(len(self.video_data), len(self.fluo_only_images), self.fluo_only_images)

        self.fluo_only_images = prepare_fluo_data_2(self.fluo_only_images)
        #display_image(self.fluo_only_images[0][0])

        self.fluo_only_images = apply_matrix(self.video_data, self.fluo_only_images)

        #for i in range(len(self.fluo_only_images)):
            #M = calculate_transform_matrix(self.fluo_only_images[i], self.video_data[i])
            #self.fluo_only_images[i] = cv2.warpAffine(self.fluo_only_images[i], M, (768,576))

        overlapped_images = []
        overlapped_images = overlap_2(self.video_data, self.fluo_only_images)

        generate_video(overlapped_images, 'video2.mp4', (480, 480))
        #generate_video(self.fluo_only_images, 'video3.mp4', (480, 480))

        #'''



def main():
    """
    Main function of the application.
    """
    opt_img = OpticalImaging()
    opt_img.run()

    print("Progam finished...")


if __name__ == '__main__':
    main()
