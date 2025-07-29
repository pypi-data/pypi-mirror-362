"""
    DIDFuse: Deep Image Decomposition for Infrared and Visible Image Fusion
    ArXiv: https://arxiv.org/pdf/2003.09210v1
    Modified from: https://github.com/Zhaozixiang1228/IVIF-DIDFuse
"""
from .model import load_model
from .inference import inference
from .config import TestOptions