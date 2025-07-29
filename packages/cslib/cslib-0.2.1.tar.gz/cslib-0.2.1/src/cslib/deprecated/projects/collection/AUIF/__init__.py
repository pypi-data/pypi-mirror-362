"""
    Codes for Efficient and Interpretable Infrared and Visible Image Fusion Via Algorithm Unrolling
    Paper: https://ieeexplore.ieee.org/document/9416456
    ArXiv: https://arxiv.org/abs/2003.09210v1
    Modified from: https://github.com/Zhaozixiang1228/IVIF-AUIF-Net
"""
from .model import load_model
from .inference import inference
from .config import TestOptions