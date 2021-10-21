#
# Protocol class
#

import json
from pkmodel.models import IntravenousModels, SubcutaneousModels
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
            'V_c': 1.0,
            'periph_default': (1.0, 1.0),      # (V_p1, Q_p1)
            'CL': 1.0,
            'X': 1.0,
            'dose': dose,
            'nr_compartments': 1,          # nr of peripheral compartments
            'injection_type': 'intravenous'     # 'subcutaneous'
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
        for i in range(self.params['nr_compartments']):
            key = f'periph_{i}'
            if key not in param_dicts:
                param_dicts[key] = self.params['periph_default']
        return param_dicts

    def generate_model(self):
        if self.params['injection_type'] == 'intravenous':
            return IntravenousModels(self.params)
        elif self.params['injection_type'] == 'subcutaneous':
            return SubcutaneousModels(self.params)
        else:
            raise Exception(
                'model type should be either intravenous or subcutaneous')
