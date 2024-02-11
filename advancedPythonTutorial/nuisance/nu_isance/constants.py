# -*- coding: utf-8 -*-
# constants.py
# Authors: Stephan Meighen-Berger
# Storage for basic constants

# imports
import numpy as np

m2GeV = 1 / (0.197 * 1e-15)
eV2GeV = 1e-9
rEarth = 6371  # in km
ratmos = 20 + rEarth  # in km

mdiff = np.array([1., 7.60e-5, 7.60e-5 + 2.35e-3]) * eV2GeV**2

earth_pot_nucraft =  4 * 1e-22  # In GeV^{-2} and this includes density

# Mixing angles
mixing_angles = np.array([
    [1, 2, np.arcsin(np.sqrt(0.307)) / np.pi * 180., 0.],  # 0.013
    [1, 3, np.arcsin(np.sqrt(0.0218)) / np.pi * 180., 0],  #  add cp violation here 0.0007
    [2, 3, np.arcsin(np.sqrt(0.512)) / np.pi * 180., 0.],  # 0.022
])

# Vearth can also be set to None for vacuum simulations
Vearth = np.diag([
        earth_pot_nucraft,
        0,
        0
    ])