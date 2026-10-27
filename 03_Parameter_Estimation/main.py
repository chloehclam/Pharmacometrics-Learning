from pathlib import Path
import sys
import numpy as np

simulator_dir = Path(__file__).resolve().parent.parent / "01_PK_Simulator"
sys.path.insert(0, str(simulator_dir))

from pk_simulator import simulate_iv_bolus, simulate_oral
from pk_plotting import plot_pk
from noise import add_noise
from sampling import sample_at_time
from fitting import fitting
from residual import find_residual, plot_residual, analyse_residual

FIGURES_DIR = Path(__file__).resolve().parent / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


#===========================================================
# Example 1: Sampling from IV bolus
#==========================================================
df_true = simulate_iv_bolus(
    dose=100,
    vd=10,
    cl=2,
    duration=24,
    interval=0.1
)

df_obs = add_noise(
    df_true,
    cv=0.1,
)

sample_times = [0.2, 0.5, 1, 2, 4, 8, 12, 24]

df_sample = sample_at_time(
    df_obs,
    sample_times=sample_times,
)

plot_pk(
    [df_true, df_sample],
    title="Concentrations sampled at specific time points",
    yaxis="log(Concentration) (mg/L)",
    yscale="log",
    filename=str(FIGURES_DIR / "noise.png")
)


#=============================================================
# Example 2: Fitting Observed Data
#=============================================================

# Define the one-compartmental model for fitting
def one_comp_iv_bolus(t, vd, k, dose=100):
    return (dose / vd * np.exp(-k * t))

model = lambda t, vd, k: one_comp_iv_bolus(t, vd, k, dose=100)

# Estimate vd and k from the observed data of example 1
popt, pcov = fitting(
    df=df_sample,
    model=model,
    p0=(12, 0.25),
    bounds=([0, 0], [np.inf, np.inf]),
)

se = np.sqrt(np.diag(pcov))

print("IV bolus parameter estimation:")
print(f"Estimated Vd: {popt[0]:.3f} \u00b1 {se[0]:.3f}  True Vd: 10")
print(f"Estimated k: {popt[1]:.3f} \u00b1 {se[1]:.3f}   True k: 0.2")

df_model = simulate_iv_bolus(
    dose=100,
    vd=popt[0],
    cl=(popt[0] * popt[1]),
)

plot_pk(
    [df_true, df_model, df_sample],
    labels=["True", "Modeled", "Sampled"],
    xlabel="Time (hr)",
    ylabel="Concentration (mg/L)",
    styles=["line", "line", "points"],
    title="Fitted curve vs sampled data",
    filename=str(FIGURES_DIR /"fitting.png"),
    show=False
)

df_res = find_residual(
    df_sample,
    model=model,
    popt=popt,
)

plot_residual(
    df_res,
    title="Residual plot of an IV bolus parameter estimation",
    filename = str(FIGURES_DIR /"residual.png")
)

analyse_residual(df_res)

#===========================================================
# Example 3: Oral dose sample modelling
#===========================================================

# Simulate concentration-time profile of an oral dose drug
df_oral_true = simulate_oral(
    dose=100,
    f=0.8, 
    vd=20,
    ka=1.3,
    cl=3.5,
)

# Add noise to the simulated concentration to mimic clinical data
df_oral_obs = add_noise(df_oral_true)

# Extract concentration at specific sampled time points
df_oral_sample = sample_at_time(
    df_oral_obs,
    sample_times,
)

# Define one-compartmental oral absorption model
def one_comp_oral(t, vd, k, f=0.8, ka=1.3, dose=100):
    return f * ka * dose * (np.exp(-k * t) - np.exp(-ka * t)) / (vd * (ka - k))

model_oral = lambda t, vd, k: one_comp_oral(t, vd, k, f=0.8, ka=1.3, dose=100)

# Estimate the PK parameters and their covariances
popt_oral, pcov_oral = fitting(
    df_oral_sample,
    model_oral,
    p0=(25, 0.15),
    bounds=[(0, 0), (np.inf, np.inf)],
)

# Find the standard error of each parameter
se_oral = np.sqrt(np.diag(pcov_oral))

print("\nOral dose parameter estimation:")
print(f"Estimated Vd: {popt_oral[0]:.3f} \u00b1 {se_oral[0]:.3f}  True Vd: 20")
print(f"Estimated k: {popt_oral[1]:.3f} \u00b1 {se_oral[1]:.3f}   True k: 0.175")

# Generate the concentration-time profile with the estimated parameters
df_oral_model = simulate_oral(
    dose=100,
    f=0.8,
    ka=1.3,
    vd=popt_oral[0],
    cl=(popt_oral[0] * popt_oral[1]),
)

plot_pk(
    [df_oral_true, df_oral_model, df_oral_sample],
    labels=["True", "Modeled", "Sampled"],
    xlabel="Time (hr)",
    ylabel="Concentration (mg/L)",
    styles=["line", "line", "points"],
    title="Fitted curve vs sampled data of an oral dose",
    filename=str(FIGURES_DIR /"fitting_oral.png"),
    show=False
)

# Find the residual between the sampled and modelled concentrations
df_oral_res = find_residual(
    df_oral_sample,
    model_oral,
    popt_oral,
)

# Plot the residues between the sampled and modelled concentrations
plot_residual(
    df_oral_res,
    title="Residual plot of an oral dose",
    filename=str(FIGURES_DIR /"residual_oral.png")
)

# Calculate mean residual, MAE and RMSE
analyse_residual(df_oral_res)