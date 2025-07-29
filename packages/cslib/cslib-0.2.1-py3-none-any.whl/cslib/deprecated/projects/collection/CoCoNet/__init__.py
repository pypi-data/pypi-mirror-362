"""
    Coconet: Coupled contrastive learning network with multi-level feature ensemble for multi-modality image fusion
    Paper: https://link.springer.com/article/10.1007/s11263-023-01952-1
    ArXiv: https://arxiv.org/pdf/2211.10960
    Modified from: https://github.com/runjia0124/CoCoNet
"""
from .model import load_model
from .inference import inference
from .config import TestOptions