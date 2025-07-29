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
            'pre_trained': 'model.pth',
            'device': 'cuda' if is_available() else 'cpu',
            'epoch': 5, # epoch number
            'num_task': 3, # k shot for support set
            'lr': 1e-4, # task-level inner update learning rate
            'bs': 10, # batch size
            'logdir': './logs/',
            'c1': 0.5, # weight gradweight grad
            'c2': 0.5, # weight entropy
            'contrast': 1.0, # contrastive loss weight
            'w_loss': 1.0, # weight of self-adaptive loss
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
            'pre_trained': 'model.pth',
            'VGG_pre_trained': 'place_holder', # use pre_trained model
            'device': 'cuda' if is_available() else 'cpu',
        })
