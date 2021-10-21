import numpy as np
import scipy.integrate
from .solution import Solution
from .AbstractModel import AbstractModel


class Model(AbstractModel):
    def __init__(self, parameters):
        self.parameters = parameters
        self.name = parameters['name']
        self.nr_compartments = parameters['nr_compartments']
        self.CL = parameters['CL']
        self.V_c = parameters['V_c']
        self.X = parameters['X']
        self.dose = parameters['dose']
        self.base_compartments = 0

    def generate_transition(self, parameter_tuple, q_central, q_peripheral):
        (V_peripheral, Q_peripheral) = parameter_tuple
        transition = Q_peripheral * (q_central / self.V_c
                                     - q_peripheral / V_peripheral)
        return transition

    def solve(self):
        t_eval = np.linspace(0, 1, 1000)
        y0 = np.array(np.zeros(
                     (self.nr_compartments + self.base_compartments)))
        sol = scipy.integrate.solve_ivp(fun=lambda t, y: self.rhs(t, y),
                                        t_span=[t_eval[0], t_eval[-1]],
                                        y0=y0,
                                        t_eval=t_eval)
        return Solution(sol)


class IntravenousModels(Model):
    """Class for the intravenous bolus model -i.e. 1 peripheral compartment."""
    def __init__(self, parameters):
        super().__init__(parameters)
        self.base_compartments = 1

    def rhs(self, t, y):
        q = y
        transitions = [0.]        # Placeholder in list for dqc_dt
        sum_of_transitions = 0.
        for i in range(1, self.nr_compartments + 1):
            key = f'periph_{i}'
            transition = self.generate_transition(self.parameters[key],
                                                  q[0],
                                                  q[i])
            transitions.append(transition)
            sum_of_transitions += transition
        dqc_dt = (self.dose(t, self.X) - q[0] / (self.V_c * self.CL)
                  - sum_of_transitions)
        transitions[0] = dqc_dt        # prepend dqc_dt to list of dq_dt
        dq_dt = transitions
        return dq_dt


class SubcutaneousModels(Model):
    """Class for the subcutaneous model -i.e. 2 peripheral compartment."""
    def __init__(self, parameters):
        super().__init__(parameters)
        self.k_a = parameters['k_a']
        self.base_compartments = 2

    def rhs(self, t, y):
        q = y
        transitions = [0., 0.]  # Placeholder [dq0_dt, dqc_dt, ... ]
        sum_of_transitions = 0.
        dq0_dt = self.dose(t, self.X) - self.k_a * q[0]
        for i in range(1, self.nr_compartments + 1):
            key = f'periph_{i}'
            transition = self.generate_transition(self.parameters[key],
                                                  q[1],
                                                  q[i])
            transitions.append(transition)
            sum_of_transitions += transition
        dqc_dt = ((self.k_a * q[0]) - q[1] / (self.V_c * self.CL)
                  - sum_of_transitions)
        transitions[0] = dq0_dt        # prepend dq0_dt to list of dq_dt
        transitions[1] = dqc_dt        # prepend dqc_dt to list of dq_dt
        dq_dt = transitions
        return dq_dt
