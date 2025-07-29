from pathlib import Path
import click

def build_file(path, content=[]):
    with open(path, 'w') as f:
        for line in content:
            if line is None:
                continue
            f.write(line+'\n')

@click.command()
@click.option('--name','-n', help='Name of algorithm.')
@click.option('--path','-p', help='Base path for the block.')
@click.option('--title','-t', help='Title of the paper.')
@click.option('--link','-l', help='Link to the paper.')
@click.option('--arxiv','-v', help='ArXiv of the paper.')
@click.option('--author','-a', help='Modified from ... or self written.')
def main(name,path,title,link,arxiv,author):
    print(f'***********************************************')
    print(f'*     Build new block for a new algorithm     *')
    print(f'***********************************************')
    
    base_path = Path(path)
    if base_path.exists() == False:
        print(f'❌ Path: {base_path} not exist! Build Failed!')
        print('Please input path to your CVPlayground!')
        return
    print(f'✅ Path: {base_path}')

    model_path = Path(base_path,'src','clib','model','collection',name)
    if model_path.exists():
        print(f'❌ Name: {name} has build! Change a name!')
        return
    print(f'✅ Name: {name}')
    model_path.mkdir()

    print(f'✅ Title: {title}')
    print(f'✅ Link: {link}')
    print(f'✅ ArXiv: {arxiv}')
    print(f'✅ Author: {author}')
    build_file(Path(model_path,"__init__.py"),
        [
            f'"""',
            f'    {title}',
            f'    Paper: {link}',
            f'    ArXiv: {arxiv}' if arxiv != "" else None,
            f'    Modified from: {author}' if author != "" else '    Author: Charles Shan',
            f'"""',
            f'from .model import {name} as Model, load_model',
            f'from .inference import inference',
            f'from .train import train'
        ])
    build_file(Path(model_path,"config.py"),
        [
            f'from torch.cuda import is_available',
            f'from ....utils import Options',
            f'',
            f'',
            f'class TrainOptions(Options):',
            f'    """',
            f'                                                    Argument Explaination',
            f'        ======================================================================================================================',
            f'                Symbol          Type            Default                         Explaination',
            f'        ----------------------------------------------------------------------------------------------------------------------',
            f'            --pre_trained       Str            model.pth                     The path of pre-trained model',
            f'        ----------------------------------------------------------------------------------------------------------------------',
            f'    """',
            f'    def __init__(self):',
            f"        super().__init__('{name}')",
             '        self.update({',
            f"            'pre_trained': 'model.pth',",
            f"            'device': 'cuda' if is_available() else 'cpu',",
            f"            'dataset_path': '../../data/mnist', ",
            f"            'epochs': 200, ",
            f"            'batch_size': 64, ",
            f"            'lr': 0.0002, ",
            f"            'train_mode': ['Holdout','K-fold'][0],"
             "        })",
            f'',
            f'',
            f'class TestOptions(Options):',
            f'    """',
            f'                                                    Argument Explaination',
            f'        ======================================================================================================================',
            f'                Symbol          Type            Default                         Explaination',
            f'        ----------------------------------------------------------------------------------------------------------------------',
            f'            --pre_trained       Str            model.pth                     The path of pre-trained model',
            f'        ----------------------------------------------------------------------------------------------------------------------',
            f'    """',
            f'    def __init__(self):',
            f"        super().__init__('{name}')",
             '        self.update({',
            f"            'pre_trained': 'model.pth',",
            f"            'device': 'cuda' if is_available() else 'cpu',",
             "        })",
        ])
    build_file(Path(model_path,"train.py"),
        [
            f'import torch.nn as nn',
            f'import torch.optim as optim',
            f'from torchvision import datasets, transforms',
            f'from torch.utils.data import DataLoader, random_split\n',
            f'from .utils import BaseTrainer',
            f'from .config import TrainOptions',
            f'from .model import {name} as Model\n',
            f'class Trainer(BaseTrainer):',
            f'    def __init__(self, opts, **kwargs):',
            f'        super().__init__(opts,TrainOptions,**kwargs)\n',
            f'    def default_model(self):',
            f'        return Model()\n',
            f'    def default_criterion(self):',
            f'        return nn.CrossEntropyLoss()\n',
            f'    def default_optimizer(self):',
            f'        return optim.SGD(self.model.parameters(), lr=self.opts.lr, momentum=self.opts.momentum)\n',
            f'    def default_transform(self):',
            f'        return transforms.Compose([',
            f'            transforms.Resize((224, 224)),',
            f'            transforms.ToTensor(),',
            f'            lambda x: x.repeat(3, 1, 1),  # 自定义转换，将单通道复制三次',
            f'            transforms.Normalize((0.1307,), (0.3081,))  # 标准化',
            f'        ])\n',
            f'    def default_train_loader(self):',
            f'        dataset = datasets.MNIST(root=self.opts.TorchVisionPath, train=True, download=True, transform=self.transform)',
            f'        train_size = int(0.8 * len(dataset))  # 80% for training',
            f'        val_size = len(dataset) - train_size   # 20% for validation',
            f'        train_dataset, _ = random_split(dataset, [train_size, val_size])',
            f'        return DataLoader(dataset=train_dataset, batch_size=self.opts.batch_size, shuffle=True)\n',
            f'    def default_val_loader(self):',
            f'        dataset = datasets.MNIST(root=self.opts.TorchVisionPath, train=True, download=True, transform=self.transform)',
            f'        train_size = int(0.8 * len(dataset))  # 80% for training',
            f'        val_size = len(dataset) - train_size   # 20% for validation',
            f'        _, val_size = random_split(dataset, [train_size, val_size])',
            f'        return DataLoader(dataset=val_size, batch_size=self.opts.batch_size, shuffle=False)',
            f'    def default_test_loader(self):',
            f'        test_dataset = datasets.MNIST(root=self.opts.TorchVisionPath, train=False, download=True, transform=self.transform)',
            f'        return DataLoader(dataset=test_dataset, batch_size=self.opts.batch_size, shuffle=False)\n\n',
             'def train(opts = {}, **kwargs):',
            f'    trainer = Trainer(opts, **kwargs)',
            f'    trainer.train()',
        ])
    build_file(Path(model_path,"inference.py"),
        [
            f'from .config import TestOptions\n',
            'def inference(opts={}):',
            '    opts = TestOptions().parse(opts)'
        ])
    build_file(Path(model_path,"model.py"),
        [
            f'import torch',
            f'import torch.nn as nn',
            f'',
            f'def load_model(opts):',
            f'    model = {name}().to(opts.device)',
            f'    params = torch.load(opts.pre_trained, map_location=opts.device)',
            f'    model.load_state_dict(params)',
            f'    return model',
            f'',
            f'class {name}(nn.Module):',
            f'    def __init__(self):',
            f'        super({name}, self).__init__()',
            f'    ',
            f'    def forward(self, x):',
            f'        return x'
        ])
    build_file(Path(model_path,"utils.py"),
        [
            f'from ....train import BaseTrainer'
        ])


if __name__ == '__main__':
    main()