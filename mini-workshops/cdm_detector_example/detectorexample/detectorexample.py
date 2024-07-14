# -*- coding: utf-8 -*-
# detectorexample.py
# Copyright (C) 2024 Stephan Meighen-Berger,
# Interface class to the package

# imports
import numpy as np
from typing import Union
from tqdm.auto import tqdm
from scipy.ndimage import gaussian_filter

# Module imports
from .config import config
from .detector import Detector
from .constants import year, c_water
from .model import neutrino_fluxes
from .injection import cross_section_CC, cross_section_NC
from .propagation import light_production


class DetectorExample(object):
    """Class for unifying injection, energy loss calculation, and photon propagation"""
    def __init__(
        self,
        userconfig: Union[None, dict, str] = None,
    ) -> None:
        """Initializes the DetectorExample class

        params
        ______
        userconfig: Configuration dictionary or path to yaml file 
            which specifies configuration

        raises
        ______

        """
        if userconfig is not None:
            if isinstance(userconfig, dict):
                config.from_dict(userconfig)
            else:
                config.from_yaml(userconfig)
        
        print("Setting up the seed")
        self._rng = np.random.RandomState(config["run"]["seed"])
        print("Random Parameters")
        self._t = config['run']['time'] * year
        print("Setting up the detector")
        self._det = Detector(config['detector']['radius'])
        self._detector_factor = self._det.nTargets * self._t * np.pi * 4
        print("Setting up the neutrino flux")
        fluxes = neutrino_fluxes(config["model"]["mceq storage"])
        self._numu = fluxes[0]
        self._nue = fluxes[1]
        self._energy_bins = config['advanced']["energy bins"]
        self._energy_grid = np.sqrt(self._energy_bins[1:] * self._energy_bins[:-1])
        self._energy_widths = (self._energy_bins[1:] + self._energy_bins[:-1]) / 2
        self._z_grid = config['advanced']["z grid"]
        self._wavelengths = config['advanced']['wavelengths']
        self._photon_cut = config["propagation"]['photon cut']
        self._ns_grid = config['advanced']['ns grid']
        print("Preliminary rates")
        self._rates = {
            "NuMu NC": self._detector_factor * self._numu * cross_section_NC(self._energy_grid) * self._energy_widths,
            "NuE CC": self._detector_factor * self._nue * cross_section_CC(self._energy_grid) * self._energy_widths,
            "NuE NC": self._detector_factor * self._nue * cross_section_NC(self._energy_grid) * self._energy_widths
        }
        self._em_lengths, self._had_lengths, self._em_photons, self._had_photons = (
            light_production(self._z_grid, self._wavelengths, self._energy_grid, photon_cut=self._photon_cut)
        )
        self._e_cut = config['analysis']['energy cuts']


    # Sampling function for the interaction
    def _spatial_sampling(self, nsamples: int, detector_radius: float, rng: np.random.RandomState) -> np.ndarray:
        """ generates an event sample

        Parameters
        ----------
        nsamples: int
            Number of samples
        detector_radius: float
            The radius of the detector
        rng: np.random.RandomState
            The random state generator

        Returns
        -------
        rsamples: np.ndarray
            Sampled radius
        phi_samples: np.ndarray
            Sampled phi (interaction point and outgoing)
        theta_samples: np.ndarray
            Sampled theta (interaction point and outgoing)
        """
        radius_samples = rng.uniform(0, detector_radius, size=nsamples)
        phi_samples = rng.uniform(0., 360., size=(nsamples, 2))
        theta_samples = rng.uniform(0., 180., size=(nsamples, 2))
        return radius_samples, phi_samples, theta_samples

    ns_bins = np.linspace(0, 100, 101)

    def event_generator(
            self,
            nsamples: np.ndarray,
            rng: np.random.RandomState,
            type='CC') -> np.ndarray:
        """ generates particle events within the detector
        """
        # Spatial generation
        spatial_samples = []
        for nsamp in nsamples:
            spatial_samples.append(
                self._spatial_sampling(int(nsamp), self._det.radius, rng)
            )
        
        if type == 'CC':
            lengths = self._em_lengths[self._e_cut[0]:self._e_cut[1]]
            distro = self._em_photons[self._e_cut[0]:self._e_cut[1]]
        else:
            lengths = self._had_lengths[self._e_cut[0]:self._e_cut[1]]
            distro = self._had_photons[self._e_cut[0]:self._e_cut[1]]
        spatial_cuts = []
        timing_arr = []
        for idE, spatial_sample in enumerate(spatial_samples):
            rsampl, phisamp, thetasampl = spatial_sample
            X_int = rsampl * np.sin(phisamp[:, 0]) * np.cos(thetasampl[:, 0])
            Y_int = rsampl * np.sin(phisamp[:, 0]) * np.sin(thetasampl[:, 0])
            Z_int = rsampl * np.cos(phisamp[:, 0])
            arrow_scale = lengths[idE]
            X_dir = arrow_scale * np.sin(phisamp[:, 1]) * np.cos(thetasampl[:, 1])
            Y_dir = arrow_scale * np.sin(phisamp[:, 1]) * np.sin(thetasampl[:, 1])
            Z_dir = arrow_scale * np.cos(phisamp[:, 1])
            # Spatial Cuts
            event_r = np.sqrt(
                (X_int + X_dir)**2 +
                (Y_int + Y_dir)**2 +
                (Z_int + Z_dir)**2
            )
            event_cut = event_r < self._det.radius
            spatial_cuts.append(event_cut)
            # Timing
            energy_sample = []
            for idS, _ in enumerate(X_int):
                hits_binned, _ = np.histogram(
                    ((np.abs(event_r[idS] - self._det.radius) + self._z_grid) / c_water) * 1e9,
                    bins=self._ns_grid, weights=distro[idE]
                )
                energy_sample.append(gaussian_filter(hits_binned, sigma=2, radius=10))
            timing_arr.append(energy_sample)
        spatial_cuts = np.array(spatial_cuts, dtype=object)
        return spatial_samples, np.array(timing_arr, dtype=object), spatial_cuts

    # -------------------------------------------------------------------------------------------
    # Some basic analysis scripts for convenience
    # Analysis
    def _tail_vs_start(self, pulses: np.ndarray) -> np.ndarray:
        """ takes an array of pulses and checks their likelihood of being a CC event
        """
        idmaxes = np.argmax(pulses, axis=1)
        ratio_arr = np.array([
            np.sum(pulses[idTest][idmaxes[idTest]+1:]) /
            np.sum(pulses[idTest][:idmaxes[idTest]+1])
            for idTest in range(len(pulses))
        ])
        return ratio_arr

    def _data_TvsS_test(self, all_pulses: np.ndarray, cuts:np.ndarray) -> np.ndarray:
        """ helper function to apply analysis to the entire set
        """
        ratio_energy_bins = []
        for idE, energy_bin in enumerate(all_pulses):
            tmp_pulses = np.array(energy_bin)[cuts[idE]]
            ratio_energy_bins.append(self._tail_vs_start(tmp_pulses))
        return np.concatenate(np.array(ratio_energy_bins, dtype=object))

    def _data_TvsS_cut(self, all_pulses: np.ndarray, cuts:np.ndarray, TvsS_cut: float) -> np.ndarray:
        """ helper function to apply analysis cuts to the entire set
        """
        tmp_bool = []
        for idE, energy_bin in enumerate(all_pulses):
            tmp_pulses = np.array(energy_bin)[cuts[idE]]
            tmp_bool.append(np.less(self._tail_vs_start(tmp_pulses), TvsS_cut))
        return np.array(tmp_bool, dtype=object)

    def _analysis_simulation(self, nTrials: int, signal: np.ndarray, background: np.ndarray, seed=1337) -> np.ndarray:
        """ entire analysis multiple times
        """
        totals_CC_pre = []
        totals_NC_pre = []
        totals_CC = []
        totals_NC = []
        rng_trial = np.random.RandomState(seed)
        # Offloading some random number work before loop
        signal_sets = rng_trial.poisson(signal[self._e_cut[0]:self._e_cut[1]], size=(nTrials, len(signal[self._e_cut[0]:self._e_cut[1]])))
        background_sets = rng_trial.poisson(background[self._e_cut[0]:self._e_cut[1]], size=(nTrials, len(signal[self._e_cut[0]:self._e_cut[1]])))
        for set in tqdm(range(nTrials)):
            _, timing_samples_CC, cuts_CC = self.event_generator(
                signal_sets[set],  # Sampling the events as well!
                rng_trial,
                type='CC'
            )
            _, timing_samples_NC, cuts_NC = self.event_generator(
                background_sets[set],
                rng_trial,
                type='NC'
            )
            CC_counts = np.array([
                np.sum(cut_e) for cut_e in cuts_CC
            ])
            NC_counts = np.array([
                np.sum(cut_e) for cut_e in cuts_NC
            ])
            cc_cut_set = self._data_TvsS_cut(timing_samples_CC, cuts_CC, 1.5023693639498166)
            nc_cut_set = self._data_TvsS_cut(timing_samples_NC, cuts_NC, 1.5023693639498166)

            # Sum didn't work
            cc_cut_counts = np.array([
                np.sum(elem) for elem in cc_cut_set
            ])
            nc_cut_counts = np.array([
                np.sum(elem) for elem in nc_cut_set
            ])
            totals_CC_pre.append(np.sum(CC_counts))
            totals_NC_pre.append(np.sum(NC_counts))
            totals_CC.append(np.sum(cc_cut_counts))
            totals_NC.append(np.sum(nc_cut_counts))
        return np.array([
            totals_NC, totals_NC_pre,
            totals_CC, totals_CC_pre,
        ])

    def _example_analysis(self, nTrials):
        return self._analysis_simulation(
            nTrials,
            self._rates['NuE CC'],
            (self._rates['NuE NC'] + self._rates['NuMu NC'])
        )