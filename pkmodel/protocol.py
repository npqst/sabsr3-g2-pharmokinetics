#
# Protocol class
#

import ast
from .models import IntravenousModels, SubcutaneousModels
from .AbstractProtocol import AbstractProtocol


class Protocol(AbstractProtocol):
    """Protocol object which initialises the Model based on the input
    parameters and default parameters

    Args:
        AbstractProtocol (Class): AbstractProtocol is super-class of Protocol.
    """
    def __init__(self, file_dir=None):
        """Initialises Protocol object with default parameters

        The parameters are:
        name = name of model - output files will be saved under this name
        injection_type = intravenous bolus or subcutaneous (as described above)
        V_c = volume of the central compartment (mL)
        nr_compartments = the number of peripheral compartments
        periph_1 = (volume in the peripheral compartment (mL), transition rate
        between the central and peripheral compartment 1 (mL/h))
        CL = the clearance rate from the central compartment (mL/h)
        X = mass of drug administered at each dose
        run_mode = option to switch between ‘save’, which saves the plot,
        solution, and parameter output files, and ‘test’, which simply
        displays the plot of the solution
        dose_mode = the dose function, which can be chosed from ‘normal’,
        which is a single dose, and ‘pulse’, which initiates a series of pulse
        doses
        time = time period in which dosing is observed (hours - maximum 5)

        Args:
            file_dir (string, optional): Path for config file to update
            parameters if defined. Defaults to None.
        """
        self.params = {
            'name': 'model1',
            'V_c': 1.0,
            'periph_default': (1.0, 1.0),      # (V_p1, Q_p1)
            'CL': 1.0,
            'X': 1.0,
            'dose_mode': 'normal',
            'nr_compartments': 1,          # nr of peripheral compartments
            'injection_type': 'intravenous',    # 'subcutaneous'
            'run_mode': 'save',
            'time': 1
        }
        if file_dir:
            self.fill_parameters(file_dir)

    def read_config(self, file_dir):
        """Reads in config file and converts into python dictionary

        Args:
            file_dir (string): Relative path for the config file

        Returns:
            dict: Dictionary of the parameters
        """
        config_file = open(file_dir, "r")
        config_file_str = config_file.read()
        config_file.close()
        dictionaries_list = ast.literal_eval(str(config_file_str))
        return dictionaries_list

    def check_fill_parametersdict(self):
        """Checks the parameters are a dictionary

        Raises:
            TypeError: If parameters are not a dictionary
        """
        if not isinstance(self.params, dict):
            raise TypeError('data input should be a dictionary')

    def check_fill_parametersstr(self):
        """Checks the name and injection_type parameters are strings

        Raises:
            TypeError: If the name and injection_type parameters are not
            strings
        """
        for i in 'name', 'injection_type':
            if not isinstance(self.params[i], str):
                raise TypeError(f'{i} should be a string')

    def check_fill_parametersint(self):
        """Checks that nr_compartments and time paramters are integers

        Raises:
            TypeError: If nr_compartments or time are not an integer
            ValueError: If nr_compartments or time are less than 0
            ValueError: If time is larger than 5
        """
        for i in 'nr_compartments', 'time':
            if not isinstance(self.params[i], int):
                raise TypeError(f'{i} should be a integer')
            if self.params[i] < 0:
                raise ValueError(f'{i} should be at least 0')
            # Makes sure that time does not get too large as not relevant for
            # the model
            if i == 'time':
                if self.params['time'] > 5:
                    raise ValueError('Time should not '
                                     'exceed a value of 5 hours')

    def check_fill_parametersperip(self):
        """Checks that periph_* parameters are a tuple with two
        floats both larger than 0.

        Raises:
            TypeError: If periph_* parameter is not a tuple
            TypeError: If a value in the tuple is not a float
            ValueError: If a value in the tuple is less than 0
        """
        for n in range(1, self.params['nr_compartments'] + 1):
            if not isinstance(self.params[f'periph_{n}'], tuple):
                raise TypeError(f'periph_{n} should be a tuple')

            for i in range(0, 1):
                if not isinstance(self.params[f'periph_{n}'][i], float):
                    raise TypeError('values associated with the peripheral'
                                    f' compartment {n} should be float')
                if self.params[f'periph_{n}'][i] < 0:
                    raise ValueError(f'values associated \
                        with the peripheral compartment \
                            {n} should be larger than 0')

    def check_fill_parametersCLX(self):
        """Checks that parameters CL and X are floats and larger than 0

        Raises:
            TypeError: If CL or X is not a float
            ValueError: If CL or X is less than 0
        """
        for i in 'CL', 'X':
            if not isinstance(self.params[i], float):
                raise TypeError(f'{i} should be a float')
            if self.params[i] < 0:
                raise ValueError(f'{i} should be at least 0')

    def call_all_checks(self):
        """Calls all the check functions at once
        """
        self.check_fill_parametersdict()
        self.check_fill_parametersint()
        self.check_fill_parametersperip()
        self.check_fill_parametersCLX()
        self.check_fill_parametersstr()

    def fill_parameters(self, file_dir):
        """Fills the parameters using the config file and updates the
        default values based on these values

        Args:
            file_dir (string): Relative path for the config file
        """
        param_dicts = self.read_config(file_dir)
        # Uses the dictionary from read_config function
        # If config_file does not define parameter, use default parameter
        for k in self.params.keys():
            if k not in param_dicts:
                param_dicts[k] = self.params[k]
        # Add parameters for each peripheral compartment based on the
        # number of compartments defined. Uses defaults if not already
        # defined in config file.
        for i in range(1, param_dicts['nr_compartments'] + 1):
            key = f'periph_{i}'
            if key not in param_dicts:
                param_dicts[key] = self.params['periph_default']
        # If modelling subcutaneous injection, add k_a parameter if not
        # defined in config_file
        if (param_dicts['injection_type'] == 'subcutaneous'
                and 'k_a' not in param_dicts.keys()):
            param_dicts['k_a'] = 1.0
        # Update parameters with new dictionary and run checks on all values
        self.params = param_dicts
        self.call_all_checks()

    def generate_model(self):
        """Generates a model object based on the parameters in the Protocol object

        Raises:
            Exception: If an incorrect mode is given
            (not intravenous nor subcutaneous)

        Returns:
            Model Obnject: An initiated model using the defined parameters
        """
        if self.params['injection_type'] == 'intravenous':
            return IntravenousModels(self.params)
        elif self.params['injection_type'] == 'subcutaneous':
            return SubcutaneousModels(self.params)
        else:
            raise Exception(
                'model type should be either intravenous or subcutaneous')
