"""
dicom2jpg
=========

A simple function tool to convert DICOM files into jpg, png, tiff, or bmp files and Numpy array.
It applies window center(level) and window width adjustment, or VOI LUT function to the images,
which makes output files looks like what we see on standard DICOM viewers.
"""

# import info
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__

from .utils import _dicom_convertor
from .utils import _dcmio_to_img


def io2img(dcmio):
    """
    DICOM BytesIO -> ndarray
    """
    return _dcmio_to_img(dcmio)

def dicom2img(origin):
    """
    DICOM -> ndarray
    origin: a .dcm file
    """
    return _dicom_convertor(origin, target_root=None, filetype='img')

def dicom2tiff(origin, target_root=None, anonymous=False, multiprocessing=True):
    # under construction
    """
    DICOM -> tiff
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders
    default target root folder is the root of origin file
    """
    return _dicom_convertor(origin, target_root, filetype='tiff',
                            multiprocessing=multiprocessing, 
                            anonymous=anonymous)

def dicom2jpg(origin, target_root=None, anonymous=False, multiprocessing=True):
    """
    DICOM -> jpg
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders
    default target root folder is the root of origin file
    """
    return _dicom_convertor(origin, target_root, filetype='jpg',
                            multiprocessing=multiprocessing, 
                            anonymous=anonymous)

def dicom2png(origin, target_root=None, anonymous=False, multiprocessing=True):
    """
    DICOM -> png
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders
    default target root folder is the root of origin file

    """
    return _dicom_convertor(origin, target_root, filetype='png',
                            multiprocessing=multiprocessing, 
                            anonymous=anonymous)


def dicom2bmp(origin, target_root=None, anonymous=False, multiprocessing=True):
    """
    DICOM -> bmp
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders
    default target root folder is the root of origin file

    """
    return _dicom_convertor(origin, target_root, filetype='bmp',
                            multiprocessing=multiprocessing, 
                            anonymous=anonymous)