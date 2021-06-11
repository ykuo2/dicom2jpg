# dicom2jpg
Converts DICOM to `JPG/PNG/BMP/TIFF` and `numpy.ndarray`

```
import dicom2jpg

dicom_img_01 = "/Users/user/Desktop/img01.dcm"
dicom_dir = "/Users/user/Desktop/Patient_01"
export_location = "/Users/user/Desktop/BMP_files"

# convert single DICOM file to numpy.ndarray for further use
img_data = dicom2jpg.dicom2img(dicom_img_01)

# convert single DICOM file to jpg format
dicom2jpg.dicom2jpg(dicom_img_01)  

# convert all DICOM files in dicom_dir folder to png format
dicom2jpg.dicom2png(dicom_dir)  

# convert all DICOM files in dicom_dir folder to bmp, to a specified location
dicom2jpg.dicom2bmp(dicom_dir, target_root=export_location) 

```
**dicom2jpg** 
converts DICOM images to `JPG/PNG/BMP/TIFF` formats and to `numpy.ndarray`. 
It applies window center(level) and window width adjustment, or VOI LUT function to the images, which makes output files looks like what we see on standard DICOM viewers.

`dicom2jpg.dicom2jpg(origin, target_root=None)`

`dicom2jpg.dicom2png(origin, target_root=None)`

`dicom2jpg.dicom2bmp(origin, target_root=None)`

`dicom2jpg.dicom2tiff(origin, target_root=None)`

`dicom2jpg.dicom2img(origin)`

- origin can be a single DICOM file or folder contains DICOM files
- target_root is would be the same root folder of the origin if not specified
- exported files will be in  

    > *target_root/Today/PatientID_filetype/StudyDate_StudyTime_Modality_AccNum/Ser_Img.filetype* 


# Image examples

|   CT   |   MR    |CXR|
|------------|-------------|------------|
|<img src="https://user-images.githubusercontent.com/37744685/120668917-8724cc00-c4c1-11eb-957b-82e59ba03806.jpg" width="250">|<img src="https://user-images.githubusercontent.com/37744685/120668923-8855f900-c4c1-11eb-80fd-8c0c2235014b.jpg" width="250">|<img src="https://user-images.githubusercontent.com/37744685/120671666-32368500-c4c4-11eb-92fd-726dc02c966c.jpg" width="250">|



# Installation
```
pip install dicom2jpg
```


# Todo
- Multiprocessing for speeding up
- Support multi-frame images
- More naming choices, including anomynous file names
- Image compression
- Support overlays
   



