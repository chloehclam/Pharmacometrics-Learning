from pathlib import Path
import sys
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pk_simulator import simulate_iv_bolus, simulate_two_cmt, two_cmt_ode

#============================================================================
# Quantify the error between the two-compartmental model (Euler's method) and the one-compartmental model
#============================================================================

# dt = 1 hr
df_cmt_1 = simulate_two_cmt(
    dose=100,
    vd1=10,
    vd2=20,
    q=0,
    cl=2,
    duration=24,
    interval=1,
)

df_1 = simulate_iv_bolus(
    dose=100,
    vd=10,
    cl=2,
    duration=24,
    interval=1,
)

error_1 = np.abs(df_cmt_1['Concentration Central (mg/L)'] - df_1['Concentration (mg/L)'])

max_error_1 = np.max(error_1)


# dt = 0.1 hr

df_cmt_01 = simulate_two_cmt(
    dose=100,
    vd1=10,
    vd2=20,
    q=0,
    cl=2,
    duration=24,
    interval=0.1,
)

df_01 = simulate_iv_bolus(
    dose=100,
    vd=10,
    cl=2,
    duration=24,
    interval=0.1,
)

error_01 = np.abs(df_cmt_01['Concentration Central (mg/L)'] - df_01['Concentration (mg/L)'])

max_error_01 = np.max(error_01)


# dt = 0.01 hr
df_cmt_001 = simulate_two_cmt(
    dose=100,
    vd1=10,
    vd2=20,
    q=0,
    cl=2,
    duration=24,
    interval=0.01,
)

df_001 = simulate_iv_bolus(
    dose=100,
    vd=10,
    cl=2,
    duration=24,
    interval=0.01,
)  

error_001 = np.abs(df_cmt_001['Concentration Central (mg/L)'] - df_001['Concentration (mg/L)'])

max_error_001 = np.max(error_001)



# Solve the two-compartmental model using ODE solver and compare with Euler's method

# dt = 1 hr
amount_1 = two_cmt_ode(
    amounts=(100, 0),
    vd1=10,
    vd2=20,
    q=0,
    cl=2,
)

solved_1 = integrate.solve_ivp(
    fun=lambda t, y: two_cmt_ode(
        amounts=y,
        vd1=10,
        vd2=20,
        q=0,
        cl=2,
    ),
    t_span=(0, 24),
    y0=[100, 0],
    t_eval=np.arange(0, 25, 1),
    method="RK45",
)

df_ode_1 = pd.DataFrame({
    "Time (hr)": solved_1.t,
    "Concentration Central (mg/L)": solved_1.y[0] / 10,
})

error_ode_1 = np.abs(df_ode_1['Concentration Central (mg/L)'] - df_1['Concentration (mg/L)'])
max_error_ode_1 = np.max(error_ode_1)

# dt = 0.1 hr
amount_01 = two_cmt_ode(
    amounts=(100, 0),
    vd1=10,
    vd2=20,
    q=0,
    cl=2,
)

solved_01 = integrate.solve_ivp(
    fun=lambda t, y: two_cmt_ode(
        amounts=y,
        vd1=10,
        vd2=20,
        q=0,
        cl=2,
    ),
    t_span=(0, 24),
    y0=[100, 0],
    t_eval=np.arange(0, 24.1, 0.1),
    method="RK45",
)

df_ode_01 = pd.DataFrame({
    "Time (hr)": solved_01.t,
    "Concentration Central (mg/L)": solved_01.y[0] / 10,
})      

error_ode_01 = np.abs(df_ode_01['Concentration Central (mg/L)'] - df_01['Concentration (mg/L)'])
max_error_ode_01 = np.max(error_ode_01)

# dt = 0.01 hr
amount_001 = two_cmt_ode(
    amounts=(100, 0),
    vd1=10,
    vd2=20,
    q=0,
    cl=2,
)

solved_001 = integrate.solve_ivp(
    fun=lambda t, y: two_cmt_ode(
        amounts=y,
        vd1=10,
        vd2=20,
        q=0,
        cl=2,
    ),
    t_span=(0, 24),
    y0=[100, 0],
    t_eval=np.arange(0, 24.01, 0.01),
    method="RK45",
)

df_ode_001 = pd.DataFrame({
    "Time (hr)": solved_001.t,
    "Concentration Central (mg/L)": solved_001.y[0] / 10,
})

error_ode_001 = np.abs(df_ode_001['Concentration Central (mg/L)'] - df_001['Concentration (mg/L)'])
max_error_ode_001 = np.max(error_ode_001)

# plot the error between the ODE solver and one compartmental model for different dt values
plt.figure(figsize=(8, 6))
dt_values = [1, 0.1, 0.01]
max_errors = [max_error_1, max_error_01, max_error_001]
slope = (np.log(max_error_001) - np.log(max_error_1)) / (np.log(0.01) - np.log(1))

max_errors_ode = [max_error_ode_1, max_error_ode_01, max_error_ode_001]
slope_ode = (np.log(max_error_ode_001) - np.log(max_error_ode_1)) / (np.log(0.01) - np.log(1))

plt.plot(dt_values, max_errors, marker='o', label=f'Euler: slope = {slope:.2f}')
plt.plot(dt_values, max_errors_ode, marker='o', label=f'ODE Solver: slope = {slope_ode:.2f}')
plt.xscale('log')
plt.yscale('log')
plt.xlabel('log(dt) (hr)')
plt.ylabel('log(maximum error) (mg/L)')
plt.title('Maximum Error vs Time Step (ODE Solver)')
plt.legend()
plt.grid(True, which="both", ls="--")
plt.savefig(
    str(
        Path(__file__).resolve().parents[1]
        / "figures"
        / "euler_error_ode.png"
    )
)

def print_error_summary(method, dt, df, errors):
    max_index = np.argmax(errors)
    print(
        f"{method}, dt={dt:g} hr | "
        f"max error={errors[max_index]:.4g} mg/L at {df['Time (hr)'].iloc[max_index]:g} hr | "
        f"mean error={np.mean(errors):.4g} mg/L"
    )

print_error_summary("Euler", 1, df_cmt_1, error_1)
print_error_summary("Euler", 0.1, df_cmt_01, error_01)
print_error_summary("Euler", 0.01, df_cmt_001, error_001)

print_error_summary("ODE solver", 1, df_ode_1, error_ode_1)
print_error_summary("ODE solver", 0.1, df_ode_01, error_ode_01)
print_error_summary("ODE solver", 0.01, df_ode_001, error_ode_001)



