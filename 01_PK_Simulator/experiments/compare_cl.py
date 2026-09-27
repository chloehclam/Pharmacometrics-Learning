# Import necessary modules and functions
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_oral
from pk_analysis import analyse_pk
from pk_plotting import plot_pk


# Compare the concentration-time profiles for different clearance values
cl_values = [1, 2, 4]

dfs_cl = [] # List to store the dataframes for different clearance values

# Simulate oral administration for different clearance values
for cl in cl_values:
    df = simulate_oral(
            dose = 100,
            F = 0.8,
            vd = 10,
            ka = 1.2,
            cl = cl,
            duration = 24,
            interval = 0.1,
        )

    dfs_cl.append(df) # Append the dataframe to the list

# Analyze the PK parameters for each clearance value and print them
for cl, df in zip(cl_values, dfs_cl):
    cmax, tmax, auc = analyse_pk(df)
    print(f"\nClearance = {cl} L/hr:")
    print(f"Cmax: {cmax:.2f} mg/L")
    print(f"Tmax: {tmax:.2f} hr")
    print(f"AUC: {auc:.2f} mg·hr/L")   

# Plot the concentration-time profiles for different clearance values
plot_pk(
    dfs_cl,
    labels=[f"CL = {cl} L/hr" for cl in cl_values],
    title="Effect of clearance",
    filename=str(
           Path(__file__).resolve().parents[1]
           / "figures"
           / "cl_comparison.png"
       )
)   