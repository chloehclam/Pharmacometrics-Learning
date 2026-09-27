# Import necessary modules and functions
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_oral
from pk_analysis import analyse_pk
from pk_plotting import plot_pk


# Compare the concentration-time profiles for different ka values
ka_values = [5.0, 1.2, 0.5]

dfs_ka = [] # List to store the dataframes for different ka values

# Simulate oral administration for different ka values
for ka in ka_values:
    df = simulate_oral(
        dose=100,
        F=0.8,
        vd=10,
        ka=ka,
        cl=2,
        duration=24,
        interval=0.1
    )

    dfs_ka.append(df) # Append the dataframe to the list

# Analyze the PK parameters for each ka value and print them
for ka, df in zip(ka_values, dfs_ka):
    cmax, tmax, auc = analyse_pk(df)
    print(f"\nka = {ka} hr⁻¹:")
    print(f"Cmax: {cmax:.2f} mg/L")
    print(f"Tmax: {tmax:.2f} hr")
    print(f"AUC: {auc:.2f} mg·hr/L")

# Plot the concentration-time profiles for different ka values
plot_pk(
    dfs_ka,
    labels=[f"ka = {ka} hr⁻¹" for ka in ka_values],
    title="Effect of absorption rate constant",
    filename=str(
        Path(__file__).resolve().parents[1]
        / "figures"
        / "ka_comparison.png"
    )
)
