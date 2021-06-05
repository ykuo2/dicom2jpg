"""
dicom2jpg
=========

A simple function tool to convert DICOM files into jpg, png, or bmp files.
It applies window center(level) and window width adjustment, or VOI LUT function to the images,
which makes output files looks like what we see on standard DICOM viewers.
"""

# import info
from .__version__ import __title__, __description__, __url__, __version__
from .__version__ import __author__, __author_email__, __license__

from .utils import dicom_convertor


def dicom2jpg(origin, target_root=None):
    """
    DICOM -> jpg
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders; default: root of origin file or folder
    full target file path = target_root/TodayDate/PatientID_filetype/StudyDate_StudyTime_Modality_AccNum/Ser_Img.jpg
    """
    return dicom_convertor(origin, target_root=None, filetype='jpg')

def dicom2png(origin, target_root=None):
    """
    DICOM -> png
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders; default: root of origin file or folder
    full target file path = target_root/TodayDate/PatientID_filetype/StudyDate_StudyTime_Modality_AccNum/Ser_Img.png
    """
    return dicom_convertor(origin, target_root=None, filetype='png')


def dicom2bmp(origin, target_root=None):
    """
    DICOM -> bmp
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders; default: root of origin file or folder
    full target file path = target_root/TodayDate/PatientID_filetype/StudyDate_StudyTime_Modality_AccNum/Ser_Img.bmp
    """
    return dicom_convertor(origin, target_root=None, filetype='bmp')