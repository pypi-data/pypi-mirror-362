''' Metrics for Image Fusion
Introduction:
    * xx(): 默认输入都是 0-1 的张量
    * xx_metric(): 默认输入都是 0-1 的张量, 但会调整调用方法()的输入，会与 Matlab 源码一致
    * xx_approach_loss()：默认输入都是 0-1 的张量，用于趋近测试

Reference:
    VIFB: X. Zhang, P. Ye and G. Xiao, "VIFB: A Visible and Infrared Image Fusion Benchmark," 
        2020 IEEE/CVF Conference on Computer Vision and Pattern Recognition Workshops (CVPRW), 
        Seattle, WA, USA, 2020, pp. 468-478, doi: 10.1109/CVPRW50498.2020.00060.
    MEFB: Zhang X. Benchmarking and comparing multi-exposure image fusion algorithms[J]. 
        Information Fusion, 2021, 74: 111-131.
    OE: Zheng Liu, Erik Blasch, Zhiyun Xue, Jiying Zhao, Robert Laganiere, and Wei Wu. 
        2012. Objective Assessment of Multiresolution Image Fusion Algorithms for Context 
        Enhancement in Night Vision: A Comparative Study. IEEE Trans. Pattern Anal. Mach. 
        Intell. 34, 1 (January 2012), 94-109. https://doi.org/10.1109/TPAMI.2011.109
    RS(没有 matlab 代码): Yuhendra, et al. “Assessment of Pan-Sharpening Methods Applied to Image Fusion of 
        Remotely Sensed Multi-Band Data.” International Journal of Applied Earth Observation 
        and Geoinformation, Aug. 2012, pp. 165-75, https://doi.org/10.1016/j.jag.2012.01.013.
    MA: J. Ma, Y. Ma, C. Li, Infrared and visible image fusion methods 
        and applications: A survey, Inf. Fusion 45 (2019) 153-178.
    Many: P. Jagalingam, Arkal Vittal Hegde, A Review of Quality Metrics for Fused Image, 
        Aquatic Procedia, Volume 4, 2015, Pages 133-142, ISSN 2214-241X, https://doi.org/10.1016/j.aqpro.2015.02.019.
    Zhihu: 
        https://blog.csdn.net/qq_49729636/article/details/134502721
        https://zhuanlan.zhihu.com/p/136013000
    Rev:
        A New Edge and Pixel-Based Image Quality Assessment Metric for Colour and Depth Images
        https://github.com/SeyedMuhammadHosseinMousavi/A-New-Edge-and-Pixel-Based-Image-Quality-Assessment-Metric-for-Colour-and-Depth-Images
    Tang:
        https://github.com/Linfeng-Tang/Image-Fusion/tree/main/General%20Evaluation%20Metric
'''

# 信息论
from ..collection.en import *              # VIFB - 信息熵
from ..collection.te import *              # MEFB - tsallis熵
from ..collection.ce import *              # VIFB - 交叉熵
from ..collection.mi import *              # VIFB - 互信息
from ..collection.nmi import *             # MEFB - 标准化互信息
from ..collection.q_ncie import *          # MEFB - 非线性相关性
from ..collection.psnr import *            # VIFB - 峰值信噪比
from ..collection.cc import *              # Tang - 相关系数
from ..collection.scc import *             # pytorch - 空间相关系数
from ..collection.scd import *             # Tang - 差异相关和

# 结构相似性
from ..collection.ssim import *            # VIFB - 结构相似度测量
from ..collection.ms_ssim import *         # Tang - 多尺度结构相似度测量
from ..collection.q_s import *             # OE   - 利用 SSIM 的指标 Piella's Fusion Quality Index
from ..collection.q import *               # REV  - Image Quality Index (q, q0, qi, uqi, uiqi)
from ..collection.q_w import *             # OE   - 利用 SSIM 的指标 Weighted Fusion Quality Index(wfqi)
from ..collection.q_e import *             # OE   - 利用 SSIM 的指标 Piella's Edge-dependent Fusion Quality Index(efqi)
from ..collection.q_c import *             # MEFB - Cvejic
from ..collection.q_y import *             # MEFB - Yang
from ..collection.mb import *              # Many - Mean bias (遥感的指标)
from ..collection.mae import *             # RS   - Mean absolute error
from ..collection.mse import *             # VIFB - Mean squared error 均方误差
from ..collection.rmse import *            # VIFB - Root mean squared error 均方误差
from ..collection.nrmse import *           # Normalized Root Mean Square Error
from ..collection.ergas import *           # Zhihu- Error relative global dimensionless synthesis (遥感的指标)
from ..collection.d import *               # Many - Degree of Distortion (遥感的指标)
# from ..collection.q_h import *             # OB   - 每个图都要用小波，战略性放弃

# 图片信息
from ..collection.ag import *              # VIFB - 平均梯度
from ..collection.mg import *              # MA   - Mean Graident (similar to AG)
from ..collection.ei import *              # VIFB - 边缘强度
from ..collection.pfe import *             # Many - 百分比拟合误差 Percentage fit error
from ..collection.sd import *              # VIFB - 标准差 sd / std / theta
from ..collection.sf import *              # VIFB - 空间频率
from ..collection.q_sf import *            # OE   - 基于空间频率的指标 (metricZheng)
from ..collection.q_abf import *           # VIFB - 基于梯度的融合性能
from ..collection.eva import *             # Zhihu- 点锐度 (遥感的指标, 中文期刊)
from ..collection.asm import *             # Zhihu- 角二阶矩 - 不可微!!! (遥感的指标)
from ..collection.sam import *             # Zhihu- 光谱角测度 - 要修改 (遥感的指标)
from ..collection.con import *             # 对比度
from ..collection.fmi import *             # OE   - fmi_w(Discrete Meyer wavelet),fmi_g(Gradient),fmi_d(DCT),fmi_e(Edge),fmi_p(Raw pixels (no feature extraction))
from ..collection.n_abf import *           # Tang - 基于噪声评估的融合性能
from ..collection.pww import *             # Many - Pei-Wei Wang's algorithms (matlab的跑不起来了,python的可以)
# from ..collection.q_p import *             # MEFB 没翻译完

# 视觉感知
from ..collection.q_cb import *            # VIFB - 图像模糊与融合的质量评估 包含 cbb,cbm,cmd
from ..collection.q_cv import *            # VIFB - H. Chen and P. K. Varshney
from ..collection.vif import *             # MEFB - 视觉保真度 VIF / VIFF

# 融合指标工具
from .demo import *   # 自带的图像

"""
metric_type = {
    1: 'Information Theory',
    2: 'Structural Similarity',
    3: 'Image Feature',
    4: 'Visual Perception'
}

info_summary_dict = {
    'en':{
        'type': metric_type[1],
        'name': 'Entropy',
        'zh': '信息熵',
        'metric':en_metric
    },
    'te':{
        'type': metric_type[1],
        'name': 'Entropy',
        'zh': 'tsallis熵',
        'metric':te_metric
    },
    'ce':{
        'type': metric_type[1],
        'name': 'Cross Entropy',
        'zh': '交叉熵',
        'metric':ce_metric
    },
    'mi':{
        'type': metric_type[1],
        'name': 'Mutual Information',
        'zh': '互信息',
        'metric':mi_metric
    },
    'nmi':{
        'type': metric_type[1],
        'name': 'Normalized Mutual Information',
        'zh': '标准化互信息',
        'metric':nmi_metric
    },
    'q_ncie':{
        'type': metric_type[1],
        'name': 'Non-Complementary Information Entropy',
        'zh': '非线性相关性',
        'metric':q_ncie_metric
    },
    'psnr':{
        'type': metric_type[1],
        'name': 'Peak Signal-to-Noise Ratio',
        'zh': '峰值信噪比',
        'metric':psnr_metric
    },
    'cc':{
        'type': metric_type[1],
        'name': 'Correlation Coefficient ',
        'zh': '相关系数',
        'metric':cc_metric
    },
    'scc':{
        'type': metric_type[1],
        'name': 'Spatial Correlation Coefficient ',
        'zh': '空间相关系数',
        'metric':scc_metric
    },
    'scd':{
        'type': metric_type[1],
        'name': 'The Sum of Correlations of Differences',
        'zh': '差异相关和',
        'metric':scd_metric
    },
    'ssim':{
        'type': metric_type[2],
        'name': 'Structural Similarity',
        'zh': '结构相似度',
        'metric':ssim_metric
    },
    'ms_ssim':{
        'type': metric_type[2],
        'name': 'Multiscale Structural Similarity',
        'zh': '多尺度结构相似度测量',
        'metric':ms_ssim_metric
    },
    'q_s':{
        'type': metric_type[2],
        'name': 'Piella\'s Fusion Quality Index',
        'zh': '基于SSIM的Piella指标',
        'metric': q_s_metric
    },
    'q':{
        'type': metric_type[2],
        'name': 'Universal Image Quality Index',
        'zh': '通用质量指数',
        'metric': q_metric
    },
    'q_w':{
        'type': metric_type[2],
        'name': 'Piella\'s Weighted Fusion Quality Index',
        'zh': '基于权重的Piella指标',
        'metric': q_w_metric
    },
    'q_e':{
        'type': metric_type[2],
        'name': 'Piella\'s Edge-dependent Fusion Quality Index',
        'zh': '基于边缘的Piella指标',
        'metric': q_e_metric
    },
    'q_c':{
        'type': metric_type[2],
        'name': 'Cvejic\'s Fusion Quality Index',
        'zh': 'Cvejic指标',
        'metric': q_c_metric
    },
    'q_y':{
        'type': metric_type[2],
        'name': 'Yang\'s Fusion Quality Index',
        'zh': 'Yang指标',
        'metric': q_y_metric
    },
    'mb':{
        'type': metric_type[2],
        'name': 'Mean bias',
        'zh': '平均偏执',
        'metric':mb_metric
    },
    'mae':{
        'type': metric_type[2],
        'name': 'Mean Absolute Error',
        'zh': '平均绝对误差',
        'metric':mae_metric
    },
    'mse':{
        'type': metric_type[2],
        'name': 'Mean Square Error',
        'zh': '平方误差',
        'metric':mse_metric
    },
    'rmse':{
        'type': metric_type[2],
        'name': 'Root Mean Square Error',
        'zh': '均方根误差',
        'metric':rmse_metric
    },
    'nrmse':{
        'type': metric_type[2],
        'name': 'Normalized Root Mean Square Error',
        'zh': '正规化均方根误差',
        'metric':nrmse_metric
    },
    'ergas':{
        'type': metric_type[2],
        'name': 'Error relative global dimensionless synthesis',
        'zh': '全局无量纲综合误差',
        'metric':ergas_metric
    },
    'd':{
        'type': metric_type[2],
        'name': 'Degree of Distortion',
        'zh': '失真度',
        'metric':d_metric
    },
    # 'q_h':{
    #     'type': metric_type[2],
    #     'name': 'Hossny\'s Fusion Quality Index',
    #     'zh': 'Hossny指标',
    #     'metric':q_h_metric
    # },
    'ag':{
        'type': metric_type[3],
        'name': 'Average Gradient',
        'zh': '平均梯度',
        'metric':ag_metric
    },
    'mg':{
        'type': metric_type[3],
        'name': 'Mean Gradient',
        'zh': '梯度均值',
        'metric':mg_metric
    },
    'ei':{
        'type': metric_type[3],
        'name': 'Edge Intensity',
        'zh': '边缘强度',
        'metric':ei_metric
    },
    'pfe':{
        'type': metric_type[3],
        'name': 'Percentage Fit Error',
        'zh': '百分比拟合误差 ',
        'metric':pfe_metric
    },
    'sd':{
        'type': metric_type[3],
        'name': 'Standard Deviation',
        'zh': '标准差',
        'metric':sd_metric
    },
    'sf':{
        'type': metric_type[3],
        'name': 'Spatial Frequency',
        'zh': '空间频率',
        'metric':sf_metric
    },
    'q_sf':{
        'type': metric_type[3],
        'name': 'Metircs Base on SF',
        'zh': '基于空间频率的指标',
        'metric':q_sf_metric
    },
    'q_abf':{
        'type': metric_type[3],
        'name': 'Qabf',
        'zh': '基于梯度的融合性能',
        'metric':q_abf_metric
    },
    'eva':{
        'type': metric_type[3],
        'name': 'EVA',
        'zh': '点锐度',
        'metric':eva_metric
    },
    'asm':{
        'type': metric_type[3],
        'name': 'Angular Second Moment',
        'zh': '角二阶矩',
        'metric':asm_metric
    },
    'sam':{
        'type': metric_type[3],
        'name': 'Spectral Angle Mapper',
        'zh': '光谱角制图',
        'metric':sam_metric
    },
    'con':{
        'type': metric_type[3],
        'name': 'Contrast',
        'zh': '对比度',
        'metric':con_metric
    },
    'fmi':{
        'type': metric_type[3],
        'name': 'Feature Mutual Information',
        'zh': '特征互信息',
        'metric':fmi_metric
    },
    'n_abf':{
        'type': metric_type[3],
        'name': 'No-reference Assessment Based on Blur and Noise Factors',
        'zh': '基于模糊和噪声因素的无参考质量评估',
        'metric':n_abf_metric
    },
    'pww':{
        'type': metric_type[3],
        'name': 'Pei-Wei Wang\'s algorithms',
        'zh': 'Pei-Wei Wang指标',
        'metric':pww_metric
    },
    # 'q_p':{
    #     'type': metric_type[2],
    #     'name': 'Feature-based Evaluation Metric',
    #     'zh': '特征基础的评价指标',
    #     'metric':q_p_metric
    # },
    'q_cb':{
        'type': metric_type[4],
        'name': 'Metric of Chen Blum',
        'zh': 'Qcb',
        'metric':q_cb_metric
    },
    'q_cv':{
        'type': metric_type[4],
        'name': 'Metric of Chen',
        'zh': 'Qcv',
        'metric':q_cv_metric
    },
    'vif':{
        'type': metric_type[4],
        'name': 'Visual Information Fidelity',
        'zh': '视觉保真度',
        'metric':vif_metric
    }
}

''' Demo: Use Example Images. (Run in experinment folder)
import cslib.metrics.fusion as metrics
need = ['ag'] # Write metrics names that you need
for (k,v) in metrics.info_summary_dict.items():
    if k not in need: continue
    print(f"{k}(CDDFuse)  : {v['metric'](metrics.ir,metrics.vis,metrics.cddfuse)}")
    print(f"{k}(DenseFuse): {v['metric'](metrics.ir,metrics.vis,metrics.densefuse)}")
    print(f"{k}(ADF)      : {v['metric'](metrics.ir,metrics.vis,metrics.adf)}")
'''
"""
