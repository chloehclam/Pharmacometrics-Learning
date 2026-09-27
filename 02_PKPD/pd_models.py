import numpy as np
import pandas as pd


def emax_model(
    concentration,
    emax,
    ec50,
    e0=0
):
    effect = e0 + (emax * concentration) / (ec50 + concentration)

    return effect


def inhibitory_emax_model(
    concentration,
    imax,
    ic50,
    e0
):
    effect = e0 - (imax * concentration) / (ic50 + concentration)

    return effect



def simulate_emax_curve(
    target_concentrations,
    emax,
    ec50,
    e0=0,
    n_points=300,
    padding=1.1,
):
    """Generate an Emax concentration-effect curve spanning the target concentrations."""
    target_concentrations = np.asarray(list(target_concentrations), dtype=float)

    if target_concentrations.size == 0:
        raise ValueError("Provide at least one target concentration.")
    if np.any(target_concentrations < 0):
        raise ValueError("Target concentrations must be non-negative.")
    if n_points < 2:
        raise ValueError("n_points must be at least 2.")
    if padding <= 0:
        raise ValueError("padding must be positive.")

    max_concentration = target_concentrations.max() * padding
    concentrations = np.linspace(0, max_concentration, n_points)
    effects = emax_model(concentrations, emax=emax, ec50=ec50, e0=e0)

    return pd.DataFrame({
        "Concentration (mg/L)": concentrations,
        "Effect": effects,
    })