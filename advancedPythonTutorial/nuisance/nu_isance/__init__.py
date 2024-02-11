    # -*- coding: utf-8 -*-

from .nu_isance import Nuisance
from .config import config
from .errors import __init__
from .nu_oscillations import __init__
from .utils import __init__

__all__ = (Nuisance, config)

# Version of the nuisance package
__version__ = "1.0.2"
__author__ = "Stephan Meighen-Berger"