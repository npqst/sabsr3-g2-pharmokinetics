#
# Protocol class
#

class Protocol(Model):
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
        }
    
    def read_config(self, file_dir):
        #get current directory and add to file_dir
        config_file = open("file_dir", "r")
        
    
    def add_parameters

    def generate_model(self, )
