"""
    MFEIF: Learning a Deep Multi-scale Feature Ensemble and an Edge-attention Guidance for Image Fusion
    Paper: https://ieeexplore.ieee.org/document/9349250
    Modified from: https://github.com/JinyuanLiu-CV/MFEIF
"""
from .model import load_model
from .inference import inference
from .config import TestOptions