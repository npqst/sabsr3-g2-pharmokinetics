#
# Protocol class
#

import ast
from .models import IntravenousModels, SubcutaneousModels
from .AbstractProtocol import AbstractProtocol


# TODO: move dose to appropriate location



class Protocol(AbstractProtocol):
    """A Pharmokinetic (PK) protocol

    Parameters
    ----------

    value: numeric, optional
        an example paramter

    """
    def __init__(self, file_dir=None):
        self.params = {
            'name': 'model1',
            'V_c': 1.0,
            'periph_default': (1.0, 1.0),      # (V_p1, Q_p1)
            'CL': 1.0,
            'X': 1.0,
            'dose': 'normal',
            'nr_compartments': 1,          # nr of peripheral compartments
            'injection_type': 'intravenous'     # 'subcutaneous'
        }
        if file_dir:
            self.fill_parameters(file_dir)

    def read_config(self, file_dir):
        #get current directory and add to file_dir
        config_file = open(file_dir, "r")
        config_file_str = config_file.read()
        config_file.close()
        dictionaries_list_str = config_file_str  # .split(",")
        # <-- for splitting up multipl dictionaries in the future
        # dictionaries_list = [json.loads(d) for d in dictionaries_list_str]
        dictionaries_list = ast.literal_eval(str(dictionaries_list_str))
        return dictionaries_list

    def fill_parameters(self, file_dir):
        param_dicts = self.read_config(file_dir)
        for k in self.params.keys():
            if k not in param_dicts:
                param_dicts[k] = self.params[k]
        for i in range(1, param_dicts['nr_compartments'] + 1):
            key = f'periph_{i}'
            if key not in param_dicts:
                param_dicts[key] = self.params['periph_default']
        if (param_dicts['injection_type'] == 'subcutaneous'
                and 'k_a' not in param_dicts.keys()):
            param_dicts['k_a'] = 1.0
        self.params = param_dicts

    def generate_model(self):
        if self.params['injection_type'] == 'intravenous':
            return IntravenousModels(self.params)
        elif self.params['injection_type'] == 'subcutaneous':
            return SubcutaneousModels(self.params)
        else:
            raise Exception(
                'model type should be either intravenous or subcutaneous')
