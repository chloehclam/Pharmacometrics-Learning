# import necessary libraries
import numpy as np


"""
    Calculate the concentration required to produce a desired effect using
    the Emax model.

    The model is E = e0 + (emax * concentration) / (ec50 + concentration).

    Parameters
    ----------
    effect : float or array-like
        Desired effect value or values.
    emax : float
        Maximum effect above the baseline.
    ec50 : float
        Concentration producing half of the maximum effect. The returned
        concentration uses the same units as ``ec50``.
    e0 : float
        Baseline effect.

    Returns
    -------
    float or numpy.ndarray
        Concentration value or values corresponding to ``effect``.

    Raises
    ------
    ValueError
        If any requested effect is below ``e0`` or above ``e0 + emax``.

    Notes
    -----
    The maximum effect, ``e0 + emax``, is approached asymptotically. The
    current function accepts that boundary in its validation, but its
    calculation divides by zero there.
    """

def concentration_for_effect(effect, emax, ec50, e0):
        # Ensure that the desired effect is within the achievable range
        if np.any(effect < e0) or np.any(effect > emax + e0):
            raise ValueError("Desired effect must be between e0 and emax + e0.")

        # Calculate the required concentration using the rearranged Emax equation
        concentration = (ec50 * (effect - e0)) / (emax + e0 - effect)

        return concentration
