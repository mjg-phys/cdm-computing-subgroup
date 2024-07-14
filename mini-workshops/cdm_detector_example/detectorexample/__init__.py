# -*- coding: utf-8 -*-

from .config import config
from .model import __init__
from .detector import __init__
from .injection import __init__
from .utils import __init__
from .constants import __init__
from .propagation import __init__
from .detectorexample import DetectorExample

__all__ = (DetectorExample, config)
__version__ = '0.0.1'
__author__ = "Stephan Meighen-Berger"
