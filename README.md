# Pharmacometrics Learning

This repository documents my ongoing journey learning computational pharmacokinetics (PK) and pharmacodynamics (PD) using Python.

I started this project to strengthen my Python programming skills while developing a deeper understanding of how pharmacological concepts can be translated into quantitative models, simulations and data analysis.

The project progresses from building PK simulators to linking drug concentrations with pharmacodynamic effects and estimating model parameters from simulated data.

## Modules

### 1. Pharmacokinetics

- One-compartment IV bolus models
- First-order drug elimination
- Oral absorption with first-order absorption and elimination
- Clearance, volume of distribution and elimination half-life
- AUC, Cmax and Tmax
- Multiple IV dosing and superposition
- IV infusion
- Steady-state concentrations and loading doses
- Comparison of dosing regimens and PK parameters
- Numerical simulation using Euler's method

### 2. Pharmacodynamics and PK/PD

- Emax model
- Inhibitory Emax model
- Concentration-effect relationships
- Effect-time profiles
- Linking simulated PK profiles to pharmacodynamic effects

### 3. Parameter Estimation and Model Evaluation

- Simulating noisy concentration-time data
- Sampling concentration data at selected time points
- Estimating PK parameters using nonlinear least squares
- Evaluating model fit using residuals, MAE and RMSE
- Calculating parameter uncertainty using covariance matrices
- Investigating parameter correlations and identifiability
- One- and two-compartment parameter estimation
- Monte Carlo parameter recovery
- Comparing two-compartment sampling schedules using bias, empirical variability and RMSE

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
│
├── 02_PKPD/
│
├── 03_Parameter_Estimation/
│   ├── README.md
│   ├── Learning_Log.md
│   ├── fitting.py
│   ├── noise.py
│   ├── residual.py
│   ├── sampling.py
│   ├── main.py
│   ├── two_cmt.py
│   └── figures/
│
├── README.md
```

The structure above highlights the main project components. Individual experiment scripts and generated outputs may be organised within their respective module folders.

## Learning Goals

My goal is to build a strong foundation in computational pharmacology by developing, testing and interpreting quantitative models.

Future directions include:

- More advanced PK/PD modelling
- Parameter estimation for additional administration routes and model structures
- Population pharmacokinetics
- Interindividual variability and covariate analysis
- Exposure-response modelling
- Simulation-based dose optimisation

## Learning Documentation

Each module includes a technical README describing its objectives, methods, experiments, results and limitations.

A separate learning log records the reasoning behind each experiment, key observations, conceptual lessons and questions for further investigation.

