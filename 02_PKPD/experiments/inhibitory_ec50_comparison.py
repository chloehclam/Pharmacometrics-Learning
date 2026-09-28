# import necessary libraries
from pathlib import Path
import sys

# Locate the project folders relative to this script
project_dir = Path(__file__).resolve().parents[1]  # 02_PKPD
simulator_dir = project_dir.parent / "01_PK_Simulator"

# Make both folders available for imports
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(simulator_dir))

from pk_simulator import simulate_iv_infusion
from pd_models import inhibitory_emax_model
from pkpd_plotting import plot_effect_concentration

FIGURES_DIR = project_dir / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Compare effect-concentration profiles for different EC50 values
inhibitory_ec50_values = [1, 5, 20]

dfs_inhibitory_ec50 = [] # List to store DataFrames for each EC50 value

# Simulate IV infusion to get concentration-time profile
df, css = simulate_iv_infusion(
    rate=10,
    vd=10,
    half_life=4
)

# Calculate the effect for each EC50 value and store the results in separate DataFrames
for ic50 in inhibitory_ec50_values:
    effect = inhibitory_emax_model(
        df["Concentration (mg/L)"].to_numpy(),
        imax=100,
        ic50=ic50,
        e0=50
    )

    # Keep each EC50 result in its own DataFrame
    df_inhibitory_ec50 = df.copy()
    df_inhibitory_ec50["Effect"] = effect
    dfs_inhibitory_ec50.append(df_inhibitory_ec50)

# Plot the effect-concentration profiles for different EC50 values
plot_effect_concentration(
    dfs_inhibitory_ec50,
    labels=[f"IC50 = {ic50} mg/L" for ic50 in inhibitory_ec50_values],
    title="Effect-Concentration Profiles for Different Inhibitory EC50 Values",
    filename=str(FIGURES_DIR / "inhibitory_ec50_comparison.png")
)


