# Import the functions from pk_simulator and pk_analysis
from pk_simulator import (
    simulate_iv_bolus,
    simulate_oral,
    simulate_multiple_iv,
    simulate_inf_ld,
    simulate_iv_infusion,
)
from pk_analysis import analyse_pk
from pk_plotting import plot_pk
from pathlib import Path

FIGURES_DIR = Path(__file__).resolve().parent / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)


# ============================================================================
# Example 1: IV Bolus Administration
# ============================================================================

# Simulate IV bolus administration
iv_bolus_df = simulate_iv_bolus(
    dose=100,
    vd=10,
    half_life=4
)

# Analyze the PK parameters for the IV bolus simulation
iv_cmax, iv_tmax, iv_auc = analyse_pk(iv_bolus_df)

# Print the PK parameters for the IV bolus simulation
print("IV Bolus Simulation:")
print(f"Cmax: {iv_cmax:.2f} mg/L")
print(f"Tmax: {iv_tmax:.2f} hr")
print(f"AUC: {iv_auc:.2f} mg·hr/L")

# Plot the concentration-time profile for the IV bolus simulation
plot_pk(
    iv_bolus_df,
    title="IV bolus PK simulation",
    filename=str(FIGURES_DIR / "iv_bolus.png")
)


# ============================================================================
# Example 2: Oral Administration
# ============================================================================

# Simulate oral administration
oral_df = simulate_oral(
    dose=100,
    F=0.8,
    vd=10,
    ka=1.2,
    cl=2,
    duration=24,
    interval=0.1
)

# Analyze the PK parameters for the oral administration simulation
oral_cmax, oral_tmax, oral_auc = analyse_pk(oral_df)

# Print the PK parameters for the oral administration simulation
print("\nOral Administration Simulation:")
print(f"Cmax: {oral_cmax:.2f} mg/L")
print(f"Tmax: {oral_tmax:.2f} hr")
print(f"AUC: {oral_auc:.2f} mg·hr/L")

# Plot the concentration-time profile for the oral administration simulation
plot_pk(
    oral_df,
    title="Oral absorption PK profile",
    filename=str(FIGURES_DIR / "oral_absorption.png")
)


# ============================================================================
# Example 3: Multiple IV Dosing
# ============================================================================

# Simulate multiple IV dosing
df_mtp_iv = simulate_multiple_iv(
    dose=100,
    vd=10,
    half_life=2,
    duration=24,
    dose_interval=4,
    simulation_interval=0.1
)

# Analyze the PK parameters for the multiple IV dosing simulation
mtp_iv_cmax, mtp_iv_tmax, mtp_iv_auc = analyse_pk(df_mtp_iv)

# Print the PK parameters for the multiple IV dosing simulation
print("\nMultiple IV Dosing Simulation:")
print(f"Cmax: {mtp_iv_cmax:.2f} mg/L")
print(f"Tmax: {mtp_iv_tmax:.2f} hr")
print(f"AUC: {mtp_iv_auc:.2f} mg·hr/L")

# Plot the concentration-time profile for the multiple IV dosing simulation
plot_pk(
    df_mtp_iv,
    title="Multiple IV dosing PK simulation",
    filename=str(FIGURES_DIR / "multiple_iv.png")
)


# ============================================================================
# Example 4: IV Infusion
# ============================================================================

# Simulate IV infusion
df_iv_inf, css = simulate_iv_infusion(
    rate=10,
    vd=10,
    half_life=4,
    duration=24,
    interval=0.1
)

# Analyze the PK parameters for the IV infusion simulation  
cmax_inf, tmax_inf, auc_inf = analyse_pk(df_iv_inf)

# Print the PK parameters for the IV infusion simulation
print("\nIV Infusion Simulation:")
print(f"Cmax: {cmax_inf:.2f} mg/L")
print(f"Tmax: {tmax_inf:.2f} hr")
print(f"AUC: {auc_inf:.2f} mg·hr/L")
print(f"Css: {css:.2f} mg/L")

# Plot the concentration-time profile for the IV infusion simulation
plot_pk(
    df_iv_inf,
    title="IV infusion PK simulation",
    filename=str(FIGURES_DIR / "iv_infusion.png")
)


# ============================================================================
# Example 5: IV Infusion with Loading Dose
# ============================================================================

# Simulate IV infusion with loading dose
df_inf_ld, df_inf, df_ld, css = simulate_inf_ld(
    rate=10,
    vd=10,
    half_life=4
)

# Analyze the PK parameters for the IV infusion with loading dose simulation
cmax_inf_ld, tmax_inf_ld, auc_inf_ld = analyse_pk(df_inf_ld)

# Print the PK parameters for the IV infusion with loading dose simulation
print("\nIV Infusion with Loading Dose Simulation:")
print(f"Cmax: {cmax_inf_ld:.2f} mg/L")
print(f"Tmax: {tmax_inf_ld:.2f} hr")
print(f"AUC: {auc_inf_ld:.2f} mg·hr/L")
print(f"Css: {css:.2f} mg/L")

# Plot the concentration-time profiles for IV infusion with loading dose
plot_pk(
    [df_inf_ld, df_inf, df_ld],
    labels=["Loading dose + infusion", "Infusion", "Loading dose"],
    title="IV infusion with loading dose",
    filename=str(FIGURES_DIR / "infusion_loading_dose.png")
)
