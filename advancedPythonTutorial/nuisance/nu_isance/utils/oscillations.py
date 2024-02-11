# -*- coding: utf-8 -*-
# oscillations.py
# Authors: Stephan Meighen-Berger
# Simplified neutrino oscillations

# imports
import numpy as np
import numpy as np
from numba import njit

# module imports
from nu_isance.constants import m2GeV, mdiff, rEarth, ratmos

# Basic functions
@njit
def mass_diff_mat(i: int, j: int, matrix: np.array) -> float:
    """ Fetches the mass differences from the mass matrix

    Parameters
    ----------
    i,j: int
        Matter states to compare
    matrix: np.array
        The mass matrix

    Returns
    -------
    mass_diff: float
        The mass difference squared
    """
    if i == j:
        return 0
    states_ordered = np.sort(np.array([i, j]))  # Need the lowest number to be 1
    if states_ordered[0] == 0:
        return matrix[states_ordered[1], states_ordered[1]]
    else:
        return (
            matrix[states_ordered[1], states_ordered[1]] -
            matrix[states_ordered[0], states_ordered[0]]
        )

# oscillation length
@njit
def l_osc(i: int, j: int, E: float, mass_matrix: np.array) -> float:
    """ The oscillation length for the given flavor combination and energy

    Parameters
    ----------
    i,j: int
        The matter states
    E: float
        The neutrino energy
    mass_matrix: np.matrix
        The mass matrix

    Returns
    -------
    losc: float
        The oscillation length
    """
    return (
        4. * np.pi * E / mass_diff_mat(int(i), int(j), mass_matrix)
    )

@njit
def buildmassmatrix(params: np.array) -> np.ndarray:
    """ constructs the squared mass matrix from the input parameters

    Parameters
    ----------
    params: jax.numpy.array
        Array containing the mass parameters. These should be the orderd
        masses of the eigenstates, with the first value being the lightest mass
        and all others the squared mass difference

    Returns
    -------
    masssqrd: jax.numpy.array
        The squared diagonal mass matrix
    """
    assert -params[0]**2 <= min(params[1:]), "All masses have to be positive!"
    
    return np.diag(
        np.array([params[0]**2] + [params[0]**2 + m for m in params[1:]])
    )

# basis transform
@njit
def rotmatrix(dim: int, i: int, j: int, ang: float, cp: float) -> np.ndarray:
    """ constructs a (Gell-Mann) rotational matrix ij with angle ang
    and cp violating phase cp for symmetry i < j is required

    Parameters
    ----------
    dim: int
        Dimensions of the matrix
    i,j: int
        Positions of the matrix
    ang: float
        Angle of roration in radians
    cp: float
        CP violating phase

    Returns
    -------
    rotmat: jax.numpy.array
        The rotation matrix

    Raises
    ------
    DimensionError:
        The input dimensions dim, i, j are wrong
    """
    # Building
    R = np.eye(int(dim), dtype=np.complex128)
    R[i, j] = np.sin(ang) * np.exp(-1j * cp)
    R[j, i] = -np.sin(ang) * np.exp(1j * cp)
    R[i, i] = R[j, j] = np.cos(ang)
    return R

@njit
def buildmixingmatrix(params: np.ndarray, anti=1) -> np.ndarray:
    """ constructs the mixing matrix from the input parameters
    for symmetry i < j is required

    For CP-violating factors, use tuples like (i,j,theta_ij,delta_ij),
    with delta_ij in degrees.

    Parameters
    ----------
    params: jax.numpy.array
        tuples descriping the mixing matrix.
        The format of each tuple should be [i, j, theta_ij]
    anti: int
        Optional: +1 for neutrino and -1 for anti

    Returns
    -------
    mixing_matrix: jax.numpy.array
        The mixing matrix constructed in revers order.
        E.g. params = [(1,2,33.89),(1,3,9.12),(2,3,45.00)]
        => U = R_23 . R_13 . R_12
    """
    dim = max(np.array([par[1] for par in params]))
    U = np.eye(int(dim), dtype=np.complex128)
    # Applying the rotation matrices
    for par in params:
        U = np.dot(
            rotmatrix(int(dim), int(par[0] - 1), int(par[1] - 1),
                      np.deg2rad(par[2]), anti * np.deg2rad(par[3])), U)
    return U

@njit
def effective_matrices(
    mixing_angles: np.ndarray, mdiff: np.ndarray, matter: np.ndarray, anti=1):
    """ constructs the effective mixing and mass matrices

    Parameters
    ----------
    mixing_angles: np.ndarray
        The mixing angles
    mdif: np.ndarray
        The mass squared differences
    matter: np.ndarray
        The effective potential (times energy)
    anti: int
        Optional: +1 for neutrino and -1 for anti
    Returns
    -------
    Ueffective, Heffective, effective_h: np.ndarray
        The effective rotational and energy matrices,
        as well as the total matrix
    """
    mixing_matrix = buildmixingmatrix(mixing_angles, anti=anti)
    # need to create the effective hamiltonian and diagonalize
    mass_matrix = buildmassmatrix(mdiff)
    mixing_matrix = mixing_matrix.astype(np.complex128)
    mass_matrix = mass_matrix.astype(np.complex128)
    # TODO:
    # Make matter radius dependent
    effective_h = (
        mixing_matrix @ (mass_matrix @ mixing_matrix.conj().T) + anti * matter
    )
    U, H, _ = np.linalg.svd(effective_h) # Output in descending order for H
    n = len(H)
    H = np.diag(H[::-1])  # Sorts in decending order 
    U[:, :n] = U[:, n-1::-1]
    return U, H, effective_h

# Transition probability using plane waves
# Following arXiv:1206.0812v1
@njit
def wp_prob(
        alpha: int, beta: int, E: float, L: float,
        mixing_angles: np.ndarray, mass_states=3, matter=None, anti=1,
    ) -> np.ndarray:
    """ Oscillation probability using a WP approach.
    This is a modified version of the calculations
    shown in arXiv:1206.0812v1.

    Parameters
    ----------
    alpha: int
        Flavor state oscillating from
    beta: int
        Flavor state to oscillate to
    E: float
        Energy of the oscillating neutrino
    L: float
        Travel distance in km
    mixing_angles: np.array
        Mixing angles between the matter and flavor states (PMNS matrix)
    mass_states: int
        Optional: Number of mass states, this should agree with the mixing matrix
    matter: np.ndarray
        Optional: Effective potential in matrix form induced by the ambient matter
    anti: int
        Optional: +1 for neutrinos and -1 for anti neutrinos

    Returns
    -------
    oscillation_prob: float
        The oscillation probability
    """
    mixing_matrix = buildmixingmatrix(mixing_angles, anti=anti)
    first  = 0
    l_tmp = L * 1e3 * m2GeV
    # need to create the effective hamiltonian and diagonalize
    mass_matrix = buildmassmatrix(mdiff)
    if matter is None:
        U = mixing_matrix
        H = mass_matrix
    else:
        mixing_matrix = mixing_matrix.astype(np.complex128)
        mass_matrix = mass_matrix.astype(np.complex128)
        # TODO:
        # Make matter radius dependent
        effective_h = (
            mixing_matrix @ (mass_matrix @ mixing_matrix.conj().T) +
            anti * (matter.astype(np.complex128) * E)
        )
        U, H, _ = np.linalg.svd(effective_h) # Output in descending order for H
        n = len(H)
        H = np.diag(H[::-1])  # Sorts in decending order 
        U[:, :n] = U[:, n-1::-1]
    for j in range(mass_states):
        # First term
        first += (np.abs(U[alpha, j])**2) * (np.abs(U[beta, j])**2)
        second = 0
        for i in range(j):
            losc = l_osc(j, i, E, H)
            second += (
                U[alpha, i] * np.conj(U[alpha, j]) *
                np.conj(U[beta, i]) * U[beta, j] *
                np.exp(
                    -2*np.pi*1j * l_tmp / losc
                )
            )
        second = np.real(second)
        first += 2 * second  
    return first

# Transition probability using plane waves
# Following arXiv:1206.0812v1
@njit
def wp_prob_effective(
        alpha: int, beta: int, E: float, L: float,
        Ueffective: np.ndarray, Meffective: np.ndarray,
        mass_states=3
    ) -> np.ndarray:
    """ Oscillation probability using a WP approach.
    This is a modified version of the calculations
    shown in arXiv:1206.0812v1. This function takes the effective
    rotation and mass matrices

    Parameters
    ----------
    alpha: int
        Flavor state oscillating from
    beta: int
        Flavor state to oscillate to
    E: float
        Energy of the oscillating neutrino
    L: float
        Travel distance in km
    Ueffective: np.ndarray
        Effective PMNS matrix
    Meffective: np.ndarray
        Effective mass differences
    mass_states: int
        Optional: Number of mass states, this
        should agree with the mixing matrix

    Returns
    -------
    oscillation_prob: float
        The oscillation probability
    """
    first  = 0
    l_tmp = L * 1e3 * m2GeV
    # need to create the effective hamiltonian and diagonalize
    U = Ueffective
    H = Meffective
    for j in range(mass_states):
        # First term
        first += (np.abs(U[alpha, j])**2) * (np.abs(U[beta, j])**2)
        second = 0
        for i in range(j):
            losc = l_osc(j, i, E, H)
            second += (
                U[alpha, i] * np.conj(U[alpha, j]) *
                np.conj(U[beta, i]) * U[beta, j] *
                np.exp(
                    -2*np.pi*1j * l_tmp / losc
                )
            )
        second = np.real(second)
        first += 2*second  
    return first

@njit
def oscillation_calc_func(
        org_flavor: int, e_grid: np.ndarray, zenith: float,
        mixing_angles: np.ndarray, mass_states=3, matter=None, anti=1
    )->np.ndarray:
    """ temporary function for the calculation loop

    Parameters
    ----------
    org_flavor: int
        Flavor state oscillating from
    e_grid: np.ndarray
        Energy of the oscillating neutrino
    zenith: float
        injection angle in radians
    mixing_angles: np.ndarray
        PMNS matrix
    mass_states: int
        Optional: Number of mass states,
        this should agree with the mixing matrix
    matter: np.ndarray or None
        Optional: The effective matter potential
    anti: int
        Optional: +1 for neutrinos and -1 for anti neutrinos

    Returns
    -------
    oscillation_probs: (np.ndarray, np.ndarray, np.ndarray)
        The oscillation probabilities to the different SM flavor states
    """
    distance = np.sqrt(
        ratmos * ratmos + rEarth*rEarth -
        2 * ratmos * rEarth * np.cos(
            zenith - np.arcsin(np.sin(np.pi-zenith) / ratmos * rEarth)
        )
    )
    probs_1 = np.array([
        wp_prob(
            org_flavor, 0, E, distance, mixing_angles, mass_states=mass_states,
            matter=matter, anti=anti)
        for E in e_grid
    ])
    probs_2 = np.array([
        wp_prob(
            org_flavor, 1, E, distance, mixing_angles, mass_states=mass_states,
            matter=matter, anti=anti)
        for E in e_grid
    ])
    probs_3 = np.array([
        wp_prob(
            org_flavor, 2, E, distance, mixing_angles, mass_states=mass_states,
            matter=matter, anti=anti)
        for E in e_grid
    ])
    return probs_1, probs_2, probs_3

@njit
def oscillation_calc_func_effective(
        org_flavor: int, e_grid: np.ndarray, zenith: float,
        Ueffective: np.ndarray, Meffective: np.ndarray, mass_states=3
    ):
    """ temporary function for the calculation loop.
    This uses the pre-calculated effective matrices

    Parameters
    ----------
    org_flavor: int
        Flavor state oscillating from
    e_grid: np.ndarray
        Energy of the oscillating neutrino
    zenith: float
        injection angle in radians
    Ueffective: np.ndarray
        effective PMNS matrix
    Meffective: np.ndarray
        effective mass matrix
    mass_states: int
        Optional: Number of mass states,
        this should agree with the mixing matrix

    Returns
    -------
    oscillation_probs: (np.ndarray, np.ndarray, np.ndarray)
        The oscillation probabilities to the different SM flavor states
    """
    distance = np.sqrt(
        ratmos * ratmos + rEarth*rEarth -
        2 * ratmos * rEarth * np.cos(
            zenith - np.arcsin(np.sin(np.pi-zenith)/ratmos*rEarth)
        )
    )
    probs_1 = np.array([
        wp_prob_effective(
            org_flavor, 0, E, distance, Ueffective, Meffective,
            mass_states=mass_states
        ) for E in e_grid
    ])
    probs_2 = np.array([
        wp_prob_effective(
            org_flavor, 1, E, distance, Ueffective, Meffective,
            mass_states=mass_states
        ) for E in e_grid
    ])
    probs_3 = np.array([
        wp_prob_effective(
            org_flavor, 2, E, distance, Ueffective, Meffective,
            mass_states=mass_states
        ) for E in e_grid
    ])
    return probs_1, probs_2, probs_3