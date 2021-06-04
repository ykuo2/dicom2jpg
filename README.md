# dicom2jpg
A simple function tool to convert DICOM files into jpg, tiff, png, or bmp files.

# Intro
It applies window center(level) and window width adjustment, or VOI LUT function to the images,
which makes output files looks like what we see on standard DICOM viewers.

# Known issue
- Error while converting multi-frame fluoroscopic image array
```
error: OpenCV(4.0.1) C:\ci\opencv-suite_1573470242804\work\modules\imgcodecs\src\loadsave.cpp:667: error: (-215:Assertion failed) image.channels() == 1 || image.channels() == 3 || image.channels() == 4 in function 'cv::imwrite_'
```

# Todo
- Multiprocessing for speeding up

# Image examples

|   CT   |   MR    |CXR|
|------------|-------------|------------|
|<img src="https://user-images.githubusercontent.com/37744685/120668917-8724cc00-c4c1-11eb-957b-82e59ba03806.jpg" width="250">|<img src="https://user-images.githubusercontent.com/37744685/120668923-8855f900-c4c1-11eb-80fd-8c0c2235014b.jpg" width="250">|<img src="https://user-images.githubusercontent.com/37744685/120671666-32368500-c4c4-11eb-92fd-726dc02c966c.jpg" width="250">|

 
  
   



