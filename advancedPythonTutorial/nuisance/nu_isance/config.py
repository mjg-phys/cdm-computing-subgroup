# -*- coding: utf-8 -*-
# Name: config.py
# Authors: Stephan Meighen-Berger
# Config file for the nuisance package.

import logging
from typing import Dict, Any
import yaml
import numpy as np

_baseconfig: Dict[str, Any]

_baseconfig = {
    ###########################################################################
    # General inputs
    ###########################################################################
    "general": {
        # Random state seed
        "random state seed": 1337,
        # Enable logger and config dump
        "enable logging": True,
        # Output level
        'debug level': logging.INFO,
        # Note the paths need to be set appropiately for your system
        # Location of logging file handler
        "log file handler": "nuisance.log",
        # Dump experiment config to this location
        "config location": "nuisance.txt",
    },
    ###########################################################################
    # Oscillation setup
    ###########################################################################
    "oscillation": {
        # If to use pre-calculated grids
        "precalc": False,
        "energy grid": np.logspace(-2, 2, 1000),
        "angle grid": np.linspace(-1, 1., 400),
        "matter": True,
    },
}


class ConfigClass(dict):
    """ The configuration class. This is used
    by the package for all parameter settings. If something goes wrong
    its usually here.
    Parameters
    ----------
    config : dic
        The config dictionary
    Returns
    -------
    None
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    # TODO: Update this
    def from_yaml(self, yaml_file: str) -> None:
        """ Update config with yaml file
        Parameters
        ----------
        yaml_file : str
            path to yaml file
        Returns
        -------
        None
        """
        yaml_config = yaml.load(open(yaml_file), Loader=yaml.SafeLoader)
        self.update(yaml_config)

    # TODO: Update this
    def from_dict(self, user_dict: Dict[Any, Any]) -> None:
        """ Creates a config from dictionary
        Parameters
        ----------
        user_dict : dic
            The user dictionary
        Returns
        -------
        None
        """
        self.update(user_dict)


config = ConfigClass(_baseconfig)