import pandas as pd
import numpy as np  
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# Plot the PK profile for the simulated data
def plot_pk(
    dfs,
    labels=None,
    xlabel="Time (hr)",
    ylabel="Concentration (mg/L)",
    title="PK profile",
    filename=None,
    show=False
):
    '''
    Plot the concentration-time profile for the simulated data.
    
    Parameters
    ----------
    dfs : pandas.DataFrame or list of pandas.DataFrame
        DataFrame(s) containing Time and Concentration.
    labels : list of str, optional
        Labels for the different concentration-time profiles.
    title : str, optional
        Title of the plot.
    filename : str, optional
        Filename to save the plot. If None, the plot will not be saved.
    show : bool, optional
        If True, the plot will be displayed. Default is False.
    
    Raises
    ------
    ValueError
        If dfs is not a pandas DataFrame or a list of pandas DataFrames.
        If any DataFrame does not contain the required columns.
    '''
    # Validate input parameters
    if not isinstance(dfs, (list, pd.DataFrame)):
        raise ValueError("dfs must be a pandas DataFrame or a list of pandas DataFrames.")
    
    # If dfs is a single DataFrame, convert it to a list for uniform processing
    if isinstance(dfs, pd.DataFrame):
        dfs = [dfs]

    # Check that each DataFrame contains the required columns
    for df in dfs:
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Each item in dfs must be a pandas DataFrame.")
        if "Time (hr)" not in df.columns or "Concentration (mg/L)" not in df.columns:
            raise ValueError("Each DataFrame must contain 'Time (hr)' and 'Concentration (mg/L)' columns.")

    # Set up the plot
    plt.figure(figsize=(8, 5))

    # Check if labels are provided and match the number of DataFrames
    if labels is not None and len(labels) != len(dfs):
        raise ValueError("The number of labels must match the number of dataframes.")

    # Plot each DataFrame
    for i, df in enumerate(dfs):
        # Use the corresponding label if provided, otherwise use None
        label = labels[i] if labels else None

        # Plot the concentration-time profile
        plt.plot(
            df[xlabel],
            df[ylabel],
            label=label
        )

    # Set plot labels and title
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    # Add legend if labels are provided
    if labels:
        plt.legend()

    # Add grid and adjust layout
    plt.grid(True)
    plt.tight_layout()

    # Save the plot to a file if a filename is provided, and show the plot if requested
    if filename:
        plt.savefig(filename, dpi=200)

    if show:
        plt.show()

    plt.close()