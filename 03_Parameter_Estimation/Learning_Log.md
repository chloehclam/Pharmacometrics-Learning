# Module 3: Learning Log

This log records the reasoning, observations and lessons from my parameter estimation experiments. It focuses not only on what I implemented, but also on why I chose each approach, what the results revealed and what I would investigate further.

## 1. One-compartment parameter estimation

**Main question:** Can I recover known PK parameters from noisy concentration-time observations?

**What I learned**

- Parameter estimation reverses the forward simulation process.
- Nonlinear optimisation estimates parameters by minimising the difference between observed and predicted concentrations.
- Initial estimates and parameter bounds can influence the optimisation.
- A good-looking fitted curve does not necessarily mean that all parameters have been accurately recovered.

**Reflection**

I initially thought parameter estimation was mainly about finding a curve that matched the observations. I learned that the estimated parameters themselves also need to be evaluated, particularly their uncertainty and sensitivity to the data.

## 2. Residual error and model evaluation

**Main question:** How does simulated residual variability affect observed data and model evaluation?

**What I learned**

- Simulated observations are not identical to model predictions once residual error is introduced.
- Proportional residual error means that the magnitude of variability increases with concentration.
- Residual plots can reveal systematic patterns that may not be apparent from the fitted concentration-time profile.
- MAE and RMSE summarise prediction error, but do not independently establish that the model is appropriate.

**Reflection**

I learned to distinguish between fitting the data and evaluating whether the model adequately describes the data. A low error metric should not replace visual diagnostics and scientific interpretation.

## 3. Sampling time selection

**Main question:** Does the timing of observations affect parameter estimation?

**What I learned**

- Early and late observations provide different information about the concentration-time profile.
- Sampling only in one part of the profile can leave other aspects of the model poorly characterised.
- The number of observations is not the only consideration. Their timing matters.

**Reflection**

This introduced me to the idea that sampling design is not simply about collecting as many observations as possible. It is about collecting informative observations.

## 4. One-compartment parameter recovery using Monte Carlo simulation

**Main question:** Is the fitting procedure reliable across different noisy datasets?

**What I learned**

Monte Carlo simulation involves repeatedly generating random datasets and evaluating the results across many replicates.

I used the following metrics:

- **Bias:** Measures systematic deviation from the true parameter.
- **Empirical SD:** Measures variability of estimates across repeated simulations.
- **RMSE:** Combines bias and variability into an overall measure of estimation error.
- **Mean estimated SE:** Summarises uncertainty estimated by the fitting procedure.

**Reflection**

I learned why one successful fit is not enough to evaluate an estimation method. Different noisy datasets can produce different estimates, and repeated simulations help quantify this variability.

I also learned that empirical variability and model-estimated uncertainty are not necessarily identical. Comparing them helps assess whether covariance-based standard errors are representative of the observed estimation variability.

## 5. Two-compartment parameter estimation

**Main question:** What changes when I estimate a more complex compartmental model?

**What I learned**

- A two-compartment model requires estimating four parameters: \(V_c\), \(V_p\), \(Q\) and \(CL\).
- Parameters can influence the concentration-time profile in interdependent ways.
- The covariance matrix provides information about parameter uncertainty and correlations.
- Strong parameter correlations can indicate poor identifiability.

**Observation**

In one fitting example, the correlation between \(V_p\) and \(CL\) was approximately -0.54.

**Reflection**

I realised that a model can reproduce the concentration-time profile reasonably well while individual parameters remain uncertain. This is particularly important for more complex models, where several parameter combinations may produce similar predictions.

## 6. Comparing two-compartment sampling schedules

**Main question:** How does sampling design affect the recovery of two-compartment PK parameters?

I compared three schedules:

- Schedule A: Balanced across early and late phases.
- Schedule B: Concentrated in the early phase.
- Schedule C: Concentrated in the later phase.

**What I learned**

- Early observations help characterise the distribution phase.
- Later observations provide information about the terminal phase.
- Early-only sampling performed poorly, particularly for \(V_p\).
- A schedule covering both phases provided more reliable parameter estimates in the experiments.

**Reflection**

This was one of the most important experiments in the module. I learned that sampling design should be informed by the underlying PK behaviour. Simply increasing the number of observations in one phase does not necessarily improve the estimation of all model parameters.

## 7. Two-compartment parameter recovery using Monte Carlo simulation

**Main question:** Which sampling schedule provides the most reliable parameter recovery across repeated noisy datasets?

I performed 200 fitting replicates for each of the three sampling schedules, giving up to 600 fitting attempts.

**What I learned**

- Monte Carlo simulation provides a more robust comparison than fitting a single noisy dataset.
- Schedule A had the lowest RMSE across all four parameters in the latest bounded experiment.
- Schedule B performed particularly poorly for \(V_p\).
- Schedule C performed better than Schedule B overall, but did not outperform Schedule A.
- The results demonstrated how insufficient sampling information can affect parameter recovery.

**Important technical issues encountered**

Some fits produced extremely large standard errors and unstable estimates. Some optimisation attempts failed to converge, and the Euler simulator generated overflow and invalid-value warnings when extreme parameter values were explored.

This helped me distinguish between:

- Poor parameter identifiability due to insufficient information in the sampling schedule.
- Numerical instability caused by extreme parameter combinations during optimisation.
- Optimisation convergence, which does not necessarily guarantee reliable parameter estimates.

**Reflection**

This experiment made me realise that successful model fitting is not simply about whether the optimiser returns a result. I need to investigate the estimates, their uncertainty, correlations, convergence behaviour and numerical stability.

It also showed me that parameter bounds can help constrain optimisation, but they should not be used to hide an underlying identifiability problem.

## Overall Reflection

The main conceptual progression in this module was moving from fitting a single simulated dataset to evaluating the reliability of parameter estimation across repeated simulations.

I learned that:

1. Parameter estimation is influenced by residual error and sampling design.
2. Parameter uncertainty and correlation are important when interpreting fitted models.
3. Monte Carlo simulation can reveal bias, variability and instability that are not apparent from individual fits.
4. More complex compartmental models require more informative data.
5. Numerical methods and optimisation settings can influence the reliability of estimated parameters.

## Questions to Revisit

- How do different residual error models affect parameter estimation?
- How can I distinguish poor identifiability from numerical instability more systematically?
- How do profile likelihoods compare with covariance-based standard errors?
- How can sampling times be selected using formal optimal design criteria?
- How do these concepts extend to population PK modelling, where interindividual variability and covariates are introduced?

