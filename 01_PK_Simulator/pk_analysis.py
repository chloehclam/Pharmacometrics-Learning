import numpy as np

# Analyze the PK parameters from the simulated data
def analyse_pk(df):
    '''
    Calculate Cmax, Tmax, and AUC from the simulated concentration-time data.
    
    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame containing Time and Concentration.
    
    Returns
    -------
    tuple
        Cmax, Tmax, and AUC values.
    '''
    # Calculate Cmax, Tmax, and AUC from the simulated concentration-time data  
    cmax = df["Concentration (mg/L)"].max()

    cmax_index = df["Concentration (mg/L)"].idxmax()

    tmax = df.loc[cmax_index, "Time (hr)"]

    # Calculate AUC using the trapezoidal rule
    concentration = df["Concentration (mg/L)"].to_numpy()

    time = df["Time (hr)"].to_numpy()

    auc = np.sum(
        (concentration[:-1] + concentration[1:]) / 2 
        * (time[1:] - time[:-1])
        )

    return cmax, tmax, auc