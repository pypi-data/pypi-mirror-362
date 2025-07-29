"""
    DeepFuse: A Deep Unsupervised Approach for Exposure Fusion with Extreme Exposure Image Pairs
    Paper: https://arxiv.org/abs/1712.07384
    Modified from: https://github.com/SunnerLi/DeepFuse.pytorch
"""
from .model import DeepFuse as model, load_model
from .inference import inference
from .train import train,train_trans
from .config import TestOptions,TrainOptions