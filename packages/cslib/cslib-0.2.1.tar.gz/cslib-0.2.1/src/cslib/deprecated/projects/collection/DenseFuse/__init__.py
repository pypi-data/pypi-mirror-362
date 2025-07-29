"""
    H. Li, X. J. Wu, "DenseFuse: A Fusion Approach to Infrared and Visible Images," 
    IEEE Trans. Image Process., vol. 28, no. 5, pp. 2614-2623, May. 2019.
    Paper: https://arxiv.org/abs/1804.08361
    Modified from: https://github.com/hli1221/densefuse-pytorch
"""
from .model import DenseFuse as model, load_model
from .inference import inference
from .config import TestOptions