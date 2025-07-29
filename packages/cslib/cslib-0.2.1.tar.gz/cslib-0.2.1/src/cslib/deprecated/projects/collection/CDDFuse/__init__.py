"""
    CDDFuse: Correlation-Driven Dual-Branch Feature Decomposition for Multi-Modality Image Fusion
    Paper: https://openaccess.thecvf.com/content/CVPR2023/html/Zhao_CDDFuse_Correlation-Driven_Dual-Branch_Feature_Decomposition_for_Multi-Modality_Image_Fusion_CVPR_2023_paper.html
    Modified from: https://github.com/Zhaozixiang1228/MMIF-CDDFuse
"""
from .model import load_model
from .inference import inference
from .config import TestOptions