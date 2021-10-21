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
            'Q_p1': 1.0,
            'V_c': 1.0,

            'V_p1': 1.0,
            'CL': 1.0,
            'X': 1.0,
            'dose': dose
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
        self.params = param_dicts

    def generate_model(self):
        return IntravenousModels(self.params)
