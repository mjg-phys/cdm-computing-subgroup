# -*- coding: utf-8 -*-
# injection.py
# Authors: Stephan Meighen-Berger
# Basic injection models

import numpy as np

def cross_section_CC(E: np.ndarray, scale=1e-38) -> np.ndarray:
    """ Oversimplified neutrino cross section

    Parameters
    ----------
    E: np.ndarray
        The energies of interest in GeV

    scale: float
        Optional: The scale of the cross section at 1 GeV
    """
    return scale * np.sqrt(E)

def cross_section_NC(E: np.ndarray, scale=1e-38) -> np.ndarray:
    """ Oversimplified neutrino cross section

    Parameters
    ----------
    E: np.ndarray
        The energies of interest in GeV

    scale: float
        Optional: The scale of the cross section at 1 GeV
    """
    return cross_section_CC(E, scale=scale) * 1./3.