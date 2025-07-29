"""
    SwinFuse: A Residual Swin Transformer Fusion Network for Infrared and Visible Images
    Paper: https://ieeexplore.ieee.org/document/9832006/
    ArXiv: https://arxiv.org/abs/2204.11436
    Modified from: https://github.com/Zhishe-Wang/SwinFuse
"""
from .model import load_model
from .inference import inference
from .config import TestOptions