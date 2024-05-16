# -*- coding: utf-8 -*-
# nu_oscillations.py
# Authors: Stephan Meighen-Berger
# Constructs the oscillation grids

# imports
import logging
import numpy as np
from tqdm import tqdm

# module import
from ..config import config
from ..errors import UnphysicalError, NotImplementedError
from ..utils import oscillation_calc_func
from ..constants import mixing_angles, Vearth

_log = logging.getLogger(__name__)

class NuOsc(object):
    """ class containing and building neutrino oscillation grids
    """
    def __init__(self):
        """ initializes the NuOsc object 
        """
        conf_pars = config["oscillation"]
        # TODO: Add a switch here to save calculation time
        if conf_pars['precalc']:
            raise NotImplementedError(
                "This options has not been implemented as of yet"
            )
        else:
            matter = 0
            if conf_pars['matter']:
                _log.info("Propagating through matter")
                matter = Vearth
            else:
                _log.info("Propagating through vacuum")
                matter is None
            self._oscillation_grid_constructor(
                conf_pars['energy grid'], conf_pars['angle grid'],
                mixing_angles, matter, anti=1
            )

    @property
    def oscillation_prob_e(self) -> np.ndarray:
        """ the oscillation probabilities of nu_e
        """
        return self._result_e
    
    @property
    def oscillation_prob_mu(self) -> np.ndarray:
        """ the oscillation probabilities of nu_mu
        """
        return self._result_mu
    
    @property
    def oscillation_prob_tau(self) -> np.ndarray:
        """ the oscillation probabilities of nu_tau
        """
        return self._result_tau

    def _oscillation_grid_constructor(
            self,
            e_grid: np.ndarray, cosZ: np.ndarray, mixing_angles: np.ndarray,
            matter: np.ndarray, anti: int
        )->np.ndarray:
        """ constructs the oscillation grids (e, mu, tau)

        Parameters
        ----------
        e_grid: np.ndarray
            Energy of the oscillating neutrino
        zenith: float
            injection angle in radians
        mixing_angles: np.ndarray
            PMNS matrix
        matter: np.ndarray or None
            Optional: The effective matter potential
        anti: int
            Optional: +1 for neutrinos and -1 for anti neutrinos

        Returns
        -------
        oscillation_probs: (np.ndarray, np.ndarray, np.ndarray)
            The oscillation probabilities to the different SM flavor states
        """
        if anti not in [1, -1]:
            raise UnphysicalError(
                "The parameters anti is set to %d." %anti +
                " It has to be either 1 or -1!"
            )
        _log.info("Building the oscillation grids")
        _log.info("Using %d as the anti setting" %anti)
        _log.info("For nu_e...")
        probs_1_tmp = []
        probs_2_tmp = []
        probs_3_tmp = []
        for zenith in tqdm(np.arccos(cosZ)):
            probs_1, probs_2, probs_3 = oscillation_calc_func(
                0, e_grid, zenith, mixing_angles, mass_states=3,
                matter=matter, anti=anti
            )
            probs_1_tmp.append(probs_1)
            probs_2_tmp.append(probs_2)
            probs_3_tmp.append(probs_3)
        probs_1_tmp = np.array(probs_1_tmp)
        probs_2_tmp = np.array(probs_2_tmp)
        probs_3_tmp = np.array(probs_3_tmp)
        self._result_e = (probs_1_tmp, probs_2_tmp, probs_3_tmp)
        self._result_e = np.copy(self._result_e)
        _log.info("Done!")
        _log.info("For nu_mu...")
        probs_1_tmp = []
        probs_2_tmp = []
        probs_3_tmp = []
        for zenith in tqdm(np.arccos(cosZ)):
            probs_1, probs_2, probs_3 = oscillation_calc_func(
                1, e_grid, zenith, mixing_angles, mass_states=3,
                matter=matter, anti=anti
            )
            probs_1_tmp.append(probs_1)
            probs_2_tmp.append(probs_2)
            probs_3_tmp.append(probs_3)
        probs_1_tmp = np.array(probs_1_tmp)
        probs_2_tmp = np.array(probs_2_tmp)
        probs_3_tmp = np.array(probs_3_tmp)
        self._result_mu = (probs_1_tmp, probs_2_tmp, probs_3_tmp)
        self._result_mu = np.copy(self._result_mu)
        _log.info("Done!")
        _log.info("For nu_tau...")
        probs_1_tmp = []
        probs_2_tmp = []
        probs_3_tmp = []
        for zenith in tqdm(np.arccos(cosZ)):
            probs_1, probs_2, probs_3 = oscillation_calc_func(
                2, e_grid, zenith, mixing_angles, mass_states=3,
                matter=matter, anti=anti
            )
            probs_1_tmp.append(probs_1)
            probs_2_tmp.append(probs_2)
            probs_3_tmp.append(probs_3)
        probs_1_tmp = np.array(probs_1_tmp)
        probs_2_tmp = np.array(probs_2_tmp)
        probs_3_tmp = np.array(probs_3_tmp)
        self._result_tau = (probs_1_tmp, probs_2_tmp, probs_3_tmp)
        self._result_tau = np.copy(self._result_tau)
        _log.info("Done!")
