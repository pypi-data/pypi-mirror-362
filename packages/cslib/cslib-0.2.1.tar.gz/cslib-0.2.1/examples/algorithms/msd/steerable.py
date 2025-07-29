import click
from cslib.algorithms.msd import Steerable
from cslib.utils import glance, Options
from cslib.metrics.fusion import ir
import torch.nn.functional as F

@click.command()
@click.option("--pyr_nlevels", type=int, default=5)
@click.option("--pyr_nbands", type=int, default=4)
@click.option("--pyr_scale_factor", type=int, default=2)
@click.option("--image_size", type=int, default=450)
def main(**kwargs):
    opts = Options('Steerable Pyramid', kwargs)
    opts.present()

    pyr = Steerable(
        height=kwargs['pyr_nlevels'], 
        nbands=kwargs['pyr_nbands'],
        scale_factor=kwargs['pyr_scale_factor'],
    )

    resized_img = F.interpolate(ir, size=(kwargs['image_size'],kwargs['image_size']), 
                                mode='bilinear', align_corners=False).float()
    coe = pyr.build(resized_img)
    recon_img = pyr.reconstruct(coe)
    glance([resized_img,recon_img])

if __name__ == '__main__':
    main()