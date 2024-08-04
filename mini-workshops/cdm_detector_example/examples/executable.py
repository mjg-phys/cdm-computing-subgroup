# imports
import numpy as np
import matplotlib.pyplot as plt
import sys
sys.path.append('../')

# Module
from detectorexample import DetectorExample, config


print("Initializing")
EventGenerator = DetectorExample()

print("Random seed")
rng = np.random.RandomState(1337)
# Generating events
spatial_samples_CC, timing_samples_CC, cuts_CC = EventGenerator.event_generator(
    EventGenerator._rates['NuE CC'][EventGenerator._e_cut[0]:EventGenerator._e_cut[1]],
    rng, 'CC'
)

spatial_samples_NC, timing_samples_NC, cuts_NC = EventGenerator.event_generator(
    (EventGenerator._rates['NuE NC'] + EventGenerator._rates['NuMu NC'])[EventGenerator._e_cut[0]:EventGenerator._e_cut[1]],
    rng, 'NC'
)

# Total counts
CC_counts = np.array([
    np.sum(cut_e) for cut_e in cuts_CC
])
NC_counts = np.array([
    np.sum(cut_e) for cut_e in cuts_NC
])

# Let's plot it
# -----------------------------------------------------------
# plot
fig, ax = plt.subplots(1, 1, figsize=(3,3))

ax.step(
    EventGenerator._energy_grid[10:22],
    EventGenerator._rates['NuE CC'][10:22],
    color='r',
    ls='-',
    label=r'$\nu_e$ CC'

)

ax.step(
    EventGenerator._energy_grid[10:22],
    CC_counts,
    color='r',
    ls=':',
    label=r'$\nu_e$ CC w/ cuts'

)

ax.step(
    EventGenerator._energy_grid[10:22],
    EventGenerator._rates['NuE NC'][10:22] + EventGenerator._rates['NuMu NC'][10:22],
    color='k',
    ls='-',
    label=r'NC'

)

ax.step(
    EventGenerator._energy_grid[10:22],
    NC_counts,
    color='k',
    ls=':',
    label=r'NC w/ cuts'

)

# ax.fill_betweenx([0, 1e5], 0, 1e0, color='k', alpha=0.2)
# -----------------------------------------------------------
# axis
ax.set_xlim(1e0, 1e1)
ax.set_ylim(1e0, 4e3)
ax.set_yscale('log')
ax.set_xscale('linear')
# -----------------------------------------------------------
# legend
ax.legend(frameon=False, ncols=2, loc=9, bbox_to_anchor=(0.5, 1.35))
# -----------------------------------------------------------
# labels
ax.set_xlabel(r"$E_\nu$ [GeV]")
ax.set_ylabel(r"Counts")
# ax.text(2e-1, 2, "Ignore", color='r')
ax.tick_params(axis='both', which='both', direction='in', right=True, top=True)
fig.tight_layout()
fig.savefig('atmospheric_flux.pdf', bbox_inches='tight', dpi=500)