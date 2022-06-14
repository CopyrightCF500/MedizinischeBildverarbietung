#!/usr/bin/python3

import xray_viewer
import sys
import os

def main():
    """
    Main function of the application.
    """
    xr_viewer = xray_viewer.XRayViewer('../data')

    xr_viewer.run()


if __name__ == '__main__':
    main()




