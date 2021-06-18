#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun  5 15:55:12 2021

@author: yukuo
"""

import test_version
import pathlib
import time

if __name__ == "__main__":
    start = time.time()
    test_bank = pathlib.Path(r'E:')
    test_version.dicom2png(test_bank)
    duration = time.time()-start