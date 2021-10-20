import matplotlib.pylab as plt
import numpy as np
import scipy.integrate

def dose(t, X):
    """The input dose."""
    return X

class intravenous_bolus:
    """Class for the intravenous bolus model -i.e. 1 peripheral compartment."""
    def __init__(self, Q_p1=1.0, V_c=1.0, V_p1=1.0, CL=1.0, X=1.0):
        self.dose=dose

    def make_model(self, Q_p1=1.0, V_c=1.0, V_p1=1.0, CL=1.0, X=1.0):
        q_c, q_p1 = y
        transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
        dqc_dt = dose(t, X) - q_c / V_c * CL - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt]

class subcutaneous:
    """Class for the subcutaneous model -i.e. 2 peripheral compartment."""
    def __init__(self, Q_p1=1.0, V_c=1.0, V_p1=1.0, CL=1.0, q_0=1.0, k_a=1.0, X=1.0):

    def make_model(self, Q_p1=1.0, V_c=1.0, V_p1=1.0, CL=1.0, q_0=1.0, k_a=1.0, X=1.0):
        q_c, q_p1 = y
        q_0=y2
        transition = Q_p1 * (q_c / V_c - q_p1 / V_p1)
        dq0_dt = dose(t, X) -k_a*q_0
        dqc_dt = k_a*q_0 - q_c / V_c * CL - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt]
