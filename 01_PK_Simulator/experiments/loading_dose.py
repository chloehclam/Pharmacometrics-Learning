from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_inf_ld
from pk_analysis import analyse_pk
from pk_plotting import plot_pk

# =============================================================================
# Compare the concentration-time profiles for IV infusion with loading dose
# =============================================================================

# Simulate IV infusion with self-defined loading dose (half of the maintenance dose)
df_inf_ld, df_inf, df_ld, css = simulate_inf_ld(
    rate=10,
    vd=10,
    half_life=4,
    loading_dose=28.85
)
# Analyze the PK parameters for the IV infusion with loading dose simulation
cmax_inf_ld, tmax_inf_ld, auc_inf_ld = analyse_pk(df_inf_ld)

# Print the PK parameters for the IV infusion with loading dose simulation
print(f"\nIV Infusion with Loading Dose Simulation:")
print(f"Cmax: {cmax_inf_ld:.2f} mg/L")
print(f"Tmax: {tmax_inf_ld:.2f} hr")
print(f"AUC: {auc_inf_ld:.2f} mg·hr/L")
print(f"Css: {css:.2f} mg/L")

# Plot the concentration-time profiles for IV infusion with loading dose
plot_pk(
    [df_inf_ld, df_inf, df_ld],
    labels=["Loading dose + infusion", "Infusion", "Loading dose"],
    title="IV infusion with loading dose",
    filename=str(
                Path(__file__).resolve().parents[1]
                / "figures"
                / "loading_dose.png"
            )
)