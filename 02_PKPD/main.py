# import necessary libraries
from pathlib import Path
import sys

simulator_dir = Path(__file__).resolve().parent.parent / "01_PK_Simulator"
sys.path.insert(0, str(simulator_dir))

from pk_simulator import simulate_iv_infusion, simulate_oral
from pd_models import emax_model, inhibitory_emax_model
from pkpd_analysis import concentration_for_effect
from pkpd_plotting import plot_effect_concentration, plot_effect_time

FIGURES_DIR = Path(__file__).resolve().parent / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

#===========================================================
# Example 1: Emax Model
#==========================================================

# Simulate IV infusion to get concentration-time profile
df, css = simulate_iv_infusion(
    rate=10,
    vd=10,
    half_life=4
)

# Calculate the effect using the Emax model
effect_ec50 = emax_model(
    df["Concentration (mg/L)"].to_numpy(),
    emax=100,
    ec50=5
)

# Add the effect to the DataFrame
df["Effect"] = effect_ec50

# Plot the effect-concentration profile
plot_effect_concentration(
    df,
    title="Effect-Concentration Profile",
    filename=str(FIGURES_DIR / "effect_concentration_profile.png")
)


#===========================================================
# Example 2: Inhibitory Emax Model
#===========================================================

# Simulate IV infusion to get concentration-time profile
df, css = simulate_iv_infusion(
    rate=10,
    vd=10,
    half_life=4
)

# Calculate the effect using the inhibitory Emax model
effect_i = inhibitory_emax_model(
    df["Concentration (mg/L)"].to_numpy(),
    imax=100,
    ic50=5,
    e0=50
)

# Add the effect to the DataFrame
df["Effect"] = effect_i

# Plot the effect-concentration profile
plot_effect_concentration(
    df,
    title="Inhibitory Effect-Concentration Profile",
    filename=str(FIGURES_DIR / "inhibitory_effect_concentration_profile.png")
)


#===========================================================
# Example 3: effect-time profile of oral dose
#===========================================================

# Simulate oral dose to get concentration-time profile
df = simulate_oral(
    dose=100,
    F=0.8,
    vd=10,
    ka=1.2,
    cl=2
)

# Calculate the effect using the Emax model
effect_ec50 = emax_model(
    df["Concentration (mg/L)"].to_numpy(),
    emax=100,
    ec50=5
)

# Add the effect to the DataFrame
df["Effect"] = effect_ec50

# Plot the effect-time profile
plot_effect_time(
    df,
    title="Effect-Time Profile of Oral Dose",
    filename=str(FIGURES_DIR / "effect_time_profile.png")
)


#===========================================================
# Example 4: Concentration for Desired Effect
#===========================================================

# Find the concentration required to achieve a desired effect using the Emax model
concentration = concentration_for_effect(
    effect=75,
    emax=100,
    ec50=5,
    e0=0
)

# Print the concentration required for the desired effect
print(f"Concentration required for desired effect of 75: {concentration:.2f} mg/L")