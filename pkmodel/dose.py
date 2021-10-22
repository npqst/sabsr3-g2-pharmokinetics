def select_dose(key):
    if key == 'normal':
        return unit_fn_dose
    elif key == 'spike':
        return spike_series_dose
    elif key == 'pulse':
        return pulse_series_dose
    elif key == 'zero':
        return zero_dose
    else:
        raise Exception('Incorrect dose key provided')


def unit_fn_dose(t, X):
    return X


def spike_series_dose(t, X, spike_interval=100):
    if t % spike_interval == 0:
        return X
    else:
        return 0.


def pulse_series_dose(t, X1, X2=0., pulse_width=100, interval=100):
    if t % (pulse_width + interval) < pulse_width:
        return X1
    else:
        return X2


def zero_dose(t, X):
    return 0.
