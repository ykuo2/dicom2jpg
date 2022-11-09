

__title__ = 'dicom2jpg'
__version__ = "0.1.10"
__author__ = 'Yu Kuo'
__description__ = 'DICOM -> JPG/PNG/BMP/TIFF/ndarray'
__url__ = 'https://github.com/ykuo2/dicom2jpg'
__author_email__ = 'ykuo2.tw@gmail.com'
__license__ = 'MIT'


### Issue, pending work
#  support overlay
#  image quality, compression

### Release Notes ###
## 0.0.8 
#  reconstruct function, for future multiprocessing and naming
#  add dicom2img, converting to ndarray
#  add dicom2tiff, converting to tiff file

## 0.0.9
#  add io2img, converting BytesIO to ndarray 

## 0.1.0
#  support multiprocessing
#  support exporting anonymous file names

## 0.1.1
#  minor fix

## 0.1.2
#  support list/tuples of file origin
#  re-write dicom2img, io2img
#  update readme

## 0.1.3
#  fix bug of repeated rescaling for window/level 

## 0.1.4
#  fix bug: int(window center/level) may lead to erronous image in small window/level files, such as DWI/ADC

## 0.1.6
#  fix bug: LUT Functions according to C.11.2 

## 0.1.7, 0.1.8, 0.1.9 0.1.10
#  minor polishment