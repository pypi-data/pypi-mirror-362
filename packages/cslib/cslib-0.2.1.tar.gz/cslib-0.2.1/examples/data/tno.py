import click
from pathlib import Path
from cslib.datasets.fusion import TNO

def demo_auto_download(root_dir):
    TNO(root = root_dir,download = True)

def demo_wave_length(root_dir):
    dataset_nir_lwir = TNO(root_dir, img_type = 'both')
    dataset_nir = TNO(root_dir, img_type = 'nir')
    dataset_lwir = TNO(root_dir, img_type = 'lwir') # Default
    print(f"Length of the 'nir_lwir' dataset: {len(dataset_nir_lwir)}") # 32
    print(f"Length of the 'nir' dataset: {len(dataset_nir)}") # 37
    print(f"Length of the 'lwir' dataset: {len(dataset_lwir)}") # 235

def demo_set(root_dir):
    dataset_both = TNO(root_dir, img_type = 'lwir',mode = 'both') # Default
    dataset_seq = TNO(root_dir, img_type = 'lwir',mode ='sequence')
    dataset_pairs = TNO(root_dir, img_type = 'lwir',mode = 'pairs')

    print(f"Length of the 'both' dataset: {len(dataset_both)}") # 235
    print(f"Length of the'sequence' dataset: {len(dataset_seq)}") # 180
    print(f"Length of the 'pairs' dataset: {len(dataset_pairs)}") # 55

def demo_export(root_dir):
    dataset_both_lwir_nir = TNO(
        root_dir, 
        export_lwir_dir = 'lwir',  # default
        export_nir_dir = 'nir',  # default
        export_vis_dir = 'vis',  # default
    )
    dataset_both_lwir_nir.export(Path(root_dir)/'tno'/'export')

def demo_dataloader(root_dir):
    # Dataloader Mode (Default) 
    dataset_both_lwir_nir = TNO(root_dir, img_type = 'both',mode = 'both')  
    for key in dataset_both_lwir_nir[0]:
        print(f"{key}: {type(dataset_both_lwir_nir[0][key])}")
    # vis: <class 'PIL.Image.Image'>
    # lwir: <class 'PIL.Image.Image'>
    # nir: <class 'PIL.Image.Image'>

    # Without Dataloader Mode
    dataset_both_lwir_nir = TNO(root_dir, img_type = 'both',mode = 'both', dataloader = False) 
    for key in dataset_both_lwir_nir[0]:
        print(f"{key}: {type(dataset_both_lwir_nir[0][key])}")  
    # vis: <class 'PIL.Image.Image'>
    # vis_path: <class 'pathlib.PosixPath'>
    # lwir_path: <class 'pathlib.PosixPath'>
    # lwir: <class 'PIL.Image.Image'>
    # nir_path: <class 'pathlib.PosixPath'>
    # nir: <class 'PIL.Image.Image'>

def demo_load_exported(root_dir):
    dataset = TNO(
        root_dir,
        dataloader = False, # To show this is from exported directory
        export_lwir_dir = 'lwir',  # default
        export_nir_dir = 'nir',  # default
        export_vis_dir = 'vis',  # default
        exported = True,
        export_root = Path(root_dir)/'tno'/'export',
    )
    for key in dataset[0]:
        print(f"{key}: {dataset[0][key]}")
    # vis: <PIL.Image.Image image mode=L size=461x381 at 0x16A332B40>
    # vis_path: /Volumes/Charles/data/vision/torchvision/tno/export/vis/127.bmp
    # lwir_path: /Volumes/Charles/data/vision/torchvision/tno/export/lwir/127.bmp
    # lwir: <PIL.Image.Image image mode=L size=461x381 at 0x169E30350>
    
def demo_fusion(root_dir):
    # You need to manually input the fusion images first
    dataset_fuse = TNO(
        root_dir,
        export_lwir_dir = 'lwir',  # default
        export_nir_dir = 'nir',  # default
        export_vis_dir = 'vis',  # default
        export_root = Path(root_dir)/'tno'/'export',
        exported = True,
        fusion_path = Path(root_dir)/'tno'/'export'/'fused'/'fusiongan',
        fused_extension = 'png', # Default
        fusion = True,
    )
    for key in dataset_fuse[0]:
        print(f"{key}: {type(dataset_fuse[0][key])}")
    # vis: <class 'PIL.Image.Image'>
    # lwir: <class 'PIL.Image.Image'>
    # fused: <class 'PIL.Image.Image'>

@click.command()
@click.option('--root_dir', type=click.Path(exists=True), default='/Volumes/Charles/data/vision/torchvision', help='Path to torchvision root directory')
def main(root_dir):
    ''' Auto Download '''
    # demo_auto_download(root_dir) # Download the dataset if it does not exist in the root directory

    ''' Load Different Wavelength Images'''
    # demo_wave_length(root_dir) # nir | lwir | both
    
    ''' Load Different Sets '''
    # demo_set(root_dir) # both | sequence | pairs

    ''' Dataloader Mode '''
    # demo_dataloader(root_dir)  # show image path or not

    ''' Export '''
    # demo_export(root_dir)

    ''' Load from exported '''
    # demo_load_exported(root_dir)

    ''' Fusion Mode (For computing Metrics) '''
    # demo_fusion(root_dir) # Can only load from exported path

if __name__ == '__main__':
    main()