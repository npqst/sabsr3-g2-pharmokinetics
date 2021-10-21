"""models.py contains Model baseclass and Intravenous and Subcutaneous
model subclasses.

:return: solution to PK ODE Model
:rtype: Solution object
"""

import numpy as np
import scipy.integrate
from .solution import Solution
from .AbstractModel import AbstractModel
from .dose import select_dose


class Model(AbstractModel):
    """Base model for PK 1st order linear ODE model with variable
    number of peripheral compartments.

    :param parameters: parameters and constants of the model
    :type parameters: dict
    """
    def __init__(self, parameters):
        """Constructor for base model of PK 1st order linear ODE model
        with variable number of peripheral compartments.

        :param parameters: parameters and constants of the model
        :type parameters: dict
        """
        self.parameters = parameters
        self.name = parameters['name']
        self.nr_compartments = parameters['nr_compartments']
        self.CL = parameters['CL']
        self.V_c = parameters['V_c']
        self.X = parameters['X']
        self.dose = select_dose(parameters['dose'])
        self.base_compartments = 0

    def generate_transition(self, parameter_tuple, q_central, q_peripheral):
        """Helper function computes single transition equation
        describing flux between central compartment and single
        peripheral compartment.

        :param parameter_tuple: (V_peripheral, Q_peripheral) - tuple
        containing volume and rate constants that define a peripheral
        compartment
        :type parameter_tuple: tuple of non-negative floats
        :param q_central: time variable amount q in central compartment
        solved numerically at time t
        :type q_central: float
        :param q_peripheral: time variable amount q in peripheral compartment
        solved numerically at time t
        :type q_peripheral: float
        :return: computed transition value describing flux between central
        and peripheral compartment at time t
        :rtype: float
        """
        (V_peripheral, Q_peripheral) = parameter_tuple
        transition = Q_peripheral * (q_central / self.V_c
                                     - q_peripheral / V_peripheral)
        return transition

    def solve(self):
        """Function computes the numeric solution of the PK ODE model with
        scipy solve_ivp for a specified time interval.

        :return: numeric solution of amount for each compartment as float
        array with dimensions N x T, where N is the total number of
        compartments and T is the length of the time eval vector.
        :rtype: Solution
        """
        t_eval = np.linspace(0, 1, 1000)
        y0 = np.array(np.zeros(
                     (self.nr_compartments + self.base_compartments)))
        sol = scipy.integrate.solve_ivp(fun=lambda t, y: self.rhs(t, y),
                                        t_span=[t_eval[0], t_eval[-1]],
                                        y0=y0,
                                        t_eval=t_eval)
        if not isinstance(sol, float):
            raise TypeError('Solution should be a float.')
        if np.any(sol < 0):
            raise ValueError('Solution should be non-negative.')
        return Solution(sol, self.parameters)


class IntravenousModels(Model):
    """Class for the intravenous bolus model with a single central compartment
    and variable number of peripheral compartments"""
    def __init__(self, parameters):
        """Constructor for intravenous model, which inherits from Model superclass.
        Intravenous model has a single base compartment (the
        central compartment)

        :param parameters: parameters and constants of the model
        :type parameters: dict
        """
        super().__init__(parameters)
        self.base_compartments = 1

    def rhs(self, t, y):
        """Right Hand Side (rhs) of the ODE model.
        Contains the implementation of the differential equations
        defining the PK model.
        $dq_c / dt = Dose(t) - \frac{q_c}{V_c}CL
                - Q_{px}(\frac{q_c}{V_c} - \frac{q_{px}}{V_{px}})$
        $dq_px / dt = Q_{px}(\frac{q_c}{V_c} - \frac{q_{px}}{V_{px}})$
        Called as lambda function within scipy solve_ivp.

        :param t: current time point
        :type t: float
        :param y: [q_c, q_p1, ..., q_pn] - current amount in compartment at
        time point t
        :type y: array of float with dimensions N
        where N is total number of compartments
        :return: dq_dt - an array of all compartments' dq_dt values at time t
        :rtype: array of float with dimensions N
        where N is total number of compartments
        """
        q = y
        transitions = [0.]        # Placeholder in list for dqc_dt
        sum_of_transitions = 0.
        for i in range(1, self.nr_compartments + 1):
            # create key to access parameter values for each compartment
            key = f'periph_{i}'
            # compute each peripheral compartment's transition to
            # the central compartment
            transition = self.generate_transition(self.parameters[key],
                                                  q[0],
                                                  q[i])
            transitions.append(transition)
            sum_of_transitions += transition
        # compute central compartment's amount rate of change at time t
        dqc_dt = (self.dose(t, self.X) - q[0] / (self.V_c * self.CL)
                  - sum_of_transitions)
        transitions[0] = dqc_dt        # prepend dqc_dt to list of dq_dt
        dq_dt = transitions
        return dq_dt


class SubcutaneousModels(Model):
    """Class for the subcutaneous injection model with a single
    central compartment, a single absorption compartment, and
    variable number of peripheral compartments
    """

    def __init__(self, parameters):
        """Constructor for subcutaneous model, which inherits from Model superclass.
        Subcutaneous model has a two base compartments (the
        central compartment and the absorption compartment)
        Absorption rate to the central compartment is k_a.

        :param parameters: parameters and constants of the model
        :type parameters: dict
        """
        super().__init__(parameters)
        self.k_a = parameters['k_a']
        self.base_compartments = 2

    def rhs(self, t, y):

        """Right Hand Side (rhs) of the ODE model.
        Contains the implementation of the differential equations
        defining the PK model.
        $dq0 / dt = Dose(t) - k_{a}q_0 $
        $dq_c / dt = k_{a}q_0 - \frac{q_c}{V_c}CL
                        - Q_{px}(\frac{q_c}{V_c} - \frac{q_{px}}{V_{px}})$
        $dq_px / dt = Q_{px}(\frac{q_c}{V_c} - \frac{q_{px}}{V_{px}})$
        Called as lambda function within scipy solve_ivp.

        :param t: current time point
        :type t: float
        :param y: [q_0, q_c, q_p1, ..., q_pn] - current amount in
        compartment at time point t
        :type y: array of float with dimensions N
        where N is total number of compartments
        :return: dq_dt - an array of all compartments' dq_dt values at time t
        :rtype: array of float with dimensions N
        where N is total number of compartments
        """

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

