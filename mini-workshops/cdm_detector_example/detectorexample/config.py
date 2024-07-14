# -*- coding: utf-8 -*-
# Name: config.py
# Copyright (C) 2024 Stephan Meighen-Berger
# Config file for the pr_dformat package.

from typing import Dict, Any
import numpy as np
import yaml

_baseconfig: Dict[str, Any]

_baseconfig = {
    ###########################################################################
    # General inputs
    ###########################################################################
    "general": {
        # Random state seed
        "version": "github"
    },
    ###########################################################################
    # Scenario input
    ###########################################################################
    "run": {
        "seed": 1337,
        "time": 10  # in years
    },
    ###########################################################################
    # Model
    ###########################################################################
    "model": {
        "model": "mceq",
        "mceq storage": '../data/'
    },
    ###########################################################################
    # Injection
    ###########################################################################
    "injection": {
        "cross section": 1e-38,  # scale of the cross section
    },
    ###########################################################################
    # Detector
    ###########################################################################
    "detector": {
        "radius": 10 * 1e2,  # in cm
    },
    ###########################################################################
    # Propagation
    ###########################################################################
    "propagation": {
        "photon cut": 100,  # minimal number of photons per cm required
    },
    ###########################################################################
    # Analysis  This is just for convenience!
    ###########################################################################
    "analysis": {
        "energy cuts": [10, 22],
    },
    ###########################################################################
    # Advanced (no touching without understanding the code!)
    ###########################################################################
    "advanced": {
        "energy bins": np.logspace(np.log10(0.07943282347242814), 11, 122),
        # TODO: This needs to become dependent on the refractive index
        "z grid": np.linspace(0, 1e4, int(1e4 / 23)),  # Weird number due to speed of light in water and timing used later
        "wavelengths": np.linspace(350., 500., 100),  # in nm
        "ns grid": np.linspace(0, 100, 101)  # Pulse shape grid
    }
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
