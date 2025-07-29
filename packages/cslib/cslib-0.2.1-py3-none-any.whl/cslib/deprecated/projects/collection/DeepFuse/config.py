import argparse
from torch.cuda import is_available
from pathlib import Path
from ....utils import Options

class TrainOptions(Options):
    """
                                                    Argument Explaination
        ======================================================================================================================
                Symbol          Type            Default                         Explaination
        ----------------------------------------------------------------------------------------------------------------------
            --folder            Str         /images/Bracketed_images        The folder path of bracketed image
            --crop_size         Int         256                             -
            --batch_size        Int         8                               -
            --resume            Str         1.pth                           The path of pre-trained model
            --det               Str         train_result                    The path of folder you want to store the result in
            --epoch             Int         15000                           -
            --record_epoch      Int         100                             The period you want to store the result
            --H                 Int         400                             The height of the result image
            --W                 Int         600                             The width of the result image
        ----------------------------------------------------------------------------------------------------------------------
    """
    def __init__(self):
        super().__init__('DeepFuse')
        parser = argparse.ArgumentParser()
        parser.add_argument('--folder'          , type = str, default = "/home/sunner/Music/HDREyeDataset/images/Bracketed_images")
        parser.add_argument('--crop_size'       , type = int, default = 256)
        parser.add_argument('--batch_size'      , type = int, default = 8)
        parser.add_argument('--resume'          , type = str, default = "1.pth")
        parser.add_argument('--det'             , type = str, default = "train_result")
        parser.add_argument('--epoch'           , type = int, default = 4)#15000
        parser.add_argument('--record_epoch'    , type = int, default = 2)#100
        parser.add_argument('--H'       , type = int, default = 400)
        parser.add_argument('--W'       , type = int, default = 600)
        self.opts = parser.parse_args()
        self.opts.device = 'cuda' if is_available() else 'cpu'

    def parse(self,parmas={}):
        # Update and Print the parameter first
        self.update(parmas)
        self.presentParameters(vars(self.opts))

        # Create the folder
        det_name = Path(self.opts.det)
        image_folder_name = Path(det_name, "image")
        model_folder_name = Path(det_name, "model")
        if not det_name.exists():
            det_name.mkdir()
        if not image_folder_name.exists():
            image_folder_name.mkdir()
        if not model_folder_name.exists():
            model_folder_name.mkdir()

        return self.opts
    

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
        super().__init__('DeepFuse')
        self.update({
            'pre_trained': 'model.pth',
            'H': 400,
            'W': 600,
            'resize': False,
            'device': 'cuda' if is_available() else 'cpu'
        })