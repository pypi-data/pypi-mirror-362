import dandeliion.client as dandeliion
import numpy as np
import matplotlib.pyplot as plt
from pybamm import Experiment

# server = "https://development.dandeliion.com"
credential = ("juser", "dandeliion")
simulator = dandeliion.Simulator(credential)

params = 'example_bpx.json'
experiment = Experiment(
    [
        (
            "Discharge at 10 A for 100 seconds",
            "Rest for 10 seconds",
            "Charge at 6 A for 100 seconds",
        )
    ]
    * 2,
    termination="250 s",
    period="1 second",
)

var_pts = {"x_n": 16, "x_s": 8, "x_p": 16, "r_n": 16, "r_p": 16}

initial_condition = (
    {
        "Initial concentration in electrolyte [mol.m-3]": 1000.0,
        "Initial state of charge": 1.0,
        "Initial temperature [K]": 298.15,
    }
)

while True:
    print('attempt')
    print(dandeliion.solve(
        simulator=simulator,
        params=params,
        model='DFN',
        experiment=experiment,
        initial_condition=initial_condition,
        var_pts=var_pts,
    ))


