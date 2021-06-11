# utils.py

import pydicom
import cv2
import numpy as np
from pathlib import Path
import os
from pydicom.pixel_data_handlers.util import apply_voi_lut
import time

    

def _get_export_file_path(ds, target_root, filetype):
    # construct export file path
    #
    # Todo: options to file naming
    # multiprocessing -> may need Manager.dict()
    # 
    # Try to get metadata       
    patient_metadata = _get_metadata(ds)
    StudyDate = patient_metadata['StudyDate']
    StudyTime = patient_metadata['StudyTime']
    AccessionNumber = patient_metadata['AccessionNumber']
    Modality = patient_metadata['Modality']
    PatientID = patient_metadata['PatientID']
    SeriesNumber = patient_metadata['SeriesNumber']
    InstanceNumber = patient_metadata['InstanceNumber']
        
    # Full export file path
    # target_root/Today/PatientID_filetype/StudyDate_StudyTime_Modality_AccNum/Ser_Img.filetype
    today_str = time.strftime('%Y%m%d')
    full_export_fp_fn = target_root/Path(today_str)/Path(f"{PatientID}_{filetype}")/Path(f"{StudyDate}_{StudyTime}_{Modality}_{AccessionNumber}")/Path(f"{SeriesNumber}_{InstanceNumber}.{filetype}")
    
    return full_export_fp_fn



def _ds_to_file(file_path, target_root, filetype):
    
    # read images and their pixel data
    ds = pydicom.dcmread(file_path, force=True)
    
    # to exclude unsupported SOP class by its UID
    # PDF
    if ds.SOPClassUID == '1.2.840.10008.5.1.4.1.1.104.1':
        print('SOP class - 1.2.840.10008.5.1.4.1.1.104.1(Encapsulated PDF Storage) is currently not supported')
        # continue
        return False
    
    # load pixel_array 
    # This is the time-limited step
    pixel_array = ds.pixel_array.astype(float)  # preparing for scaling
    
    # if pixel_array.shape[2]==3 -> means color files [x,x,3]
    # [o,x,x] means multiframe
    if len(pixel_array.shape)==3 and pixel_array.shape[2]!=3:
        print('Multiframe images are currently not supported')
        # continue
        return False

    # rescale slope, rescale intercept, adjust window and level
    try:
        # cannot use INT, because resale slope could be<1 
        rescale_slope = ds.RescaleSlope # int(ds.RescaleSlope)
        rescale_intercept = ds.RescaleIntercept #  int(ds.RescaleIntercept)
        pixel_array = (pixel_array)*rescale_slope+rescale_intercept
    except:
        pass

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
        pixel_array = _get_LUT_value(pixel_array, window_width, window_center)
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

    # if PhotometricInterpretation == "MONOCHROME1", then inverse; eg. xrays
    try:
        if ds.PhotometricInterpretation == "MONOCHROME1":
        # if ds.PresentationLUTShape=='INVERSE':  # not always be shown
        # NOT add minus directly
            pixel_array = np.max(pixel_array) - pixel_array
    except:
        pass
    
    # conver float -> 8-bit
    pixel_array = pixel_array.astype('uint8')
    
    ##########################
    # convert to pixel image #
    ##########################
    if filetype.lower()=='img':
        return pixel_array
    
    ########################
    # Process to save file #
    ########################
    # YBR_RCT and RGB data already be converted by RGB implicitly by pydicom  
    # how about YBR_FULL/YBR_FULL_422/Palette Colour/YBR_ICT  ?
    # should be convert to "BGR" due to open-cv's RGB arrangement
    if 'PhotometricInterpretation' in ds and ds.PhotometricInterpretation in ['YBR_RCT','RGB']:
        # pixel_array = cv2.cvtColor(np.float32(pixel_array), cv2.COLOR_RGB2BGR)
        pixel_array[:,:,[0,2]] = pixel_array[:,:,[2,0]]
    
    # get full export file path and file name
    full_export_fp_fn = _get_export_file_path(ds, target_root, filetype)
    # make dir
    Path.mkdir(full_export_fp_fn.parent, exist_ok=True, parents=True)
    # write file
    cv2.imwrite(str(full_export_fp_fn), pixel_array)
    
    return True


def _dicom_convertor(origin, target_root=None, filetype=None):
    """
    origin: can be a .dcm file or a folder
    target_root: root of output files and folders; default: root of origin file or folder
    filetype: can be jpg, jpeg, png, bmp, or ndarray
    full target file path = target_root/Today/PatientID_filetype/StudyDate_StudyTime_Modality_AccNum/Ser_Img.filetype
    """
    # set file type
    if filetype is None:
        filetype = 'jpg'
    elif filetype.lower() not in ['jpg','png','jpeg', 'bmp', 'img', 'tiff']:
        raise Exception('Target file type should be jpg, png, or bmp')
    
    # get root folder (as target_root) and dicom_file_list
    target_root, dicom_file_list = _get_root_get_dicom_file_list(origin, target_root)

    # process image and return ndarray, only one file in dicom_file_list
    if filetype.lower()=='img':
        return _ds_to_file(dicom_file_list[0], target_root, filetype)
    
    # process image and export files (prepare for multiprocessing)
    # Iterate through all dicom files
    for file_path in dicom_file_list:
        _ds_to_file(file_path, target_root, filetype)

    return True


def _get_root_get_dicom_file_list(origin, target_root):
    # if single file, return root folder of origin file and a list of that file
    origin = Path(origin)
    dicom_file_list = []
    
    # if file or folder does not exist
    if not origin.exists():
        raise OSError('File or folder does not exist')
    # if it is a file, then check if it's a dicom and convert it to a list
    if origin.is_file():
        if origin.suffix.lower()!='.dcm':
            raise Exception('Input file type should be a DICOM file')
        else:
            dicom_file_list = [origin]

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
        
    # set root_folder
    # if target root is not specified, set as same root of origin file 
    if target_root is None:
        root_folder = origin.parent
    else:
        root_folder = Path(target_root)
        
    return root_folder, dicom_file_list



def _get_LUT_value(data, window, level):
    # Adjust according to LUT, window center(level) and width values
    # xxx=np.piecewise(x, [condition1,condition2], [func1,func2])
    return np.piecewise(data, 
        [data<=(level-0.5-(window-1)/2),
        data>(level-0.5+(window-1)/2)],
        [0,255,lambda data: ((data-(level-0.5))/(window-1)+0.5)*(255-0)])


def _get_metadata(ds):
    # get patient metadata
    metadata = {}
    try:
        metadata['StudyDate'] = ds.StudyDate  # study date
    except:
        metadata['StudyDate'] = 'UnknownDate'
    try:
        metadata['StudyTime'] = ds.StudyTime.split('.')[0] # study time
    except:
        metadata['StudyTime'] = 'UnknownTime'
    try:
        metadata['AccessionNumber'] = ds.AccessionNumber  # Acc number
    except:
        metadata['AccessionNumber'] = 'UnknownAccNum'
    try:
        metadata['Modality'] = ds.Modality  # modality
    except:
        metadata['Modality'] = 'UnknownModality'
    try:
        metadata['PatientID'] = ds.PatientID  # patient id
    except:
        metadata['PatientID'] = 'UnknownID'
    try:
        metadata['SeriesNumber'] = ds.SeriesNumber  # series number
    except:
        metadata['SeriesNumber'] = 'Ser'
    try:
        metadata['InstanceNumber'] = ds.InstanceNumber
    except:
        metadata['InstanceNumber'] = 'Ins'
    return metadata

