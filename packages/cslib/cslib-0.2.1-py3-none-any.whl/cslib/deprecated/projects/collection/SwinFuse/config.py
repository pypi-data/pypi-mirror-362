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
        super().__init__('SwinFuse')
        self.update({
            'pre_trained': 'model.pth',
            'device': 'cuda' if is_available() else 'cpu',
            'fusion_type': 'l1_mean',
        })