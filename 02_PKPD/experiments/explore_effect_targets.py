# import necessary libraries
from pathlib import Path
import sys

# Locate the project folders relative to this script
project_dir = Path(__file__).resolve().parents[1]  # 02_PKPD
simulator_dir = project_dir.parent / "01_PK_Simulator"

# Make both folders available for imports
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(simulator_dir))

from pd_models import simulate_emax_curve
from pkpd_analysis import concentration_for_effect
from pkpd_plotting import plot_effect_concentration

FIGURES_DIR = project_dir / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Find the conencentration required to achieve a desired effect using the Emax model
desired_effects = [30, 50, 70]

target_concentrations = [
    concentration_for_effect(
        effect=effect,
        emax=100,
        ec50=5,
        e0=0,
    )
    for effect in desired_effects
]

# Each point is (concentration, effect), as expected by plot_pkpd.
target_points = list(zip(target_concentrations, desired_effects))

curve_df = simulate_emax_curve(
    target_concentrations=target_concentrations,
    emax=100,
    ec50=5,
    e0=0,
)

plot_effect_concentration(
    curve_df,
    title="Emax Effect-Concentration Profile",
    filename=str(FIGURES_DIR / "effect_concentration_profile.png"),
    target_points=target_points,
)




