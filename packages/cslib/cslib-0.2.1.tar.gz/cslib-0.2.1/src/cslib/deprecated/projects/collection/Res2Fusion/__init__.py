"""
    Res2Fusion: Infrared and visible image fusion based on dense Res2net and double nonlocal attention models
    Paper: https://ieeexplore.ieee.org/document/9670874
    Modified from: https://github.com/Zhishe-Wang/Res2Fusion
"""
from .model import load_model
from .inference import inference
from .config import TestOptions