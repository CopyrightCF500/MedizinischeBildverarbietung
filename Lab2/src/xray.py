
import pydicom as dicom
import matplotlib.pylab as plt
import numpy as np
import glob


# specify path
list_of_files = glob.glob('data/1.2.826.0.1.3417726.3.338569.20080226110111828/*.dcm')         

def ASReadDICOM2(path):
    dict = {}
    for file_name in path:
        ds = dicom.dcmread(str(file_name))
        dict[ds.AcquisitionNumber] = ([ds.pixel_array, ds.PixelSpacing, ds])

    ret = []
    for i in range(len(dict)):
        ret.append(dict[i])
    return ret


data = ASReadDICOM2(list_of_files)