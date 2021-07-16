# dicom2jpg
Converts DICOM to `JPG/PNG/BMP/TIFF` and `numpy.ndarray`



# Installation
```
pip install dicom2jpg
```

# Introdunction
```
import dicom2jpg

dicom_img_01 = "/Users/user/Desktop/img01.dcm"
dicom_dir = "/Users/user/Desktop/Patient_01"
export_location = "/Users/user/Desktop/BMP_files"

# convert single DICOM file to jpg format
dicom2jpg.dicom2jpg(dicom_img_01)  

# convert all DICOM files in dicom_dir folder to png format
dicom2jpg.dicom2png(dicom_dir)  

# convert all DICOM files in dicom_dir folder to bmp, to a specified location
dicom2jpg.dicom2bmp(dicom_dir, target_root=export_location) 

# convert single DICOM file to numpy.ndarray for further use
img_data = dicom2jpg.dicom2img(dicom_img_01)

# convert DICOM ByteIO to numpy.ndarray
img_data = dicom2jpg.io2img(dicomIO)

```
**dicom2jpg** 
converts DICOM images to `JPG/PNG/BMP/TIFF` formats and to `numpy.ndarray`. 
It piplines the lookup transformations by applying Modality LUT, VOI LUT, and Presentation LUT to the images,
which makes output files looks like what we see on standard DICOM viewers.


`dicom2jpg.dicom2jpg(origin, target_root=None, anonymous=False, multiprocessing=True)`

`dicom2jpg.dicom2png(origin, target_root=None, anonymous=False, multiprocessing=True)`

`dicom2jpg.dicom2bmp(origin, target_root=None, anonymous=False, multiprocessing=True)`

`dicom2jpg.dicom2tiff(origin, target_root=None, anonymous=False, multiprocessing=True)`

- origin can be a single DICOM file, a folder, or a list/tuple of file/folder
- target_root would be the root folder of the first file/folder if not specified
- exported files paths would be

    > *target_root / Today / PatientID_Filetype / StudyDate_StudyTime_Modality_AccNum / Ser_Img.Filetype* 

- anonymous files paths would be

    > *target_root / Today / Patient_SerialNum / ModalitySerialNum_Modality / Ser_Img.Filetype*


`dicom2jpg.dicom2img(origin)`

`dicom2jpg.io2img(dicomIO)`

- converting dicom files or ByteIO to ndarray
- ndarray is in 8 bit; RGB format if it's a color image



# Image examples

|   CT   |   MR    |CXR|
|------------|-------------|------------|
|<img src="https://user-images.githubusercontent.com/37744685/120668917-8724cc00-c4c1-11eb-957b-82e59ba03806.jpg" width="250">|<img src="https://user-images.githubusercontent.com/37744685/120668923-8855f900-c4c1-11eb-80fd-8c0c2235014b.jpg" width="250">|<img src="https://user-images.githubusercontent.com/37744685/120671666-32368500-c4c4-11eb-92fd-726dc02c966c.jpg" width="250">|



# Todo
- Support multi-frame images
- Image compression
- Support overlays
   
   
# Performance
- Environment: Windows10, Jupyter Notebook, Python 3.8.10
- 598MB 1873 files {'CT': 1528, 'CR': 52, 'MR': 174, 'DX': 36}
- Intel(R) Core(TM) i7-7700 CPU @ 3.60GHz. 4 Cores (hyper-threading off)
- Tested on Ramdisk (no physical HDD was tortured :P)

| multiprocessing  |  anonymous |  duration (seconds) |
|------------|-------------|------------|
|False|True|154.6-159.7|
|True|True|79.2-82.9|
|False|False|157.9-162.8|
|True|False|56-58.5|
