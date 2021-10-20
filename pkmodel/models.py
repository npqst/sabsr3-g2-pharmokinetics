import numpy as np
import scipy.integrate
from Solution import Solution
from AbstractModel import AbstractModel


class IntravenousModels(AbstractModel):
    """Class for the intravenous bolus model -i.e. 1 peripheral compartment."""
    def __init__(self, parameters):
        self.parameters = parameters
        self.CL = parameters['CL']
        self.V_c = parameters['V_c']
        self.V_p1 = parameters['V_p1']
        self.Q_p1 = parameters['Q_p1']
        self.X = parameters['X']
        self.dose = parameters['dose']

    def rhs(self, t, y):
        q_c, q_p1 = y
        transition = self.Q_p1 * (q_c / self.V_c - q_p1 / self.V_p1)
        dqc_dt = self.dose(t, self.X) - q_c / self.V_c * self.CL - transition
        dqp1_dt = transition
        return [dqc_dt, dqp1_dt]

    def solve(self):
        t_eval = np.linspace(0, 1, 1000)
        y0 = np.array([0.0, 0.0])
        sol = scipy.integrate.solve_ivp(fun=lambda t, y: self.rhs(t, y),
                                        t_span=[t_eval[0], t_eval[-1]],
                                        y0=y0,
                                        t_eval=t_eval)
        return Solution(sol)


class SubcutaneousModels(AbstractModel):
    """Class for the subcutaneous model -i.e. 2 peripheral compartment."""
    def __init__(self, parameters):
        self.parameters = parameters
        self.CL = parameters['CL']
        self.V_c = parameters['V_c']
        self.V_p1 = parameters['V_p1']
        self.Q_p1 = parameters['Q_p1']
        self.k_a = parameters['k_a']
        self.X = parameters['X']
        self.dose = parameters['dose']

    def rhs(self, t, y):
        q_c, q_p1, q_0 = y
        dq0_dt = self.dose(t, X) - self.k_a * q_0
        transition = self.Q_p1 * (q_c / self.V_c - q_p1 / self.V_p1)
        dqc_dt = self.k_a * q_0 - q_c / self.V_c * self.CL - transition
        dqp1_dt = transition
        return [dq0_dt, dqc_dt, dqp1_dt]

    def solve(self):
        t_eval = np.linspace(0, 1, 1000)
        y0 = np.array([0.0, 0.0])
        sol = scipy.integrate.solve_ivp(fun=lambda t, y: self.rhs(t, y),
                                        t_span=[t_eval[0], t_eval[-1]],
                                        y0=y0,
                                        t_eval=t_eval)
        return Solution(sol)
