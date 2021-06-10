#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 15:55:12 2021

@author: yukuo
"""

import test_version
import pathlib

test_bank = pathlib.Path(r'C:\Users\user\Desktop\dcm_test_bank')

test_version.dicom2jpg(test_bank)