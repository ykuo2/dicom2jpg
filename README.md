# dicom2jpg
A simple function tool to convert DICOM files into jpg, tiff, png, or bmp files.

# Intro
It applies window center(level) and window width adjustment, or VOI LUT function to the images,
which makes output files looks like what we see on standard DICOM viewers.

# Known issue
- Error code
```
error: OpenCV(4.0.1) C:\ci\opencv-suite_1573470242804\work\modules\imgcodecs\src\loadsave.cpp:667: error: (-215:Assertion failed) image.channels() == 1 || image.channels() == 3 || image.channels() == 4 in function 'cv::imwrite_'
```
- Color inversion issue
  -- of some color "print screen" images, such as ultrasound, PET, and dosimetry info of CT, etc..

# Todo
- Multiprocessing for speeding up
