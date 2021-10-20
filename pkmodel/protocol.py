#
# Protocol class
#

import json
from pkmodel.models import IntravenousModels
from pkmodel.AbstractProtocol import AbstractProtocol


# TODO: move dose to appropriate location
def dose(t, X):
    return X


class Protocol(AbstractProtocol):
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self):
        self.params = {
            'name': 'model1',
            'Q_p1': 1.0,
            'V_c': 1.0,

            'V_p1': 1.0,
            'CL': 1.0,
            'X': 1.0,
            'dose': dose
        }

    def read_config(self, file_dir):
        #get current directory and add to file_dir
        config_file = open("file_dir", "r")
        dictionaries_list_str = config_file  # .split(",")
        # <-- for splitting up multipl dictionaries in the future
        # dictionaries_list = [json.loads(d) for d in dictionaries_list_str]
        dictionaries_list = json.loads(dictionaries_list_str)
        return dictionaries_list

    def fill_parameters(self, param_dicts):
        for k in self.params.keys:
            if k not in param_dicts:
                param_dicts[k] = self.params[k]
        return param_dicts

    def generate_model(self):
        return IntravenousModels(self.params)
