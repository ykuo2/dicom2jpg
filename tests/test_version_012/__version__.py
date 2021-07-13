

__title__ = 'dicom2jpg'
__version__ = "0.1.2"
__author__ = 'Yu Kuo'
__description__ = 'DICOM -> JPG/PNG/BMP/TIFF/ndarray'
__url__ = 'https://github.com/ucs198604/dicom2jpg'
__author_email__ = 'ucs198604@gmail.com'
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