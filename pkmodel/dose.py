"""Dose functions defining the dosing regimens of pharmokinetic model.
"""


def select_dose(key):
    """Function to select dose function specified by key in config or protocol.

    :param key: ['normal', 'pulse', 'zero'] selection ID for function from
        parameters
    :type key: String
    :raises Exception: Dose key incorrect, does not point to a dose function
    :return: dose function
    :rtype: function
    """
    if key == 'normal':
        return unit_fn_dose
    elif key == 'pulse':
        return pulse_series_dose
    elif key == 'zero':
        return zero_dose
    else:
        raise Exception('Incorrect dose key provided')


def unit_fn_dose(t, X):
    """Unit step function (Heaviside) for dosing regimen, with amount X of
        dose administered at every time step.

    :param t: current time point
    :type t: float
    :param X: amount of dose administered
    :type X: float
    :return: dose X administered at time t
    :rtype: float
    """
    return X


def pulse_series_dose(t, X1, X2=0., pulse_width=0.1, interval=0.1):
    """Pulse function for dose administration, with X1 and X2 amounts
        alternately administered.

    :param t: current time point
    :type t: float
    :param X1: amount of dose administered in high pulse
    :type X1: float
    :param X2: amount of dose administered in low pulse, defaults to 0.
    :type X2: float, optional
    :param pulse_width: time duration of high pulse, defaults to 0.1
    :type pulse_width: float, optional
    :param interval: time duration of low pulse, ie interval between high
        pulses; defaults to 0.1
    :type interval: float, optional
    :return: dose administered at time t
    :rtype: float
    """
    if t % (pulse_width + interval) < pulse_width:
        return X1
    else:
        return X2


def zero_dose(t, X):
    """Dose function returns zero dose at all times.

    :param t: current time point
    :type t: float
    :param X: amount of dose administered
    :type X: float
    :return: zero
    :rtype: float
    """
    return 0.
