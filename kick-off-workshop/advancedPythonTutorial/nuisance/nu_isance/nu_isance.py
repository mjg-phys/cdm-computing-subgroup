# -*- coding: utf-8 -*-
# Name: nu_isance.py
# Authors: Stephan Meighen-Berger
# Quick and dirty code to extrapolate neutrino fluxes

# Native modules
import logging
from typing import Union
from  time import time
import numpy as np
import sys
import yaml

# Package modules
# ---------------------------
from .config import config
from .nu_oscillations import NuOsc


# unless we put this class in __init__, __name__ will be nuisance.nuisance
_log = logging.getLogger("")

# TODO: Make this an option in the config!
# Suppressing the numba logger
numba_logger = logging.getLogger('numba')
numba_logger.setLevel(logging.WARNING)

matplotlib_logger = logging.getLogger('matplotlib')
matplotlib_logger.setLevel(logging.WARNING)


class Nuisance(object):
    """ the Nuisance class. This object is the interface to the
    nuisance package
    """
    def __init__(
        self,
        userconfig: Union[None, dict, str]=None
    ) -> None:
        """Initializes the nuisance class
        params
        ------
        userconfig: Configuration dictionary or
        path to yaml file which specifies configuration

        raises
        ------
        """
        start = time()
        # The config
        if userconfig is not None:
            if isinstance(userconfig, dict):
                config.from_dict(userconfig)
            else:
                config.from_yaml(userconfig)

        # Create RandomState
        if config["general"]["random state seed"] is None:
            _log.warning("No random state seed given, constructing new state")
            rstate = np.random.RandomState()
        else:
            rstate = np.random.RandomState(
                config["general"]["random state seed"]
            )
        config["runtime"] = {"random state": rstate}

        # Logger
        # Logging formatter
        fmt = "%(levelname)s: %(message)s"
        fmt_with_name = "[%(name)s] " + fmt
        formatter_with_name = logging.Formatter(fmt=fmt_with_name)
        # creating file handler with debug messages
        if config["general"]["enable logging"]:
            fh = logging.FileHandler(
                config["general"]["log file handler"], mode="w"
            )
            fh.setLevel(logging.DEBUG)
            fh.setFormatter(formatter_with_name)
            _log.addHandler(fh)
        else:
            _log.disabled = True
        # console logger with a higher log level
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(config["general"]["debug level"])
        # add class name to ch only when debugging
        if config["general"]["debug level"] == logging.DEBUG:
            ch.setFormatter(formatter_with_name)
        else:
            formatter = logging.Formatter(fmt=fmt)
            ch.setFormatter(formatter)
        _log.addHandler(ch)
        _log.setLevel(logging.DEBUG)
        _log.info("Starting")
        _log.info("Welcome to nuisance. I'm here to help")
        self.osc = NuOsc()
        _log.info("Setup took %.f seconds" % (start - time()))

    def close(self):
        """ Wraps up the program
        Parameters
        ----------
        None
        Returns
        -------
        None
        """
        _log.info('---------------------------------------------------')
        _log.info('---------------------------------------------------')
        # A new simulation
        if config["general"]["enable logging"]:
            _log.debug(
                "Dumping run settings into %s",
                config["general"]["config location"],
            )
            with open(config["general"]["config location"], "w") as f:
                yaml.dump(config, f)
            _log.debug("Finished dump")
            _log.info("................................................................................")
            _log.info("................................................................................")
            _log.info(".......................................#@@@@@@#,................................")
            _log.info("............................*@@/ ....... ...@@@*****,... @@.....................")
            _log.info("........................@..***********************@@*******...#@................")
            _log.info(".....................@******%@@( . . . . ..@@@********@********.  %.............")
            _log.info("...................@****@....... ............... /@*****@*********.@............")
            _log.info(".................@***@.. ....... ....... ....... ....@***@*********.@...........")
            _log.info(".................**@...(((((.... .........((((.. .....@***@*********@...........")
            _log.info("................@**.(((((&#((...&&&& ...((&((((((((. ..@**//********/.@(........")
            _log.info("................&**@((((((((.... ........((((&#(((((((.@**@**********@**,/......")
            _log.info("................@@*@&((. .......,&&&.... .......((((((@***@**********@***@......")
            _log.info("...............@**@**@/......... ............... ..(@%**@@*,*******/*@@@@.......")
            _log.info("............@ ******@***@@                      .@@***@(**************@.........")
            _log.info("..........@@@  @@@*****@*****(@@@@/.....%@@@@******@@@ @,************@..........")
            _log.info("...........@@   @@@@@@.....@@&****************@@#..@ .@  @  (/***(@(............")
            _log.info("........................................................@ @.....................")
            _log.info("................................................................................")
            _log.info("Bye!")
        # Closing log
        logging.shutdown()
