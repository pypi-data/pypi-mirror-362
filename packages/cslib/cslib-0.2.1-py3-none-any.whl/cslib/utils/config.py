"""
Config Utils Module

Contains Base Options class for clib module and user module.
"""

from typing import Dict, Any, Union
from argparse import Namespace
from pathlib import Path
from os import makedirs
import json

__all__ = [
    'Options', 'get_device'
]

class Options(Namespace):
    """
    Base Options class.

    This class provides a way to define and update command line arguments.

    Attributes:
        opts (argparse.Namespace): A namespace containing the parsed command line arguments.

    Methods:
        INFO(string): Print an information message.
        presentParameters(args_dict): Print the parameters setting line by line.
        update(parmas): Update the command line arguments.
    
    Example: 
        * config.py in a specific algorithm
        >>> from torch.cuda import is_available
        >>> from xxx import Options
        >>> class TestOptions(Options):
        >>> def __init__(self):
        >>>     super().__init__('DenseFuse')
        >>>     self.update({
        >>>         'pre_trained': 'model.pth',
        >>>         'device': 'cuda' if is_available() else 'cpu'
        >>>     })

        * update TestOptions in other files
        >>> opts = TestOptions().parse(other_opts_dict)

        * use TestOptions in other files
        >>> pre_trained_path = opts.pre_trained
    """

    def __init__(self, name: str = 'Undefined', params: Dict[str, Any] = {}):
        # self.opts = Namespace()
        self.name = name
        if len(params) > 0:
            self.update(params)

    def info(self, string: str):
        """
        Print an information message.

        Args:
            string (str): The message to be printed.
        """
        print("[ %s ] %s" % (self.name,string))

    def presentParameters(self):
        """
        Print the parameters setting line by line.

        Args:
            args_dict (Dict[str, Any]): A dictionary containing the command line arguments.
        """
        self.info("========== Parameters ==========")
        for key in vars(self).keys():
            self.info("{:>15} : {}".format(key, getattr(self, key)))
        self.info("================================")
    present = presentParameters

    def update(self, parmas: Dict[str, Any] = {}):
        """
        Update the command line arguments.

        Args:
            parmas (Dict[str, Any]): A dictionary containing the updated command line arguments.
        """
        for (key, value) in parmas.items():
            setattr(self, key, value)
    
    def parse(self, parmas: Dict[str, Any] = {}, present: bool = False):
        """
        Update the command line arguments. Can also present into command line.
        
        Args:
            parmas (Dict[str, Any]): A dictionary containing the updated command line arguments.
            present (bool) = True: Present into command line.
        """
        self.update(parmas)
        if present:
            self.presentParameters()
        return self
    
    def save(self, src: Union[str,Path] = ''):
        """
        Save Config when train is over.

        Args:
            params
        """
        src = self.model_base_path if src == '' else src
        p = Path(src)
        if p.exists() == False:
            makedirs(p)
        with open(Path(p,'config.json'), 'w') as f:
            f.write(self.__str__())
    
    def __str__(self):
        return json.dumps({
            key: getattr(self, key).__str__() for key in vars(self).keys()
        },indent=4)


import torch

def get_device(device: str = 'auto') -> torch.device:
    if device != 'auto':
        return torch.device(device)
    if torch.cuda.is_available():
        return torch.device('cuda')
    elif torch.backends.mps.is_available():
        return torch.device('mps')
    else:
        return torch.device('cpu')