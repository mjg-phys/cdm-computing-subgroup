# -*- coding: utf-8 -*-
# Name: package_test_script.py
# Authors: Stephan Meighen-Berger
# Basic script to test if the package is working

import matplotlib.pyplot as plt
import numpy as np

# Module import
from nu_isance import Nuisance, config

# A nusciance instance with options
config['oscillation']['matter'] = True
nuisance = Nuisance()

# Fetching the used grids
e_grid = config["oscillation"]["energy grid"]
cosZ = config["oscillation"]["angle grid"]
zenith = np.rad2deg(np.arccos(cosZ))

# ------------------------------------------------------------------------------
# Plotting
# ------------------------------------------------------------------------------
# Setup
_, axs = plt.subplots(1, 3, figsize=(12, 3), sharey=True)
# ------------------------------------------------------------------------------
# Grids
nu_e_e = nuisance.osc.oscillation_prob_e[0]
nu_e_mu = nuisance.osc.oscillation_prob_e[1]
nu_e_tau = nuisance.osc.oscillation_prob_e[2]
Xfine, Yfine = np.meshgrid(e_grid, cosZ)
# ------------------------------------------------------------------------------
# Nu_e -> Nu_e
axs[0].pcolormesh(
    Xfine, Yfine, nu_e_e,
    cmap='inferno_r', vmin=0, vmax=1
)
axs[0].set_xscale('log')
axs[0].set_xlim(min(e_grid), max(e_grid))
axs[0].set_xlabel(r'$E_\nu$ [GeV]')
axs[0].set_ylabel(r'$\cos\theta$')
axs[0].set_title(r'$\nu_e\rightarrow \nu_e$')
# ------------------------------------------------------------------------------
# Nu_e -> Nu_mu
axs[1].pcolormesh(
    Xfine, Yfine, nu_e_mu,
    cmap='inferno_r', vmin=0, vmax=1
)
axs[1].set_xscale('log')
axs[1].set_xlim(min(e_grid), max(e_grid))
axs[1].set_xlabel(r'$E_\nu$ [GeV]')
axs[1].set_title(r'$\nu_e\rightarrow \nu_\mu$')
# ------------------------------------------------------------------------------
# Nu_e -> Nu_tau
pc = axs[2].pcolormesh(
    Xfine, Yfine, nu_e_tau,
    cmap='inferno_r', vmin=0, vmax=1
)
axs[2].set_xscale('log')
axs[2].set_xlim(min(e_grid), max(e_grid))
axs[2].set_xlabel(r'$E_\nu$ [GeV]')
axs[2].set_title(r'$\nu_e\rightarrow \nu_\tau$')
# ------------------------------------------------------------------------------
# Color bar
plt.colorbar(pc)
# ------------------------------------------------------------------------------
# Saving
plt.tight_layout()
plt.savefig('../pics/package_test_plot.png', dpi=250)