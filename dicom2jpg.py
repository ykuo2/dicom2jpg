# -*- coding: utf-8 -*-
"""
dicom2jpg
=========

A simple function tool to convert DICOM files into jpg, tiff, png, or bmp files.
It applies window center(level) and window width adjustment, or VOI LUT function to the images,
which makes output files looks like what we see on standard DICOM viewers.

@author: Yu Kuo

# Todo: multiprocessing for speeding up

"""


import pydicom
import cv2
import pandas
from PIL import Image
import numpy as np
from pathlib import Path
import os
from pydicom.pixel_data_handlers.util import apply_voi_lut
import time



def get_root_get_dicom_file_list(origin):
    # if single file, return root folder of origin file and a list of that file
    origin = Path(origin)
    dicom_file_list = []
    
    # if file or folder does not exist
    if not origin.exists():
        raise OSError('File or folder does not exist')
    # if it is a file
    if origin.is_file():
        if origin.suffix.lower()!='.dcm':
            raise Exception('Input file type should be a DICOM file')
        else:
            dicom_file_list = [origin]
            root_folder = origin.parent
    # if it is a folder
    else:
        # read file
        for root, sub_f, file in os.walk(origin):
            for f in file:
                if f.lower().endswith('.dcm'):
                    file_path_dcm = Path(root)/Path(f)
                    # file_path_exp =  folder_destination / Path(f).with_suffix('.jpg')
                    # stor origin / destination
                    dicom_file_list.append(file_path_dcm)
        # sort the list
        dicom_file_list.sort()
        # foot folder
        root_folder = origin.parent
    return root_folder, dicom_file_list


def dicom2jpg(origin, target_root=None, filetype=None):
    """
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders; default: root of origin file or folder
    filetype: can be jpg, jpeg, tiff, png, or bmp
    full target file path = target_root/Today/PatientID_filetype/StudyDate_StudyTime_Modality_AccNum/Ser_Img.filetype
    """
    # set file type
    if filetype is None:
        filetype = 'jpg'
    elif filetype.lower() not in ['jpg','tiff','png', 'jpeg', 'bmp']:
        raise Exception('Target file type should be jpg, tiff, png, or bmp')
    
    # get root folder and dicom_file_list
    root_folder, dicom_file_list = get_root_get_dicom_file_list(origin)

    # if target root is not specified, set as same root of origin file 
    if target_root is None:
        target_root = root_folder
    else:
        target_root = Path(target_root)

    # Iterate through all dicom files
    for file_path in dicom_file_list:
        # read images and their pixel data
        ds = pydicom.dcmread(file_path, force=True)
        # convert pixel_array (img) to -> gray image 
        # Need JPEG 2000 plugin for pillow
        pixel_array = ds.pixel_array.astype(float)  # preparing for scaling

        # rescale slope, rescale intercept, adjust window and level
        try:
            rescale_slope = int(ds.RescaleSlope)
            rescale_intercept = int(ds.RescaleIntercept)
            pixel_array = (pixel_array)*rescale_slope+rescale_intercept
        except:
            pass

        # Adjust according to LUT, window center(level) and width values
        # xxx=np.piecewise(x, [condition1,condition2], [func1,func2])
        def get_LUT_value(data, window, level):
            return np.piecewise(data, 
                [data<=(level-0.5-(window-1)/2),
                data>(level-0.5+(window-1)/2)],
                [0,255,lambda data: ((data-(level-0.5))/(window-1)+0.5)*(255-0)])

        # get window center and window width value
        try:
            window_center = ds.WindowCenter
            window_width = ds.WindowWidth
            # some values may be stored in an array
            if type(window_center)==pydicom.multival.MultiValue:
                window_center = int(window_center[0])
            else:
                window_center = int(window_center)
            if type(window_width)==pydicom.multival.MultiValue:
                window_width = int(window_width[0])
            else:
                window_width = int(window_width)
            pixel_array = get_LUT_value(pixel_array, window_width, window_center)
        except:
        # if there is no window center, window width tag, try obtaining VOI LUT setting (usually happens to plain films)
            try:
                if ds.VOILUTSequence:
                    pixel_array = apply_voi_lut(ds.pixel_array, ds)
            except:
                pass

        # normalize to 8bit information
        # Conver to uint8 (8-bit unsigned integer), for image to save/display
        # almost no difference. However, this formula yeild slightly more standard deviation 
        pixel_array = ((pixel_array-pixel_array.min())/(pixel_array.max()-pixel_array.min())) * 255.0

        # These 2 formula are the same
        # pixel_array = (np.maximum(pixel_array,0) / pixel_array.max()) * 255.0
        #pixel_array = pixel_array - np.min(pixel_array)
        #pixel_array = pixel_array / np.max(pixel_array)
        #pixel_array = (pixel_array*255).astype(np.uint8)

        # if PhotometricInterpretation == "MONOCHROME1", then inverse; eg. xrays
        try:
            if ds.PhotometricInterpretation == "MONOCHROME1":
            # if ds.PresentationLUTShape=='INVERSE':  # not always be shown
            # NOT add minus directly
                pixel_array = np.max(pixel_array) - pixel_array
        except:
            pass
        
        # Try to get metadata        
        try:
            StudyDate = ds.StudyDate  # study date
        except:
            StudyDate = 'UnknownDate'
        try:
            StudyTime = ds.StudyTime.split('.')[0] # study time
        except:
            StudyTime = 'UnknownTime'
        try:
            AccessionNumber = ds.AccessionNumber  # Acc number
        except:
            AccessionNumber = 'UnknownAccNum'
        try:
            Modality = ds.Modality  # modality
        except:
            Modality = 'UnknownModality'
        try:
            PatientID = ds.PatientID  # patient id
        except:
            PatientID = 'UnknownID'
        try:
            SeriesNumber = ds.SeriesNumber  # series number
        except:
            SeriesNumber = 'Ser'
        try:
            InstanceNumber = ds.InstanceNumber
        except:
            InstanceNumber = 'Ins'
            
        # Full export file path
        # target_root/Today/PatientID_filetype/StudyDate_StudyTime_Modality_AccNum/Ser_Img.filetype
        today_str = time.strftime('%Y%m%d')
        full_export_fp_fn = target_root/Path(today_str)/Path(f"{PatientID}_{filetype}")/Path(f"{StudyDate}_{StudyTime}_{Modality}_{AccessionNumber}")/Path(f"{SeriesNumber}_{InstanceNumber}.{filetype}")
        # make dir
        Path.mkdir(full_export_fp_fn.parent, exist_ok=True, parents=True)
        # write file
        cv2.imwrite(str(full_export_fp_fn), pixel_array)


