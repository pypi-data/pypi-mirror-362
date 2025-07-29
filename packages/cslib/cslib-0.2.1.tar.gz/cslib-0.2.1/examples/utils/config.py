from cslib.utils import Options
from pathlib import Path

''' Config

    1. `Options` is basic option class, we can use build project uniqe options.
    2. `__init__`: we need to define model name.
    3. `Options.update`: update params.
    4. `Options.info`: print params.
    5. `Optinos.parse` = `Options.update` + `Options.info` + return namespace.
    6. `Options.save`: save options to a file.
'''


''' Example One: TrainOptions and TestOptions Demo

    1. Define Class
    2. Add, print and parse
    3. Save after train or test
'''

from torch.cuda import is_available

#   1.1 Define Options Class

class TrainOptions(Options):
    def __init__(self):
        super().__init__('LeNet')
        self.update({
            'device': 'cuda' if is_available() else 'cpu',
            'dataset_path': '../../data/mnist', 
            'epochs': 1, 
            'batch_size': 64, 
            'lr': 0.001, 
            'repeat': 2,
            'seed': 42,
            'train_mode': ['Holdout','K-fold'][0]
        })

class TestOptions(Options):
    def __init__(self):
        super().__init__('LeNet')
        self.update({
            'pre_trained': 'model.pth',
            'device': 'cuda' if is_available() else 'cpu',
            'batch_size': 64, 
        })

def train():
    #   1.2 In Train or Test function, get params
    opts = TestOptions().parse({})

    # train ...
    pass

    #   1.3 Save Params
    opts.save(Path(__file__).parent / 'config')

train()


''' Example Two: Recommand Workflow

    1. .sh
'''
# use bash script to save a command
# ```
# 
# ```