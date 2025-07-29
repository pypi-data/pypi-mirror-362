import torch
from torch.utils.data import DataLoader
from pathlib import Path
from tqdm import tqdm
import click

import cslib.projects.sr as sr
import cslib.datasets.sr as sr_data
from cslib.utils import save_array_to_img
import config

'''
生成超分辨率重建图片
1. 选择数据集(dataset: torch.utils.data.DataSet)
2. 选择数据集根目录(root_dir = root_dir_base + root_dir_path)
3. 选择超分辨率重建图片保存目录(des_dir), 一般和root_dir一样就行
4. 选择超分辨率重建方案(algorithm_name)
5. 选择超分辨率重建方案的配置名称(algorithm_config),在 config.py 中
6. 选择预训练模型路径(pre_trained), 最好在config里边配置好
7. 选择图片名称(img_id)
'''
@click.command()
@click.option('--dataset','-n',default='SRBase', help='Name of images dataset.')
@click.option('--root_dir_base','-rb',default="", help='Root directory containing the dataset.')
@click.option('--root_dir_path','-rp',default="Set5", help='Root directory containing the dataset.')
@click.option('--upscale_factor','-u',default="2", help='2 3 4.')
@click.option('--des_dir','-dr',default='', help='Destination directory to save the results.')
@click.option('--des_suffix','-ds',default='', help='Destination directory suffix to save the results.')
@click.option('--algorithm_name','-a',default='SRCNN', help='SR algorithm.')
@click.option('--algorithm_config','-ac',default='SRCNN2', help='Config name of SR algorithm.')
@click.option('--pre_trained','-p',default=(),multiple=True, help='path to pretrained model.')
@click.option('--img_id','-i',default=(),multiple=True, help='Image IDs to compute metrics for.')
def main(dataset, root_dir_base, root_dir_path, upscale_factor, des_dir, des_suffix, algorithm_name, algorithm_config, pre_trained, img_id):
    # load Algorithm Module and Options
    assert hasattr(sr_data, dataset)
    SRDataSet = getattr(sr_data, dataset)
    root_dir = Path(config.SRPath if root_dir_base=="" else root_dir_base,root_dir_path)
    for path in [root_dir,Path(root_dir,f'X{upscale_factor}','GT'),Path(root_dir,f'X{upscale_factor}','LR')]:
        assert path.exists()
    des_dir = root_dir if des_dir == '' else des_dir
    if des_dir.exists() == False: des_dir.mkdir()
    assert hasattr(sr, algorithm_name)
    algorithm = getattr(sr, algorithm_name)
    assert algorithm_config in config.opts
    opts = algorithm.TestOptions().parse(config.opts[algorithm_config])
    if pre_trained[0] != '':
        setattr(opts, 'pre_trained', pre_trained[0] if len(pre_trained) == 1 else pre_trained)
    img_id = None if img_id == () else [str(_id) for _id in img_id]
    
    # Load Dataset, Dataloader and model with pre-trained params
    dataset = SRDataSet(root_dir=Path(root_dir),img_id=img_id,upscale_factor=upscale_factor)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False) # batch size should be 1
    model = algorithm.load_model(opts)

    # run inference and save
    des_dir = Path(des_dir,f'X{upscale_factor}','HR',f'{algorithm_name}{des_suffix}')
    if des_dir.exists() == False: des_dir.mkdir()
    bar = tqdm(range(len(dataset)))
    with torch.no_grad():
        for _,batch in zip(bar,dataloader):
            img_res_path = Path(des_dir,Path(batch['gt'][0]).name)
            if img_res_path.exists(): continue
            img = algorithm.inference(model,batch['lr'][0],batch['gt'][0],opts)
            save_array_to_img(img,img_res_path)

if __name__ == '__main__':
    main()