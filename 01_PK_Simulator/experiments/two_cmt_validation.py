from pathlib import Path
import sys
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_two_cmt
from pk_analysis import analyse_pk
from pk_plotting import plot_pk

# ============================================================================
# Two-Compartment Model Validation with q=0 (no inter-compartmental transfer)
# ============================================================================

df = simulate_two_cmt(
    dose=100,
    vd1=10,
    vd2=20,
    q=0,
    cl=1,
    duration=24,
    interval=0.1
)

cmax, tmax, auc = analyse_pk(df)

df["log(Concentration (mg/L))"] = np.log(df["Concentration (mg/L)"])

plot_pk(
    df,
    title="Two-Compartment Model Validation",
    xlabel="Time (hr)",
    ylabel="log(Concentration (mg/L))",
    filename=str(
        Path(__file__).resolve().parents[1]
        / "figures"
        / "two_cmt_validation.png"
    )
)
