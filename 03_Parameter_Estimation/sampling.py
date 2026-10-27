import numpy as np

def sample_at_time(
        df,
        sample_times=None,
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

    Returns
    -------
    pandas.DataFrame
        DataFrame containing sampled Time and Concentration columns.
    """
    # If no sample times are provided, return the original DataFrame
    if sample_times is None:
        return df

    # Ensure sample timepoints is ordered as a numpy array for easier indexing
    sample_times = np.array(sample_times)

    # Sample the DataFrame at the specified time points
    sampled_df = df[df["Time (hr)"].isin(sample_times)].reset_index(drop=True)

    return sampled_df