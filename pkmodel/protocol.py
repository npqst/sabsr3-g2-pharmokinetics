#
# Protocol class
#

import ast
from .models import IntravenousModels, SubcutaneousModels
from .AbstractProtocol import AbstractProtocol


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
            'dose_mode': 'normal',
            'nr_compartments': 1,          # nr of peripheral compartments
            'injection_type': 'intravenous',    # 'subcutaneous'
            'save_mode': 'save'
            'time': 1
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

    def check_fill_parametersdict(self):
        if not isinstance(self.params, dict):
            raise TypeError('data input should be a dictionary')

    def check_fill_parametersstr(self):
        for i in 'name', 'injection_type':
            if not isinstance(self.params[i], str):
                raise TypeError(f'{i} should be a string')

    def check_fill_parameterscompartments(self):
        if not isinstance(self.params['nr_compartments'], int):
            raise TypeError('nr_compartments should be a integer')
        if self.params['nr_compartments'] < 0:
            raise ValueError('nr_compartments should be at least 0')

    def check_fill_parametersperip(self):
        if not isinstance(self.params['periph_1'], tuple):
            raise TypeError('periph_1 should be a tuple')

        for i in range(0, 1):
            for n in len(self.params['nr_compartments']):
                if not isinstance(self.params[f'periph_{n}'][i], int):
                    raise TypeError(f'values associated with the peripheral'
                                    ' compartment should be integer')
                if self.params[f'periph_{n}'][i] < 0:
                    raise ValueError('values associated with the peripheral'
                                    f' compartment {n} should be positive')

    def check_fill_parametersCLXtime(self):
        for i in 'Cl', 'X', 'time':
            if not isinstance(self.params[i], float):
                raise TypeError(f'{i} should be a float')
            if self.params[i] < 0:
                raise ValueError(f'{i} should be at least 0')
            if i == time:
                if time > 5:
                    raise ValueError('Time should not exceed a value of 5 hours')
    
    def call_all_checks(self):
        self.check_fill_parametersdict()
        self.check_fill_parameterscompartments()
        self.check_fill_parametersperip()
        self.check_fill_parametersCLXtime()
    

    def generate_model(self):
        if self.params['injection_type'] == 'intravenous':
            return IntravenousModels(self.params)
        elif self.params['injection_type'] == 'subcutaneous':
            return SubcutaneousModels(self.params)
        else:
            raise Exception(
                'model type should be either intravenous or subcutaneous')
    
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
