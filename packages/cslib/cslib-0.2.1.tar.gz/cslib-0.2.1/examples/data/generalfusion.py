import click
from cslib.datasets.fusion import GeneralFusion
from cslib.utils import Options
from torch.utils.data import DataLoader

default_ir_dir = "/Volumes/Charles/data/vision/torchvision/llvip/infrared/test"
default_vis_dir = "/Volumes/Charles/data/vision/torchvision/llvip/visible/test"
default_fused_dir_a = "/Volumes/Charles/data/vision/torchvision/llvip/fused"
# Condition A: There are child folders in fused_dir
# each child folder represent a kind of algorithm
default_fused_dir_b = "/Volumes/Charles/data/vision/torchvision/llvip/fused/cpfusion"
# Condition B: There is no child folder in fused_dir
# The name of dir represent the name of algorithm

@click.command()
@click.option('--ir_dir', default=default_ir_dir, type=click.Path(exists=True), help='Infraed directory of the dataset.')
@click.option('--vis_dir', default=default_vis_dir, type=click.Path(exists=True), help='Visiable directory of the dataset.')
@click.option('--fused_dir_a', default=default_fused_dir_a, type=click.Path(exists=True), help='Visiable directory of the dataset.')
@click.option('--fused_dir_b', default=default_fused_dir_b, type=click.Path(exists=True), help='Visiable directory of the dataset.')
@click.option('--suffix', default='jpg')
def main(**kwargs):
    opts = Options("GeneralFusion Demo", kwargs).parse({},present=True)
    
    print("Condition A: There are child folders in fused_dir")
    dataset_a = GeneralFusion(
        ir_dir=opts.ir_dir, 
        vis_dir=opts.vis_dir, 
        fused_dir=opts.fused_dir_a, 
        algorithms=['cpfusion', 'datfuse'],
        img_id=['190002','190001'],
        suffix=opts.suffix,
    )
    print(f"len = {len(dataset_a)}")
    dataloader = DataLoader(dataset_a, batch_size=1, shuffle=False)
    for batch in dataloader:
        print(batch['ir'].shape, batch['vis'].shape, batch['fused'].shape, batch['algorithm'])
        break

    print("Condition B: There is no child folder in fused_dir")
    dataset_b = GeneralFusion(
        ir_dir=opts.ir_dir, 
        vis_dir=opts.vis_dir, 
        fused_dir=opts.fused_dir_b, 
        algorithms=None, # <- This should be None
        img_id=['190003','190002'], # <- set to [], you will get all images in the folder
        suffix=opts.suffix,
    )
    print(f"len = {len(dataset_b)}")
    dataloader = DataLoader(dataset_b, batch_size=1, shuffle=False)
    for batch in dataloader:
        print(batch['ir'].shape, batch['vis'].shape, batch['fused'].shape, batch['algorithm'])
        break

if __name__ == '__main__':
    main()
    # [ GeneralFusion Demo ] ========== Parameters ==========
    # [ GeneralFusion Demo ]            name : GeneralFusion Demo
    # [ GeneralFusion Demo ]          ir_dir : /Volumes/Charles/data/vision/torchvision/llvip/infrared/test
    # [ GeneralFusion Demo ]         vis_dir : /Volumes/Charles/data/vision/torchvision/llvip/visible/test
    # [ GeneralFusion Demo ]     fused_dir_a : /Volumes/Charles/data/vision/torchvision/llvip/fused
    # [ GeneralFusion Demo ]     fused_dir_b : /Volumes/Charles/data/vision/torchvision/llvip/fused/cpfusion
    # [ GeneralFusion Demo ]          suffix : jpg
    # [ GeneralFusion Demo ] ================================
    # Condition A: There are child folders in fused_dir
    # len = 4
    # torch.Size([1, 3, 1024, 1280]) torch.Size([1, 3, 1024, 1280]) torch.Size([1, 3, 1024, 1280]) ['cpfusion']
    # Condition B: There is no child folder in fused_dir
    # len = 2
    # torch.Size([1, 3, 1024, 1280]) torch.Size([1, 3, 1024, 1280]) torch.Size([1, 3, 1024, 1280]) ['cpfusion']
