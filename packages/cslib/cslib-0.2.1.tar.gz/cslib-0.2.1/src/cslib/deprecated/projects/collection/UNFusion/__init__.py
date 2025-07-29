"""
    UNFusion: A unified multi-scale densely connected network for infrared and visible image fusion
    Paper: https://ieeexplore.ieee.org/document/9528393/
    ArXiv: https://arxiv.org/abs/2204.11436
    Modified from: https://github.com/Zhishe-Wang/SwinFuse
"""
from .model import load_model
from .inference import inference
from .config import TestOptions