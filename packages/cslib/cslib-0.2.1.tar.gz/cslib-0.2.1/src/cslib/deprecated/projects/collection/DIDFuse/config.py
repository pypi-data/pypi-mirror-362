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
        super().__init__('DIDFuse')
        self.update({
            'pre_trained': ['model1.pth','model2.pth'],
            'device': 'cuda' if is_available() else 'cpu',
            'channel': 64,
            'addition_mode': 'Sum',#'Sum', 'Average', 'l1_norm'
        })