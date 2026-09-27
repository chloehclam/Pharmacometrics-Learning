import pandas as pd 
import numpy as np


def check_parameters(**kwargs):
    """
    Validate recognized pharmacokinetic simulation parameters.

    Parameters
    ----------
    **kwargs : float
        Named parameters to validate. Recognized values must be positive, except
        bioavailability (F), which must be in the range (0, 1]. Values set to
        None are skipped.

    Returns
    -------
    None

    Raises
    ------
    ValueError
        If a recognized parameter is non-positive or F is outside (0, 1].
    """
    allowed_positive = {
        "dose",
        "rate",
        "vd",
        "half_life",
        "duration",
        "interval",
        "F",
        "ka",
        "cl",
        "dose_interval",
        "simulation_interval",
    }

    for name, value in kwargs.items():
        if value is None:
            continue

        if name == "F":
            if not 0 < value <= 1:
                raise ValueError("Bioavailability (F) must be between 0 and 1.")
            continue

        if name in allowed_positive and value <= 0:
            label = name.replace("_", " ").title()
            raise ValueError(f"{label} must be positive.")


def simulate_iv_bolus(
    dose,
    vd,
    half_life,
    duration=24, 
    interval=1,
):
    """
    Simulate a one-compartment, single-dose IV bolus model.

    Parameters
    ----------
    dose : float
        Drug dose in mg.
    vd : float
        Volume of distribution in L.
    half_life : float
        Elimination half-life in hours.
    duration : float, optional
        Total simulation time in hours. Defaults to 24.
    interval : float, optional
        Time between simulated samples in hours. Defaults to 1.

    Returns
    -------
    pandas.DataFrame
        Concentration-time data with ``Time (hr)`` and
        ``Concentration (mg/L)`` columns.

    Raises
    ------
    ValueError
        If a validated parameter is outside its allowed range.
    """
    # Check the validity of input parameters
    check_parameters(
        dose=dose,
        vd=vd,
        half_life=half_life,
        duration=duration,
        interval=interval,
    )

    # Calculate initial concentration and elimination rate constant
    c0 = dose/vd 

    # Calculate elimination rate constant (k) using half-life
    k = np.log(2) / half_life

    # Generate time points for simulation
    time = np.arange(0, duration + interval, interval)

    # Calculate concentration at each time point using the one-compartment IV bolus model
    concentration = c0 * np.exp(-k * time)

    # Create a DataFrame to store the time and concentration data
    data = {
    "Time (hr)": time,
    "Concentration (mg/L)": concentration
    }

    df = pd.DataFrame(data) 

    return df


def simulate_oral(
    dose,
    F, 
    vd,
    ka,
    cl,
    duration=24,
    interval=1,
):
    '''
    Simulate a one-compartment oral administration model.

    Parameters
    ----------
    dose : float
        Drug dose in mg.
    F : float
        Bioavailability as a fraction between 0 and 1.
    vd : float
        Volume of distribution in L.
    ka : float
        Absorption rate constant in hr⁻¹. Must differ from the elimination
        rate constant (cl / vd) for the implemented equation.
    cl : float
        Clearance in L/hr.
    duration : float, optional
        Total simulation time in hours. Defaults to 24.
    interval : float, optional
        Time between simulated samples in hours. Defaults to 1.

    Returns
    -------
    pandas.DataFrame
        Concentration-time data with ``Time (hr)`` and
        ``Concentration (mg/L)`` columns.

    Raises
    ------
    ValueError
        If a validated parameter is outside its allowed range.
    '''
    # Validate input parameters
    check_parameters(
        dose=dose,
        vd=vd,
        duration=duration,
        interval=interval,
        F=F,
        ka=ka,
        cl=cl,
    )

    k = cl / vd
    
    # Generate time points for simulation
    time = np.arange(0, duration + interval, interval)

    # Calculate the concentration at each time point using the one-compartment oral administration model
    constant = F * dose * ka / (vd * (ka - k))

    concentration = constant * (np.exp(-k * time) - np.exp  (-ka * time))

    # Create a DataFrame to store the time and concentration data
    data = {
    "Time (hr)": time,
    "Concentration (mg/L)": concentration
    }

    df = pd.DataFrame(data)

    return df


def simulate_multiple_iv(
    dose,
    vd,
    half_life,
    duration=24,
    dose_interval=4,
    simulation_interval=0.1,     
):
    '''
    Simulate repeated IV bolus doses using a one-compartment model.

    Parameters
    ----------
    dose : float
        Amount administered at each dose, in mg.
    vd : float
        Volume of distribution in L.
    half_life : float
        Elimination half-life in hours.
    duration : float, optional
        Total simulation time in hours. Defaults to 24.
    dose_interval : float, optional
        Time between doses in hours. Defaults to 4.
    simulation_interval : float, optional
        Time between simulated samples in hours. Defaults to 0.1.

    Returns
    -------
    pandas.DataFrame
        Concentration-time data with ``Time (hr)`` and
        ``Concentration (mg/L)`` columns.

    Raises
    ------
    ValueError
        If a validated parameter is outside its allowed range.
    '''
    # Validate input parameters
    check_parameters(
        dose=dose,
        vd=vd,
        half_life=half_life,
        duration=duration,
        dose_interval=dose_interval,
        simulation_interval=simulation_interval,
    )

    # Calculate initial concentration and elimination rate constant
    c0 = dose/vd

    k = np.log(2) / half_life

    # Generate time points for simulation
    time = np.arange(0, duration + simulation_interval, simulation_interval)

    # Calculate the times at which doses are administered
    dose_times = np.arange(0, duration, dose_interval)

    # Calculate the concentration at each time point using the one-compartment multiple IV bolus model
    concentration = np.zeros_like(time, dtype=float)

    # Add the contribution of each dose to the concentration-time profile
    for dose_time in dose_times:
        mask = time >= dose_time

        concentration[mask] += (
            c0 * np.exp(-k * (time[mask] - dose_time))
        )

    # Create a DataFrame to store the time and concentration data
    data = {
        "Time (hr)": time,
        "Concentration (mg/L)": concentration
    }

    df = pd.DataFrame(data)

    return df


def simulate_iv_infusion(
    rate,
    vd,
    half_life,
    duration=24,
    interval=0.1,
):
    """
    Simulate a one-compartment constant-rate IV infusion.

    Parameters
    ----------
    rate : float
        Infusion rate in mg/hr.
    vd : float
        Volume of distribution in L.
    half_life : float
        Elimination half-life in hours.
    duration : float, optional
        Total simulation time in hours. Defaults to 24.
    interval : float, optional
        Time between simulated samples in hours. Defaults to 0.1.

    Returns
    -------
    tuple[pandas.DataFrame, float]
        A tuple containing:
        - Concentration-time data with ``Time (hr)`` and
          ``Concentration (mg/L)`` columns.
        - Steady-state concentration in mg/L.

    Raises
    ------
    ValueError
        If a validated parameter is outside its allowed range.
    """
    # Check the validity of input parameters
    check_parameters(
        rate=rate,
        vd=vd,
        half_life=half_life,
        duration=duration,
        interval=interval,
    )

    # Calculate initial concentration and elimination rate constant
    c0 = rate / vd

    # Calculate elimination rate constant (k) using half-life
    k = np.log(2) / half_life

    # Generate time points for simulation
    time = np.arange(0, duration + interval, interval)

    # Calculate concentration at each time point using the one-compartment IV infusion model
    css = rate / (k * vd)

    concentration = css * (1 - np.exp(-k * time))

    # Create a DataFrame to store the time and concentration data
    data = {
        "Time (hr)": time,
        "Concentration (mg/L)": concentration
    }

    df = pd.DataFrame(data)

    return df, css


def simulate_inf_ld(
    rate,
    vd,
    half_life,
    loading_dose=None,
    duration=24,
    interval=0.1
):
    """
    Simulate a constant-rate IV infusion with a loading dose.

    If ``loading_dose`` is None, it is calculated as ``rate / k``, where
    ``k`` is the elimination rate constant. The function returns the combined
    profile and the profiles for each component separately.

    Parameters
    ----------
    rate : float
        Infusion rate in mg/hr.
    vd : float
        Volume of distribution in L.
    half_life : float
        Elimination half-life in hours.
    loading_dose : float or None, optional
        Loading dose in mg. If None, it is calculated to target the infusion's
        steady-state concentration. Defaults to None.
    duration : float, optional
        Total simulation time in hours. Defaults to 24.
    interval : float, optional
        Time between simulated samples in hours. Defaults to 0.1.

    Returns
    -------
    tuple[pandas.DataFrame, pandas.DataFrame, pandas.DataFrame, float]
        A tuple containing, in order:
        - Combined loading-dose and infusion concentration data.
        - Infusion-only concentration data.
        - Loading-dose-only concentration data.
        - Steady-state concentration in mg/L.

    Raises
    ------
    ValueError
        If a validated parameter is outside its allowed range.
    """
    # Validate input parameters
    check_parameters(
        rate=rate,
        vd=vd,
        half_life=half_life,
        loading_dose=loading_dose,
        duration=duration,
        interval=interval
    )  

    # Calculate elimination rate constant (k) using half-life
    k = np.log(2) / half_life

    # If loading_dose is not provided, calculate it to achieve the steady-state concentration of the infusion
    if loading_dose is None:
        loading_dose = rate / k

    # Simulate the loading dose and infusion separately
    df_loading = simulate_iv_bolus(
        dose=loading_dose,
        vd=vd,
        half_life=half_life,
        duration=duration,
        interval=interval
    )

    df_inf, css = simulate_iv_infusion(
        rate=rate,
        vd=vd,
        half_life=half_life,
        duration=duration,
        interval=interval
    )

    # Combine the loading dose and infusion concentration-time profiles
    df_overall = pd.DataFrame({
        "Time (hr)": df_loading["Time (hr)"],
        "Concentration (mg/L)": (df_loading["Concentration (mg/L)"] + 
                                 df_inf["Concentration (mg/L)"])
    })

    # Return the combined profile, individual profiles, and steady-state concentration
    return df_overall, df_inf, df_loading, css
