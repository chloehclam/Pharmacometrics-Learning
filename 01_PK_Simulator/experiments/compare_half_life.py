# Import necessary modules and functions
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_multiple_iv
from pk_analysis import analyse_pk
from pk_plotting import plot_pk


# Compare the concentration-time profiles for different half-life values
half_lives = [2, 4, 8]

dfs_half_life = [] # List to store the dataframes for different half-life values

# Simulate multiple IV dosing for different half-life values
for half_life in half_lives:
    df = simulate_multiple_iv(
        dose=100,
        vd=10,
        half_life=half_life,
        duration=24,
        dose_interval=4,
        simulation_interval=0.1
    )

    dfs_half_life.append(df) # Append the dataframe to the list

# Analyze the PK parameters for each half-life value and print them
for half_life, df in zip(half_lives, dfs_half_life):
    cmax, tmax, auc = analyse_pk(df)
    print(f"\nHalf-life = {half_life} hr:")
    print(f"Cmax: {cmax:.2f} mg/L")
    print(f"Tmax: {tmax:.2f} hr")
    print(f"AUC: {auc:.2f} mg·hr/L")

# Plot the concentration-time profiles for different half-life values
plot_pk(
    dfs_half_life,
    labels=[f"Half-life = {half_life} hr" for half_life in half_lives],
    title="Effect of half-life",
    filename=str(
            Path(__file__).resolve().parents[1]
            / "figures"
            / "half_life_comparison.png"
        )
)