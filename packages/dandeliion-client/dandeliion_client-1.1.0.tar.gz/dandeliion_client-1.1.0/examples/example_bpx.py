import dandeliion.client as dandeliion
import numpy as np
import matplotlib.pyplot as plt
from pybamm import Experiment

# Authentication - exact implementation is up to the API creators.
# One of the ways to define the simulator object can be the following:
api_url = "https://server-address"
api_key = "some_hash"
simulator = dandeliion.Simulator(api_url, api_key)

# A valid BPX file with battery cell parameters (json-file)
params = "examples/AE_gen1_BPX.json"

# PyBaMM Experiment object, for example:
experiment = Experiment(
    [
        (
            "Discharge at 10 A for 200 seconds",
            "Rest for 10 seconds",
            "Charge at 6 A for 100 seconds",
        )
    ]
    * 2,
    period="1 second",  # Optional
)

# Number of mesh points in PyBaMM format (default is 16 mesh points everywhere):
var_pts = {"x_n": 16, "x_s": 8, "x_p": 16, "r_n": 16, "r_p": 16}

# A list of output times (optional)
t_eval = np.arange(0, 3600, 1)

# The solution object
solution = dandeliion.solve(
    simulator=simulator,
    params=params,
    model="DFN",  # Optional, default is "DFN". Translate this into the "User-defined" section, "DandeLiion: Model" key
    experiment=experiment,  # Optional, default is 1C discharge. Translate this into the "DandeLiion: Experiment" section
    var_pts=var_pts,  # Optional. Default is 16 pts everywhere. To be translated into the "DandeLiion: Mesh" section
)

# Print all available keys in the solution object.
# Here method `keys()` is used to get all available keys in the solution object.
for key in sorted(solution.keys()):
    print(key)

# Print the final values of time, voltage, and temperature
print(f"Final time [s]: {solution['Time [s]'][-1]}")
print(f"Final voltage [V]: {solution['Voltage [V]'][-1]}")
print(f"Final temperature [K]: {solution['Temperature [K]'][-1]}")

# Plot current and voltage vs time.
# Here we access scalar values vs time.
fig, axs = plt.subplots(2, 1, figsize=(10, 8))
axs[0].plot(solution["Time [s]"], solution["Current [A]"], label="Dandeliion")
axs[0].set_xlabel("time [s]")
axs[0].set_title("Current [A]")
axs[0].legend()
axs[0].grid()
axs[1].plot(solution["Time [s]"], solution["Voltage [V]"], label="Dandeliion")
axs[1].set_xlabel("time [s]")
axs[1].set_title("Voltage [V]")
axs[1].legend()
axs[1].grid()
plt.tight_layout()
plt.show()

# Concentration in the electrolyte vs `x` at the last time step.
# Here we access spatially dependent values vs time.
plt.plot(
    solution["Electrolyte x-coordinate [m]"] * 1e6,
    solution["Electrolyte concentration [mol.m-3]"][-1],
    label="Dandeliion",
)
plt.xlabel(r"x [$\mu$m]")
plt.title("Electrolyte conc. (end of experiment) [mol.m-3]")
plt.legend()
plt.grid()
plt.show()

# If the user needs the solution at the `t_eval` times, the following code can be used:
V = solution["Voltage [V]"](t=t_eval)

