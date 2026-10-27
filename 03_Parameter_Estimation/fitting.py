import scipy.optimize as optimize
import numpy as np

def fitting(
        df,
        model,
        p0,
        bounds,
        xcol="Time (hr)",
        ycol="Concentration (mg/L)",
        weighting="proportional",
):
    """
    Find PK parameters by fitting sampled data 

    Parameters
    ----------
    df: pandas.DataFrame
        DataFrame containing Time and Concentration columns.
    model: callable
        Model function called as ``model(t, *params)``. It takes the time 
        values followed by the parameters to fit, and returns predicted
        concentrations with the same shape as the observed concentrations.
    p0: array-like
        Initial guesses for the parameters to estimate.
    bounds: 2-tuples of array-like
        Upper and lower bounds of each PK parameters.
    xcol: str
        Name of x-column of df.
    ycol: str
        Name of y-column of df.
    weighting : {"none", "proportional"}, default="proportional"
        Residual weighting method used during fitting.
    
    Returns
    -------
    popt: numpy.ndarray
        Estimated PK parameter values at the optimum.
    pcov : numpy.ndarray
        Approximate covariance matrix of the estimated parameters.

    Raises
    ------
    ValueError
        if weighting is not "none" or "proportional", or if any observed 
        concentration is zero or negative
    """
    t = df[xcol].to_numpy(dtype=float)
    y = df[ycol].to_numpy(dtype=float)

    if weighting not in {"none", "proportional"}:
        raise ValueError("weighting must be 'none' or 'proportional'")

    if np.any(y <= 0):
        raise ValueError("Concentrations must be positive.")

    if weighting == "none":
        popt, pcov = optimize.curve_fit(model, t, y, p0=p0, bounds=bounds)

    else:
        popt, pcov = optimize.curve_fit(model, t, y, p0=p0, bounds=bounds, sigma=y)

    return popt, pcov