# -*- coding: utf-8 -*-
# detector.py
# Detector Functions

#  simulation parameters

from ..constants import water_nucleons, molecules_per_cm3
import numpy as np

class Detector(object):
    """ detector class
    """
    def __init__(self, radius: float):
        """ initializes the class
        """
        self._radius = radius
        self._volume = 4 / 3 * np.pi * radius**3
        self._nTargets = molecules_per_cm3 * self._volume * water_nucleons

    @property
    def nTargets(self):
        return self._nTargets

    @property
    def volume(self):
        return self._volume

    @property
    def radius(self):
        return self._radius