from torch.cuda import is_available
from ....utils import Options

class TestOptions(Options):
    """
                                                    Argument Explaination
        ======================================================================================================================
                Symbol          Type            Default                         Explaination
        ----------------------------------------------------------------------------------------------------------------------
            --pre_trained       Str         model.pth                       The path of pre-trained model
        ----------------------------------------------------------------------------------------------------------------------
    """
    def __init__(self):
        super().__init__('Res2Fusion')
        self.update({
            'pre_trained': 'model.pth',
            'device': 'cuda' if is_available() else 'cpu',
            'strategy_type': 'add', #'add', 'atten',
            'channel': 1, # 1, 3
            'mode': 'L'
        })