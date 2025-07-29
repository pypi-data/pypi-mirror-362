from pathlib import Path
from cslib.deprecated import ConfigDict
        
opts = ConfigDict(data_root_path_list=[
            '/root/autodl-tmp',
            '/Volumes/Charles/data',
            '/Users/kimshan/public/data'
        ])

opts['DeepFuse'] = {
    # pytorch复现版的, https://github.com/SunnerLi/DeepFuse.pytorch
    'pre_trained': Path(opts.ModelBasePath,'DeepFuse','DeepFuse_model.pth'),
}
opts['DenseFuse_gray'] = {
    # https://github.com/hli1221/densefuse-pytorch
    'pre_trained': Path(opts.ModelBasePath,'DenseFuse','densefuse_gray.model'), 
    'color': 'gray',
}
opts['DenseFuse_rgb'] = {
    # # https://github.com/hli1221/densefuse-pytorch
    # 'pre_trained': Path(opts.ModelBasePath,'DenseFuse','densefuse_rgb.model'),
    'pre_trained': Path(opts.ModelBasePath,'DenseFuse','densefuse_gray.model'),
    'color': 'color', # 看了论文,rgb 的 densefuse 是三个通道分别进行单通道融合然后拼起来!
}
opts['CDDFuse'] = {
    # https://github.com/Zhaozixiang1228/MMIF-CDDFuse
    'pre_trained': Path(opts.ModelBasePath,'CDDFuse','CDDFuse_IVF.pth'), 
}
opts['AUIF'] = {
    'pre_trained': [ # https://github.com/Zhaozixiang1228/IVIF-AUIF-Net
        Path(opts.ModelBasePath,'AUIF','TCSVT_Encoder_Base.model'),
        Path(opts.ModelBasePath,'AUIF','TCSVT_Encoder_Detail.model'),
        Path(opts.ModelBasePath,'AUIF','TCSVT_Decoder.model'),
    ],
}
opts['DIDFuse'] = {
    'pre_trained': [ # https://github.com/Zhaozixiang1228/IVIF-DIDFuse
        Path(opts.ModelBasePath,'DIDFuse','Encoder_weight_IJCAI.pkl'),
        Path(opts.ModelBasePath,'DIDFuse','Decoder_weight_IJCAI.pkl'),
    ],
}
opts['SwinFuse'] = {
    # https://github.com/Zhishe-Wang/SwinFuse
    'pre_trained': Path(opts.ModelBasePath,'SwinFuse','Final_epoch_50_Mon_Feb_14_17_37_05_2022_1e3.model'), 
}
opts['MFEIF'] = {
    # https://github.com/JinyuanLiu-CV/MFEIF
    'pre_trained': Path(opts.ModelBasePath,'MFEIF','default.pth'), 
}
opts['Res2Fusion'] = {
    # https://github.com/Zhishe-Wang/Res2Fusion
    # 'pre_trained': Path(ModelBasePath,'Res2Fusion','Final_epoch_4_1e0.model'), 
    # 'pre_trained': Path(ModelBasePath,'Res2Fusion','Final_epoch_4_1e1.model'),
    # 'pre_trained': Path(ModelBasePath,'Res2Fusion','Final_epoch_4_1e2.model'),
    'pre_trained': Path(opts.ModelBasePath,'Res2Fusion','Final_epoch_4_1e3.model'),
}
opts['UNFusion_l1_mean'] = {
    'pre_trained': Path(opts.ModelBasePath,'UNFusion','UNFusion.model'),
    'fusion_type': 'l1_mean',#['l1_mean', 'l2_mean', 'linf']
}
opts['UNFusion_l2_mean'] = {
    'pre_trained': Path(opts.ModelBasePath,'UNFusion','UNFusion.model'),
    'fusion_type': 'l2_mean',#['l1_mean', 'l2_mean', 'linf']
}
opts['UNFusion_linf'] = {
    'pre_trained': Path(opts.ModelBasePath,'UNFusion','UNFusion.model'),
    'fusion_type': 'linf',#['l1_mean', 'l2_mean', 'linf']
}
opts['CoCoNet'] = {
    # https://github.com/runjia0124/CoCoNet
    'pre_trained': Path(opts.ModelBasePath,'CoCoNet','latest.pth'), 
}
opts['DDFM'] = {
    # https://github.com/openai/guided-diffusion
    'pre_trained': Path(opts.ModelBasePath,'DDFM','256x256_diffusion_uncond.pt'), 
}
# opts['SRCNN2'] = {
#     # https://github.com/Lornatang/SRCNN-PyTorch
#     'pre_trained': Path(opts.ModelBasePath,'SRCNN','srcnn_x2-T91-7d6e0623.pth.tar'),
# }
# opts['SRCNN3'] = {
#     # https://github.com/Lornatang/SRCNN-PyTorch
#     'pre_trained': Path(opts.ModelBasePath,'SRCNN','srcnn_x3-T91-919a959c.pth.tar'),
# }
# opts['SRCNN4'] = {
#     # https://github.com/Lornatang/SRCNN-PyTorch
#     'pre_trained': Path(opts.ModelBasePath,'SRCNN','srcnn_x4-T91-7c460643.pth.tar'),
# }
# opts['GAN'] = {
#     'dataset_path': Path(opts.TorchVisionPath),
#     'images_path': Path(opts.ModelBasePath,'GAN','images'),
#     'models_path': Path(opts.ModelBasePath,'GAN','epoch200'),
#     'pre_trained': Path(opts.ModelBasePath,'GAN','epoch200','generator.pth')
# }
