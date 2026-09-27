# Pharmacometrics Learning

This repository documents my ongoing journey learning computational pharmacokinetics and pharmacodynamics using Python.

I started this project to strengthen my Python skills while developing a deeper understanding of how pharmacokinetic and pharmacodynamic concepts can be translated into quantitative models and simulations.

## Current Topics

### Pharmacokinetics
- One-compartment IV bolus models
- First-order elimination
- Oral absorption with first-order absorption and elimination
- Clearance, volume of distribution, and half-life
- AUC, Cmax, and Tmax
- Multiple IV dosing and superposition
- IV infusion
- Steady-state concentration
- Loading doses
- Comparison of dosing regimens and PK parameters

### Pharmacodynamics
- Emax model
- Inhibitory Emax model
- Concentration-effect relationships
- Effect-time profiles
- Linking simulated PK profiles to pharmacodynamic effects

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
└── README.md