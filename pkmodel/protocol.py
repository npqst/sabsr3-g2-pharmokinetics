#
# Protocol class
#

import ast
from .models import IntravenousModels
from .AbstractProtocol import AbstractProtocol


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
    def __init__(self, file_dir=None):
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
        for i in range(self.params['nr_compartments']):
            key = f'periph_{i}'
            if key not in param_dicts:
                param_dicts[key] = self.params['periph_default']
        self.params = param_dicts

    def check_fill_parametersdict(self):
        if not isinstance(self.params, dict):
            raise TypeError('data input should be a dictionary')

    def check_fill_parametersstr(self):
        for i in 'name', 'injection_type':
            if not isinstance(self.params[i], str):
                raise TypeError('i should be a string')

    def check_fill_parameterscompartments(self):
        if not isinstance(self.params['nr_compartments'], int):
            raise TypeError('nr_compartments should be a integer')
        if self.params['nr_compartments'] < 0:
            raise ValueError('nr_compartments should be at least 0')

    def check_fill_parametersperip(self):
        if not isinstance(self.params['periph_1'], tuple):
            raise TypeError('periph_1 should be a tuple')

        for i in range(0, 1):
            if not isinstance(self.params['periph_1'][i], float):
                raise TypeError('values associated with the peripheral'
                                ' compartment should be floats')
            if self.params['periph_1'][i] < 0:
                raise ValueError('values associated with the peripheral'
                                 ' compartment should be positive')

    def check_fill_parametersCLX(self):
        for i in 'Cl', 'X':
            if not isinstance(self.params['i'], float):
                raise TypeError('i should be a float')
            if self.params[i] < 0:
                raise ValueError('i should be at least 0')

    def generate_model(self):
        if self.params['injection_type'] == 'intravenous':
            return IntravenousModels(self.params)
        elif self.params['injection_type'] == 'subcutaneous':
            return SubcutaneousModels(self.params)
        else:
            raise Exception(
                'model type should be either intravenous or subcutaneous')
