"""Run file for 1st order linear ODE pharmokinetic model.
Authors: SABS R3 Group 2
20.10.2021

usage: python run.py
"""

import pkmodel as pk

protocol = pk.Protocol('pkmodel/config_file.txt')
model = protocol.generate_model()
x = model.solve()

x.output()


