# Pharmacometrics Learning

This repository documents my ongoing journey learning computational pharmacokinetics (PK) and pharmacodynamics (PD) using Python.

I started this project to strengthen my Python programming skills while developing a deeper understanding of how pharmacological concepts can be translated into quantitative models, simulations, and data analysis.

The project progresses from building PK simulators to linking drug concentrations with pharmacodynamic effects and estimating model parameters from simulated data.

## Current Topics

### 1. Pharmacokinetics

- One-compartment IV bolus models
- First-order drug elimination
- Oral absorption with first-order absorption and elimination
- Clearance, volume of distribution, and elimination half-life
- Area under the concentration-time curve (AUC), maximum concentration (Cmax), and time to maximum concentration (Tmax)
- Multiple IV dosing and superposition
- IV infusion
- Steady-state concentrations and loading doses
- Comparison of dosing regimens and PK parameters
- Numerical simulation using Euler's method

### 2. Pharmacodynamics

- Emax model
- Inhibitory Emax model
- Concentration-effect relationships
- Effect-time profiles
- Linking simulated PK profiles to pharmacodynamic effects

### 3. Parameter Estimation and Model Evaluation

*In progress*

- Simulating noisy concentration-time data
- Sampling concentration data at selected time points
- Estimating PK parameters using nonlinear least squares
- Comparing unweighted and proportional residual weighting
- Calculating parameter uncertainty from the estimated covariance matrix
- Evaluating model fit using residuals, mean absolute error (MAE), and root mean squared error (RMSE)
- Investigating parameter estimation performance across repeated simulations

## Tools and Libraries

- Python
- NumPy
- pandas
- Matplotlib
- SciPy

## Project Structure

```text
Pharmacometrics-Learning/
│
├── 01_PK_Simulator/
│   ├── pk_simulator.py
│   ├── pk_analysis.py
│   ├── pk_plotting.py
│   ├── main.py
│   ├── experiments/
│   └── figures/
│
├── 02_PKPD/
│   ├── pd_models.py
│   ├── pkpd_analysis.py
│   ├── pkpd_plotting.py
│   ├── main.py
│   ├── experiments/
│   └── figures/
│
├── 03_Parameter_Estimation/
│   ├── fitting.py
│   ├── noise.py
│   ├── residual.py
│   ├── sampling.py
│   ├── main.py
│   └── figures/
│
└── README.md
```

## Learning Goals

My goal is to build a strong foundation in computational pharmacology by developing, testing, and interpreting quantitative models. Future directions include more advanced PK/PD modelling, population pharmacokinetics, and exposure-response analysis.