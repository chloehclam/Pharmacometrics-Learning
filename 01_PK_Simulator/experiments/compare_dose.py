from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_multiple_iv
from pk_analysis import analyse_pk
from pk_plotting import plot_pk

# ============================================================================
# Compare the concentration-time profiles for different doses
# ============================================================================

doses = [50, 100, 200] # List of doses to compare

dfs_dose = [] # List to store the dataframes for different doses

# Simulate multiple IV administrations for different doses
for dose in doses:
    df = simulate_multiple_iv(
        dose=dose,
        vd=10,
        half_life=2,
        duration=24,
        dose_interval=4,
        simulation_interval=0.1
    )

    dfs_dose.append(df) # Append the dataframe to the list

# Analyze the PK parameters for each dose and print them
for dose, df in zip(doses, dfs_dose):
    cmax, tmax, auc = analyse_pk(df)
    print(f"\nDose = {dose} mg:")
    print(f"Cmax: {cmax:.2f} mg/L")
    print(f"Tmax: {tmax:.2f} hr")
    print(f"AUC: {auc:.2f} mg·hr/L")

# Plot the concentration-time profiles for different doses
plot_pk(
    dfs_dose,
    labels=[f"Dose = {dose} mg" for dose in doses],
    title="Effect of dose",
    filename=str(
            Path(__file__).resolve().parents[1]
            / "figures"
            / "dose_comparison.png"
    )
)
