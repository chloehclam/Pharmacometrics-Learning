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

from pk_simulator import simulate_two_cmt
from noise import add_noise
from sampling import sample_at_time
from fitting import fitting

FIGURES_DIR = project_dir / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Generate a concentration-time dataframe of a two-compartmental IV bolus
df_true = simulate_two_cmt(
    dose=100, # mg
    vd1=10, # L
    vd2=20, # L
    q=2, # L/hr
    cl=3, # L/hr 
)

sample_times = [0.2, 0.5, 1, 2, 4, 8, 12, 24]

# Extract concentrations at sampled times
df_true_sample = sample_at_time(
    df_true,
    sample_times=sample_times,
)

# Add noise to sampled concentration
df_sample = add_noise(df_true_sample)

def two_cmt_iv_bolus(t, vd1, vd2, q, cl, dose=100):
    df_two_cmt = simulate_two_cmt(
        dose=dose,
        vd1=vd1,
        vd2=vd2,
        q=q,
        cl=cl,
    )

    df_two_cmt_sample = df_two_cmt.loc[df_two_cmt["Time (hr)"].isin(t)].copy()

    return df_two_cmt_sample["Concentration (mg/L)"]

model_two_cmt = lambda t, vd1, vd2, q, cl: two_cmt_iv_bolus(t, vd1, vd2, q, cl,)

popt, pcov = fitting(
    df=df_sample,
    model=model_two_cmt,
    p0=(30, 20, 5, 10),
    bounds=([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf]),
)

se = np.sqrt(np.diag(pcov))

print("Two-compartmental IV bolus parameter estimation:")
print(f"Estimated central Vd: {popt[0]:.3f} \u00b1 {se[0]:.3f}  True central Vd: 10")
print(f"Estimated peripheral Vd: {popt[1]:.3f} \u00b1 {se[1]:.3f}   True peripheral Vd: 20")
print(f"Estimated intercompartmental clearance: {popt[2]:.3f} \u00b1 {se[2]:.3f}  True Q: 2")
print(f"Estimated clearance: {popt[3]:.3f} \u00b1 {se[3]:.3f}   True cl: 3")

