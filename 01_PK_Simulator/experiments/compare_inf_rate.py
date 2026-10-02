from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_iv_infusion
from pk_analysis import analyse_pk
from pk_plotting import plot_pk

# ============================================================================
# Compare the concentration-time profiles for different infusion rates
# ============================================================================

inf_rates = [5, 10, 20] # List of infusion rates to compare

dfs_iv_inf = [] # List to store the dataframes for different infusion rates

css_set = [] # List to store the steady-state concentrations for different infusion rates

# Simulate IV infusion for different infusion rates
for inf_rate in inf_rates:
    df, css = simulate_iv_infusion(
        rate=inf_rate,
        vd=10,
        half_life=4,
        duration=24,
        interval=0.1
    )

    dfs_iv_inf.append(df)

    css_set.append(css)

# Analyze the PK parameters for each infusion rate and print them
for inf_rate, df, css in zip(inf_rates, dfs_iv_inf, css_set):
    cmax, tmax, auc = analyse_pk(df)
    print(f"\nInfusion rate = {inf_rate} mg/hr:")
    print(f"Cmax: {cmax:.2f} mg/L")
    print(f"Tmax: {tmax:.2f} hr")
    print(f"AUC: {auc:.2f} mg·hr/L")
    print(f"Css: {css:.2f} mg/L")

# Plot the concentration-time profiles for different infusion rates
plot_pk(
    dfs_iv_inf,
    labels=[f"Infusion rate = {inf_rate} mg/hr" for inf_rate in inf_rates],
    title="IV infusion rate comparison",
    filename=str(
            Path(__file__).resolve().parents[1]
            / "figures"
            / "inf_rate_comparison.png"
        )
)