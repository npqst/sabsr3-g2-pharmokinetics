"""Run file for 1st order linear ODE pharmokinetic model.
Authors: SABS R3 Group 2
20.10.2021

usage: python run.py $PATH_TO_CONFIG$
"""

import pkmodel as pk
import sys

arg = sys.argv
protocol = pk.Protocol(arg[1])
model = protocol.generate_model()
x = model.solve()

x.output()


