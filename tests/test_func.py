# -*- coding: utf-8 -*-
"""
Created on Fri Jun 18 01:10:19 2021

@author: user
"""

from pathlib import Path
import os
import pydicom


import concurrent.futures
from multiprocessing import Manager

from pathlib import Path
import os



def test(file_path, patient_dict):
    try:
        ds = pydicom.dcmread(file_path)
        p = ds.Modality
    except Exception as e:
        p = 'error'
    if p in patient_dict:
        patient_dict[p] +=1
    else:
        patient_dict[p] = 0

#     print(patient_dict)
    #patient_dict[ds.Modality]+=1

    

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
        # root folder
        root_folder = origin.parent
    return root_folder, dicom_file_list

if __name__ == '__main__':
    fl = get_root_get_dicom_file_list(r"E:")[1]
    
    # import test_func
    with Manager() as manager:
    #manager = Manager()
    #patient_dict = manager.dict()    
        with concurrent.futures.ProcessPoolExecutor() as executor:        
            patient_dict = manager.dict({})
            [executor.submit(test, file_path, patient_dict) for file_path in fl]
        print(patient_dict)
    
    