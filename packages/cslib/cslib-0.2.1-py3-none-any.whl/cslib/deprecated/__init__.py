from typing import Dict, List, Any
from pathlib import Path
from collections import UserDict
import torch

class ConfigDict(UserDict):
    """
    ConfigDict is declared when calling clib. It is used to specify the highest 
    priority parameters. It requires a list of data root directories, and the 
    dictionary will automatically find the first existing root directory, which 
    is used to adapt to multi-platform scenarios.
    
    The directory structure of your data root directory needs to be as follows:
    - data_root_path
      | - torchvision: Contains the official datasets of torchvision
      | - model: Contains the training results and pre-trained models of each model
      | - Fusion: Contains data for image fusion
      | - SR: Contains data for super-resolution reconstruction
      | - ...: Contains other data, which users can define and extend as needed
    
    Example: # In config.py
    >>> from pathlib import Path
    >>> from clib.utils import ConfigDict
    >>> opts = ConfigDict([
                    '/root/autodl-fs/DateSets',
                    '/Volumes/Charles/DateSets',
                    '/Users/kimshan/resources/DataSets'
                ])
    >>> opts['LeNet'] = {
            'ResBasePath': Path(opts.ModelBasePath,'LeNet','MNIST','temp'),
            'pre_trained': Path(opts.ModelBasePath,'LeNet','MNIST','9839_m1_d003','model.pth'),
        }
    """
    def __init__(self, data_root_path_list: List[str]):
        super().__init__({})
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.data_root_path_list = data_root_path_list
        self.DataRootPath = None
        for path in self.data_root_path_list:
            if Path(path).exists() and Path(path).is_dir():
                self.DataRootPath = path
                break
        assert(self.DataRootPath is not None)
        self.TorchVisionPath = Path(self.DataRootPath, "torchvision").__str__()
        self.FusionPath = Path(self.DataRootPath, "Fusion").__str__()
        self.SRPath = Path(self.DataRootPath, "SR").__str__()
        self.ModelBasePath = Path(self.DataRootPath, "Model").__str__()

    def __setitem__(self, key: str, value: Dict[str, Any]):
        check_list = [
            'device','DataRootPath','TorchVisionPath',
            'FusionPath','SRPath','ModelBasePath',
        ]
        for item in check_list:
            if item not in value:
                value[item] = getattr(self,item)
        
        for item in list(value.keys()):
            if item.startswith('*'):
                temps = value[item] if isinstance(value[item],list) else [value[item]]
                for i,temp in enumerate(temps):
                    part_list = []
                    for part in Path(temp).parts:
                        if not part.startswith('@'):
                            part_list.append(part)
                        else:
                            if hasattr(self,part[1:]):
                                part_list.append(getattr(self,part[1:]))
                            else:
                                part_list.append(value[part[1:]])
                    temps[i] = Path(*part_list).__str__()
                value[item[1:]] = temps[0] if len(temps)==1 else temps
                
        super().__setitem__(key, {k: value[k] for k in value if not k.startswith('*')})
