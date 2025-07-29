"""
    Image Super-Resolution Using Deep Convolutional Networks, TPAMI 2016
    Paper: https://arxiv.org/abs/1501.00092v3
    Modified from: https://github.com/Lornatang/SRCNN-PyTorch
"""
from .model import load_model
from .inference import inference 
from .config import TestOptions