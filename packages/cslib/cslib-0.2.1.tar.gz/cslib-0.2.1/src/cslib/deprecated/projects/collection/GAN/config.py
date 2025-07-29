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
        super().__init__('GAN')
        self.update({
            'pre_trained': 'model.pth',
            'device': 'cuda' if is_available() else 'cpu',
            'dataset_path': '../../data/mnist', 
            'n_epochs': 200,# 200 # number of epochs of training
            'batch_size': 64, # size of the batches
            'lr': 0.0002, # adam: learning rate
            'b1': 0.5, # adam: decay of first order momentum of gradient
            'b2': 0.999, # adam: decay of first order momentum of gradient
            'n_cpu': 8, # number of cpu threads to use during batch generation
            'latent_dim': 100, # dimensionality of the latent space
            'img_size': 28, # size of each image dimension
            'channels': 1, # number of image channels
            'sample_interval': 400, # interval between image samples
        })
        self.update({
            'img_shape': (self.opts.channels, self.opts.img_size, self.opts.img_size)
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
        super().__init__('GAN')
        self.update({
            'pre_trained': 'model.pth',
            'device': 'cuda' if is_available() else 'cpu',
            'batch_size': 64, # size of the batches
            'latent_dim': 100, # dimensionality of the latent space
            'img_size': 28, # size of each image dimension
            'channels': 1, # number of image channels
        })
        self.update({
            'img_shape': (self.opts.channels, self.opts.img_size, self.opts.img_size)
        })

