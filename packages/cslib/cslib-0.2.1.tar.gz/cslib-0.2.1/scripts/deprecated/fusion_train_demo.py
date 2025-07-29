'''
训练融合网络
'''

import torch
from torch.utils.data import DataLoader
from pathlib import Path

from cslib.projects.fusion import DeepFuse as Method
from cslib.datasets.fusion import GeneralFusion
import config

opts = Method.TrainOptions().parse(config.opts['DeepFuse'])

dataset = GeneralFusion(
        root_dir=Path(config.opts['DeepFuse'].FusionPath,'Toy'),
        transform=Method.train_trans(opts),
        only_path=False
    )

dataloader = DataLoader(dataset, batch_size=opts.batch_size, shuffle=False)

model = Method.model(device=opts.device)

Method.train(model,dataloader,opts)