import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def find_residual(
    df_sample,
    model,
    popt,
    xcol="Time (hr)",
    ycol="Concentration (mg/L)",
):
    """
    Return a copy of the sampled data with predictions and residuals.

    The model is evaluated at the sampled times using the fitted parameters.
    Residuals are calculated as observed concentration minus predicted
    concentration.

    Parameters
    ----------
    df_sample : pandas.DataFrame
        Sampled observations containing the time and concentration columns.
    model : callable
        Model function called as ``model(t, *popt)``. It must return predicted
        concentrations with a shape compatible with the observations.
    popt : array-like
        Fitted model parameters, in the order expected by ``model``.
    xcol : str, default="Time (hr)"
        Name of the column containing the sample times.
    ycol : str, default="Concentration (mg/L)"
        Name of the column containing the observed concentrations.

    Returns
    -------
    pandas.DataFrame
        A copy of ``df_sample`` with ``Predicted Concentration (mg/L)`` and
        ``Residual Concentration (mg/L)`` columns added.
    """
    # Create a residual DataFrame from the sampled DataFrame
    df_res = df_sample.copy()

    # Extract the sampled time and concentration from the observed DataFrame
    t = df_res[xcol].to_numpy()
    observed = df_res[ycol].to_numpy()

    # Calculate the concentrations at sampled times using parameters from modelling
    predicted = model(t, *popt)

    # Calculate the residues at each sampled times
    df_res["Predicted Concentration (mg/L)"] = predicted
    df_res["Residual Concentration (mg/L)"] = observed - predicted

    return df_res

def plot_residual(
        df_res,
        xcol="Time (hr)",
        ycol="Residual Concentration (mg/L)",
        xaxis=None,
        yaxis=None,
        title="Residual Plot",
        filename=None,
        show=False,
):
    """
    Plot residuals against a selected column and optionally save the plot.

    A horizontal reference line is drawn at zero residual.

    Parameters
    ----------
    df_res : pandas.DataFrame
        Residual data containing the columns selected by ``xcol`` and
        ``ycol``.
    xcol : str, default="Time (hr)"
        Name of the column to use for the horizontal axis.
    ycol : str, default="Residual Concentration (mg/L)"
        Name of the column to use for the vertical axis.
    xaxis : str or None, default=None
        Optional horizontal-axis label. If None, ``xcol`` is used.
    yaxis : str or None, default=None
        Optional vertical-axis label. If None, ``ycol`` is used.
    title : str, default="Residual Plot"
        Plot title.
    filename : str or None, default=None
        If provided, save the plot to this path.
    show : bool, default=False
        If True, display the plot.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If ``df_res`` is not a pandas DataFrame.
    """
    # Validate the input DataFrame
    if not isinstance(df_res, pd.DataFrame):
        raise ValueError("df_res must be a pandas DataFrame.")
    
    # Set up the plot
    plt.figure(figsize=(8, 5))

    # Draw a reference line at residual concentration = 0
    plt.axhline(y=0)

    plt.scatter(
        df_res[xcol],
        df_res[ycol]
    )

    # Set plot labels and title
    if xaxis:
        plt.xlabel(xaxis)
    else:
        plt.xlabel(xcol)

    if yaxis:
        plt.ylabel(yaxis)
    else:
        plt.ylabel(ycol)
    
    plt.title(title)

    # Add grid and adjust layout
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file if a filename is provided, and show the plot if requested
    if filename:
        plt.savefig(filename, dpi=200)

    if show:
        plt.show()

    plt.close()


def analyse_residual(df_res):
    """
    Calculate and print summary metrics for concentration residuals.

    The function reports the mean residual, mean absolute error (MAE), and
    root mean square error (RMSE), using the ``Residual Concentration (mg/L)``
    column in ``df_res``.

    Parameters
    ----------
    df_res : pandas.DataFrame
        Residual data containing a ``Residual Concentration (mg/L)`` column.

    Returns
    -------
    None
        The metrics are printed; they are not returned.
    """
    residuals = df_res["Residual Concentration (mg/L)"]

    mean_residual = residuals.mean()
    mae = residuals.abs().mean()
    rmse = np.sqrt((residuals ** 2).mean())

    print(f"Mean residual: {mean_residual:.3f} mg/L")
    print(f"Mean absolute error (MAE): {mae:.3f} mg/L")
    print(f"Root Mean Square Error (RMSE): {rmse:.3f} mg/L")