from pathlib import Path
import sys
import numpy as np
import pandas as pd

# Locate the project folders relative to this script
project_dir = Path(__file__).resolve().parents[1]  # 03_Parameter_Estimation
simulator_dir = project_dir.parent / "01_PK_Simulator"

# Make both folders available for imports
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(simulator_dir))

from pk_simulator import simulate_iv_bolus
from noise import add_noise
from sampling import sample_at_time
from fitting import fitting

FIGURES_DIR = project_dir / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

#==============================================================
# To evaluate the accuracy, precision, and uncertainty of nonlinear parameter estimation
#==============================================================

# Generate an IV bolus concentration-time dataset
df_true = simulate_iv_bolus(
    dose=100, # mg
    vd=10, # L
    cl=2, # L/hr
)

sample_times = [0.2, 0.5, 1, 2, 4, 8, 12, 24]

# Extract concentrations at sampled times
df_true_sample = sample_at_time(
    df_true,
    sample_times=sample_times,
)

rng = np.random.default_rng(42)

noisy_columns = []

for i in range(200):
    df_noisy = add_noise(df_true_sample.copy(), rng=rng)
    noisy_columns.append(
        df_noisy["Concentration (mg/L)"].to_numpy()
    )

noisy_array = np.array(noisy_columns).T

df_sample = pd.concat(
    [
        df_true_sample[["Time (hr)"]].reset_index(drop=True),
        pd.DataFrame(noisy_array, columns=range(200)),
    ],
    axis=1,
)


# Define the one-compartmental model for fitting
def one_comp_iv_bolus(t, vd, k, dose=100):
    return (dose / vd * np.exp(-k * t))

model = lambda t, vd, k: one_comp_iv_bolus(t, vd, k, dose=100)

popts = []
pcovs = []

for i in range(200):
    df_fit = pd.DataFrame({
        "Time (hr)": df_sample["Time (hr)"],
        "Concentration (mg/L)": df_sample[i],
    })

    popt, pcov = fitting(
        df=df_fit, 
        model=model,
        p0=(30, 0.5),
        bounds=([0, 0], [np.inf, np.inf]),
        )

    popts.append(popt)
    pcovs.append(pcov)

popt_arr = np.array(popts)

se_arr = np.array([
    np.sqrt(np.diag(pcov))
    for pcov in pcovs
])

mean_se = se_arr.mean(axis=0)

summary = pd.DataFrame({
    "Parameter": ["Vd", "k"],
    "True value": [10, 0.2],
    "Mean estimate": popt_arr.mean(axis=0),
    "Bias": popt_arr.mean(axis=0) - np.array([10, 0.2]),
    "Empirical SD": popt_arr.std(axis=0, ddof=1),
    "Mean estimated SE": se_arr.mean(axis=0),
    "RMSE": np.sqrt(
        np.mean((popt_arr - np.array([10, 0.2]))**2, axis=0)
    ),
})

print(summary)




