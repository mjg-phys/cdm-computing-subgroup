# -*- coding: utf-8 -*-
# flux_model.py
# Authors: Stephan Meighen-Berger
# Basic primary and neutrino flux models

# imports
import pickle as pkl


def neutrino_fluxes(path_to_data: str) -> list:
    """ Fetches pre-calculated neutrino flux tables based on MCEq

    https://github.com/mceq-project/MCEq

    Parameters
    ----------
    path_to_data: str
        Path to data files

    Returns
    -------
    fluxes: list
        list of dictionaries [numu, nue], where each dictionary contains pre-calculated neutrino fluxes for
        locations, primary and interaction models, and zenith angles.
    """
    with open(path_to_data + 'mceq_numu_grid.pkl', 'rb') as handle:
        numu_dict = pkl.load(handle)

    with open(path_to_data + 'mceq_nue_grid.pkl', 'rb') as handle:
        nue_dict = pkl.load(handle)

    return [numu_dict, nue_dict]
