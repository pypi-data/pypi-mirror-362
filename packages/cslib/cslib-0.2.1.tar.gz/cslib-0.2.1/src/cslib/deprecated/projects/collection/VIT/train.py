import torch.nn as nn
import torch.optim as optim
from torchvision import datasets, transforms
from torch.utils.data import DataLoader, random_split

from .utils import BaseTrainer
from .config import TrainOptions
from .model import VIT as Model

class Trainer(BaseTrainer):
    def __init__(self, opts, **kwargs):
        super().__init__(opts,TrainOptions,**kwargs)

    def default_model(self):
        return Model()

    def default_criterion(self):
        return nn.CrossEntropyLoss()

    def default_optimizer(self):
        return optim.SGD(self.model.parameters(), lr=self.opts.lr, momentum=self.opts.momentum)

    def default_transform(self):
        return transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            lambda x: x.repeat(3, 1, 1),  # 自定义转换，将单通道复制三次
            transforms.Normalize((0.1307,), (0.3081,))  # 标准化
        ])

    def default_train_loader(self):
        dataset = datasets.MNIST(root=self.opts.TorchVisionPath, train=True, download=True, transform=self.transform)
        train_size = int(0.8 * len(dataset))  # 80% for training
        val_size = len(dataset) - train_size   # 20% for validation
        train_dataset, _ = random_split(dataset, [train_size, val_size])
        return DataLoader(dataset=train_dataset, batch_size=self.opts.batch_size, shuffle=True)

    def default_val_loader(self):
        dataset = datasets.MNIST(root=self.opts.TorchVisionPath, train=True, download=True, transform=self.transform)
        train_size = int(0.8 * len(dataset))  # 80% for training
        val_size = len(dataset) - train_size   # 20% for validation
        _, val_size = random_split(dataset, [train_size, val_size])
        return DataLoader(dataset=val_size, batch_size=self.opts.batch_size, shuffle=False)
    def default_test_loader(self):
        test_dataset = datasets.MNIST(root=self.opts.TorchVisionPath, train=False, download=True, transform=self.transform)
        return DataLoader(dataset=test_dataset, batch_size=self.opts.batch_size, shuffle=False)


def train(opts = {}, **kwargs):
    trainer = Trainer(opts, **kwargs)
    trainer.train()
