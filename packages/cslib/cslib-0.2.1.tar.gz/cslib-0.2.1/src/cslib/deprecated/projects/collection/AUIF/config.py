from torch.cuda import is_available
from ....utils import Options

class TrainOptions(Options):
    """
                                                    Argument Explaination
        ======================================================================================================================
                Symbol          Type            Default                         Explaination
        ----------------------------------------------------------------------------------------------------------------------
            --pre_trained       Str         model.pth                       The path of pre-trained model
        ----------------------------------------------------------------------------------------------------------------------
    """
    def __init__(self):
        super().__init__('AUIF')
        self.update({
            'pre_trained': ['model1.pth','model2.pth','model3.pth'],
            'device': 'cuda' if is_available() else 'cpu',
            'channel': 64,
            'lr': 1*1e-2,
            'img_size': 128,
            'layer_numb': 10,
            'batch_size': 32,
            'log_interval': 12,
            'epoch': 80,
            'addition_mode': 'Sum',#'Sum', 'Average', 'l1_norm'
        })

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
        super().__init__('AUIF')
        self.update({
            'pre_trained': ['model1.pth','model2.pth','model3.pth'],
            'device': 'cuda' if is_available() else 'cpu',
            'channel': 64,
            'img_size': 128,
            'layer_numb': 10,
            'batch_size': 32,
            'addition_mode': 'Sum',#'Sum', 'Average', 'l1_norm'
        })
