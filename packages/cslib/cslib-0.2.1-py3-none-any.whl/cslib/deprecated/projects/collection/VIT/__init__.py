"""
    An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale
    Paper: https://api.semanticscholar.org/CorpusID:225039882
    ArXiv: https://arxiv.org/abs/2010.11929
    Author: Charles Shan
"""
from .model import VIT as Model, load_model
from .inference import inference
from .train import train
