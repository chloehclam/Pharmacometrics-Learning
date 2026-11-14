from pathlib import Path
import sys
import numpy as np

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
# Monte Carlo simulation to evaluate the effect of different sampling schedules on 
# parameter estimation for a two-compartmental IV bolus model
#==============================================================
# Define the sampling schedules
schedules = [[0.2, 0.5, 1, 2, 4, 8, 12, 24],
             [0.2, 0.5, 1, 1.5, 2, 2.5, 3, 4],
             [1, 2, 4, 6, 8, 12, 18, 24]]

# Define a two-compartmental iv bolus model for fitting
model_two_cmt = lambda t, vd1, vd2, q, cl: two_cmt_iv_bolus(t, vd1, vd2, q, cl)

# Initialise a dicionary to store the results for each schedule
results = {
    "A": {
        "estimates": [],
        "standard_errors": [],
        "covariance_matrices": [],
        "correlation_matrices": [],
        "success": []
    },
    "B": {
        "estimates": [],
        "standard_errors": [],
        "covariance_matrices": [],
        "correlation_matrices": [],
        "success": []
    },
    "C": {
        "estimates": [],
        "standard_errors": [],
        "covariance_matrices": [],
        "correlation_matrices": [],
        "success": []
    }
}

# Intialise a summary dictionary to store the summary of the results for each schedule
summary = {
    "A": {
        "mean_estimates": None,
        "mean_standard_errors": None,
        "bias": None,
        "empirical_se": None,
        "rmse": None
    },
    "B": {
        "mean_estimates": None,
        "mean_standard_errors": None,
        "bias": None,
        "empirical_se": None,
        "rmse": None
    },
    "C": {
        "mean_estimates": None,
        "mean_standard_errors": None,
        "bias": None,
        "empirical_se": None,
        "rmse": None
    }
}

for i, schedule in enumerate(schedules):
    # Sample the true data at the specified time points
    df_sample = sample_at_time(
        df_true.copy(),
        schedule,
        conc="Concentration Central (mg/L)"
    )

    for j in range(200):
        rng = np.random.default_rng(42 + i + j)

        # Add noise to the sampled data
        df_sample_noisy = add_noise(
            df_sample,
            col="Concentration Central (mg/L)",
            rng=rng
        )

        try: 
            # Fit the two-compartmental model to the noisy data
            popt, pcov = fitting(
                df=df_sample_noisy,
                model=model_two_cmt,
                ycol="Concentration Central (mg/L)",
                p0=[10, 20, 2, 3],  # Initial guesses for vd1, vd2, q, cl
                bounds=[(1, 1, 0.1, 0.1), (50, 100, 20, 20)]
            )

            se = np.sqrt(np.diag(pcov))

            # Calculate the correlation matrix
            correlation_matrix = pcov / np.outer(se, se)

            # Store the results in the dictionary
            schedule_key = chr(65 + i)  # Convert index to letter A, B
            results[schedule_key]["estimates"].append(popt)
            results[schedule_key]["standard_errors"].append(se)
            results[schedule_key]["covariance_matrices"].append(pcov)
            results[schedule_key]["correlation_matrices"].append(correlation_matrix)

            results[schedule_key]["success"].append(True)

        except (RuntimeError, ValueError, np.linalg.LinAlgError) as e:
            print(f"Fitting failed for schedule {chr(65 + i)} on iteration {j}: {e}")
            results[schedule_key]["success"].append(False)

    # Calculate mean estimates and standard errors for the current schedule
    mean_estimates = np.mean(results[schedule_key]["estimates"], axis=0)
    mean_standard_errors = np.mean(results[schedule_key]["standard_errors"], axis=0)
    bias = mean_estimates - np.array([10, 20, 2, 3])  # True values for vd1, vd2, q, cl
    empirical_se = np.std(results[schedule_key]["estimates"], axis=0)
    rmse = np.sqrt(np.mean((results[schedule_key]["estimates"] - np.array([10, 20, 2, 3]))**2, axis=0))

    # Store the summary statistics in the summary dictionary
    summary[schedule_key]["mean_estimates"] = mean_estimates
    summary[schedule_key]["mean_standard_errors"] = mean_standard_errors
    summary[schedule_key]["bias"] = bias
    summary[schedule_key]["empirical_se"] = empirical_se
    summary[schedule_key]["rmse"] = rmse

def format_array(values):
    return np.array2string(
        values,
        formatter={"float_kind": lambda value: f"{value:.3f}"}
    )

print("\nSummary of parameter estimation across sampling schedules:")
for schedule_key in summary.keys():
    print(f"\nSchedule {schedule_key}:")
    print(f"Mean Estimates: {format_array(summary[schedule_key]['mean_estimates'])}")
    print(f"Mean Standard Errors: {format_array(summary[schedule_key]['mean_standard_errors'])}")
    print(f"Bias: {format_array(summary[schedule_key]['bias'])}")
    print(f"Empirical SE: {format_array(summary[schedule_key]['empirical_se'])}")
    print(f"RMSE: {format_array(summary[schedule_key]['rmse'])}")