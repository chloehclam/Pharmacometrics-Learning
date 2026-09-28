# import necessary libraries
from pathlib import Path
import sys

# Locate the project folders relative to this script
project_dir = Path(__file__).resolve().parents[1]  # 02_PKPD
simulator_dir = project_dir.parent / "01_PK_Simulator"

# Make both folders available for imports
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(simulator_dir))

from pk_simulator import simulate_multiple_iv
from pd_models import emax_model
from pkpd_plotting import plot_effect_time

FIGURES_DIR = project_dir / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Simulate multiple IV doses to get concentration-time profile
df = simulate_multiple_iv(
    dose=100,
    vd=10,
    half_life=2,
    duration=24,
    dose_interval=4,
    simulation_interval=0.1
)

# Calculate the effect using the Emax model
df["Effect"] = emax_model(
    df["Concentration (mg/L)"].to_numpy(),
    emax=100,
    ec50=5
)

# Plot the effect-time profile for the multiple IV doses
plot_effect_time(
    df,
    title="Effect-Time Profile for Multiple IV Boluses",
    filename=str(FIGURES_DIR / "multiple_iv_effect_time.png")
)

