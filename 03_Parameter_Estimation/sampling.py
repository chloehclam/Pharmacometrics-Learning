import numpy as np
import pandas as pd

def sample_at_time(
        df,
        sample_times=None,
        conc="Concentration (mg/L)"
):
    """
    Sample the concentration data at specified time points.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing Time and Concentration columns.
    sample_times : list or numpy.ndarray, optional
        List or array of time points at which to sample the concentration data.
        If None, the function will return the original DataFrame.
    conc: str, optional
        Name of the concentration column.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing sampled Time and Concentration columns.
    """
    # If no sample times are provided, return the original DataFrame
    if sample_times is None:
        return df

    # Ensure sample timepoints is ordered as a numpy array for easier indexing
    sample_times = np.array(sample_times, dtype=float)

    available_times = df["Time (hr)"].to_numpy()
    concentrations = df[conc].to_numpy()

    # Raise ValueError if a requested time is out of range
    if np.any(sample_times < available_times.min()) or \
       np.any(sample_times > available_times.max()):
        raise ValueError(
            "Requested sampling times must fall within "
            "the simulation time range."
        )

    # interpolate concentrations for sample times between two available times
    sampled_concentrations = np.interp(
        sample_times,
        available_times,
        concentrations
    )

    sampled_df = pd.DataFrame({
        "Time (hr)": sample_times,
        conc: sampled_concentrations
    })

    return sampled_df