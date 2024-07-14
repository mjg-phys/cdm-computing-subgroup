# -*- coding: utf-8 -*-
# array_manipulations.py
# Authors: Stephan Meighen-Berger
# Basic propagation and light production

import numpy as np

def find_nearest(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx