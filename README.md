# Medizinische Bildverarbietung

This repository contains the lab exercises of the ***Medical image processing*** module at the University Of Applied Sciences Munich.

## 1. Lab - Optical Imaging

The goal of the task is to read in a DICOM volume image dataset, process it and display it in different ways.
### [Task](https://github.com/CopyrightCF500/MedizinischeBildverarbietung/blob/main/Lab1/mbv_aufabe_optical_imaging.pdf)

## 2. Lab - Digital Imaging and Communications in Medicine

The aim of the task is to read in, prepare and display the optical image data of a flexible endoscope.

### [Task](https://github.com/CopyrightCF500/MedizinischeBildverarbietung/blob/main/Lab2/mbv_aufgabe_xray_mk002.pdf)

## Prepare Workspace
Because the Mice2_cetu2_131213_210250_color.fits and Mice2_cetu2_131213_210250_fluo.fits files are too large, you have to put them own your own into the Lab1/res folder that you have to create aswell.

## Requiered Python Modules

* [Astropy](https://docs.astropy.org/en/stable/io/fits/index.html#) provides access to FITS files. FITS (Flexible Image Transport System) 
is a portable file standard widely used in the astronomy community to store images and tables.

``` bash
python3 -m pip install --user astropy
```

* [OpenCV](https://opencv.org/) for image processing.

``` bash
pip3 install opencv-python
```
