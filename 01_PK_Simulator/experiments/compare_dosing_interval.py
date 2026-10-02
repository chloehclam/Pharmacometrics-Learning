from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_multiple_iv
from pk_analysis import analyse_pk
from pk_plotting import plot_pk

# ============================================================================
# Compare the concentration-time profiles for different dosing intervals
# ============================================================================

dose_intervals = [2, 4, 8] # List of dosing intervals to compare

dfs_dose_interval = [] # List to store the dataframes for different dosing intervals

# Simulate multiple IV dosing for different dosing intervals
for dose_interval in dose_intervals:
    df = simulate_multiple_iv(
        dose=100,
        vd=10,
        half_life=2,
        duration=24,
        dose_interval=dose_interval,
        simulation_interval=0.1
    )

    dfs_dose_interval.append(df) # Append the dataframe to the list

# Analyze the PK parameters for each dosing interval and print them
for dose_interval, df in zip(dose_intervals, dfs_dose_interval):
    cmax, tmax, auc = analyse_pk(df)
    print(f"\nDose interval = {dose_interval} hr:")
    print(f"Cmax: {cmax:.2f} mg/L")
    print(f"Tmax: {tmax:.2f} hr")
    print(f"AUC: {auc:.2f} mg·hr/L")

# Plot the concentration-time profiles for different dosing intervals
plot_pk(
    dfs_dose_interval,
    labels=[f"dosing interval = {dose_interval} hr" for dose_interval in dose_intervals],
    title="Effect of dosing interval",
    filename=str(
            Path(__file__).resolve().parents[1]
            / "figures"
            / "dosing_interval_comparison.png"
        )
)
