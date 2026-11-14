from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt

# Locate the project folders relative to this script
project_dir = Path(__file__).resolve().parents[1]  # 03_Parameter_Estimation
simulator_dir = project_dir.parent / "01_PK_Simulator"

# Make both folders available for imports
sys.path.insert(0, str(project_dir))
sys.path.insert(0, str(simulator_dir))

from noise import add_noise
from sampling import sample_at_time
from fitting import fitting
from two_cmt import df_true, two_cmt_iv_bolus

FIGURES_DIR = project_dir / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

#==============================================================
# To evaluate the effect of different sampling schedules on parameter estimation for a two-compartmental IV bolus model
#==============================================================

# Generate three different sampling schedules for a two-compartmental IV bolus
schedules = [[0.2, 0.5, 1, 2, 4, 8, 12, 24],
             [0.2, 0.5, 1, 1.5, 2, 2.5, 3, 4],
             [1, 2, 4, 6, 8, 12, 18, 24]]

# Create lists to store the sampled data, noisy data, and parameter estimates for each schedule
dfs_sample = []
dfs_noisy = []
popts = []
pcovs = []
correlation_matrices = []

# Define a two-compartmental iv bolus model for fitting
model_two_cmt = lambda t, vd1, vd2, q, cl: two_cmt_iv_bolus(t, vd1, vd2, q, cl)

# Loop through each sampling schedule, sample the true data, add noise, and fit the model
for i, schedule in enumerate(schedules):
    # Sample the true data at the specified time points
    df_sample = sample_at_time(
        df_true.copy(),
        schedule,
        conc="Concentration Central (mg/L)"
    )

    dfs_sample.append(df_sample)

    rng = np.random.default_rng(42 + i)

    # Add noise to the sampled data
    df_sample_noisy = add_noise(
        df_sample,
        col="Concentration Central (mg/L)",
        rng=rng
    )

    dfs_noisy.append(df_sample_noisy)

    # Fit the two-compartmental model to the noisy sampled data
    popt, pcov = fitting(
        df=df_sample_noisy,
        model=model_two_cmt,
        p0=(30, 20, 5, 10),
        bounds=([0, 0, 0, 0], [np.inf, np.inf, np.inf, np.inf]),
        ycol="Concentration Central (mg/L)"
    )

    popts.append(popt)
    pcovs.append(pcov)
    
    # Calculate standard errors and estimated parameters
    vdc_se, vdp_se, q_se, cl_se = np.sqrt(np.diag(pcov))
    est_vdc, est_vdp, est_q, est_cl = popt

    # Print the estimated parameters, their standard errors, and relative errors compared to true values
    print(f"\nTwo-compartmental IV bolus parameter estimation sampled with schedule {chr(65+i)}: {schedule}")
    print(f"Estimated central Vd: {est_vdc:.3f} \u00b1 {vdc_se:.3f}  True: 10  Relative Error: {(est_vdc - 10) / 10 * 100:+.3f}%")
    print(f"Estimated peripheral Vd: {est_vdp:.3f} \u00b1 {vdp_se:.3f}   True: 20  Relative Error: {(est_vdp - 20) / 20 * 100:+.3f}%")
    print(f"Estimated intercompartmental clearance: {est_q:.3f} \u00b1 {q_se:.3f}  True: 2  Relative Error: {(est_q - 2) / 2 * 100:+.3f}%")
    print(f"Estimated clearance: {est_cl:.3f} \u00b1 {cl_se:.3f}   True: 3  Relative Error: {(est_cl - 3) / 3 * 100:+.3f}%")

    # Calculate the correlation matrix of the estimated parameters
    parameter_se = np.sqrt(np.diag(pcov))
    correlation_matrix = pcov / np.outer(parameter_se, parameter_se)

    correlation_matrices.append(correlation_matrix)

    print(f"Correlation matrix: \n{correlation_matrix}")

# Plot the true concentration profile, fitted profiles, and observed noisy data for each sampling schedule
fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)

time_grid = np.linspace(0.01, 24, 300)

for i, ax in enumerate(axes):
    ax.plot(
        df_true["Time (hr)"],
        df_true["Concentration Central (mg/L)"],
        label="True profile"
    )

    fitted_conc = two_cmt_iv_bolus(time_grid, *popts[i])

    ax.plot(
        time_grid,
        fitted_conc,
        label="Fitted profile"
    )

    ax.scatter(
        dfs_noisy[i]["Time (hr)"],
        dfs_noisy[i]["Concentration Central (mg/L)"],
        label="Observed data",
        zorder=3
    )

    ax.set_yscale("log")
    ax.set_xlabel("Time (h)")
    ax.set_title(f"Schedule {chr(65+i)}")
    ax.grid(alpha=0.3)

axes[0].set_ylabel("Concentration (mg/L)")
axes[-1].legend()

fig.suptitle("Effect of Sampling Schedule on PK Model Fitting")
fig.tight_layout()
fig.savefig(
    FIGURES_DIR / "sampling_profiles.png",
    dpi=300,
    bbox_inches="tight"
)  

# Plot the estimated parameters across sampling schedules
parameters = ["Vc", "Vp", "Q", "CL"]
true_values = np.array([10, 20, 2, 3])

estimates = np.array(popts)

standard_errors = np.array([
    np.sqrt(np.diag(pcov))
    for pcov in pcovs
])

fig, axes = plt.subplots(2, 2, figsize=(11, 8))

for j, ax in enumerate(axes.flat):

    ax.errorbar(
        ["A", "B", "C"],
        estimates[:, j],
        yerr=standard_errors[:, j],
        fmt="o",
        capsize=5
    )

    ax.axhline(
        true_values[j],
        linestyle="--",
        label="True value"
    )

    ax.set_title(parameters[j])
    ax.set_xlabel("Sampling schedule")
    ax.set_ylabel("Parameter estimate")
    ax.grid(alpha=0.3)
    ax.legend()

fig.suptitle("Parameter Estimation Across Sampling Schedules")
fig.tight_layout()

fig.savefig(
    FIGURES_DIR / "parameter_estimates.png",
    dpi=300,
    bbox_inches="tight"
)

    
