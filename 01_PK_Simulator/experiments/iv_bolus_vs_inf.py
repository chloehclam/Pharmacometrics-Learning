# Import necessary modules and functions
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_iv_bolus, simulate_iv_infusion
from pk_analysis import analyse_pk
from pk_plotting import plot_pk

'''
Compare the concentration-time profiles for IV bolus and IV infusion administration
'''
# ==============================================================================
# IV Bolus
# ==============================================================================

# Simulate IV bolus administration
df_bolus = simulate_iv_bolus(
    dose=40,
    vd=10,
    half_life=4,
    duration=24, 
    interval=1,
)

# Analyze the PK parameters for the IV bolus simulation
cmax_bolus, tmax_bolus, auc_bolus = analyse_pk(df_bolus)

# Print the PK parameters for the IV bolus simulation
print(f"IV Bolus Simulation:")
print(f"Cmax: {cmax_bolus:.2f} mg/L")
print(f"Tmax: {tmax_bolus:.2f} hr")
print(f"AUC: {auc_bolus:.2f} mg·hr/L")

# ==============================================================================
# IV Infusion
# ==============================================================================

# Simulate IV infusion administration
df_inf, css = simulate_iv_infusion(
    rate=10,
    vd=10,
    half_life=4,
    duration=24,
    interval=0.1,
)

# Analyze the PK parameters for the IV infusion simulation
cmax_inf, tmax_inf, auc_inf = analyse_pk(df_inf)

# Print the PK parameters for the IV infusion simulation
print(f"\nIV Infusion Simulation:")
print(f"Cmax: {cmax_inf:.2f} mg/L")
print(f"Tmax: {tmax_inf:.2f} hr")
print(f"AUC: {auc_inf:.2f} mg·hr/L")
print(f"Css: {css:.2f} mg/L")


# =============================================================================
# Compare IV Bolus and IV Infusion
# =============================================================================

# Plot the concentration-time profiles for IV bolus and IV infusion administration
plot_pk(
    [df_bolus, df_inf],
    labels=["Bolus: 40 mg", "Infusion: 10 mg/hr"],
    title="IV bolus vs IV infusion",
    filename=str(
            Path(__file__).resolve().parents[1]
            / "figures"
            / "iv_bolus_vs_infusion.png"
        )
)

