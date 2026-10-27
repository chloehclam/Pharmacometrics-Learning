import numpy as np

_DEFAULT_RNG = np.random.default_rng(42) 

def add_noise(df, cv=0.1, rng=None):
    """
    Add Gaussian noise to the concentration data in the DataFrame.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing Time and Concentration columns.
    cv : float, optional
        Coefficient of variation for the Gaussian noise to be added. Default is 0.1.
    rng : numpy.random.Generator, optional
        Random number generator. Default is None.

    Returns
    -------
    pandas.DataFrame
        DataFrame with added noise to the Concentration column.
    """
    noisy_df = df.copy() # Create a copy of the original DataFrame to avoid modifying it directly

    # If no random number generator is provided, use the default one
    if rng is None:
        rng = _DEFAULT_RNG

    # Calculate the noise level based on the coefficient of variation and the concentration values
    noise_level = cv * df["Concentration (mg/L)"]

    # Add Gaussian noise to the concentration values
    noisy_df["Concentration (mg/L)"] += rng.normal(
        0, noise_level, size=len(df)
    )
    
    return noisy_df