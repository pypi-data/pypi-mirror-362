import click
from cslib.algorithms.msd import Contrust
from cslib.utils import glance, Options
from cslib.metrics.fusion import vis

@click.command()
@click.option('--gau_blur_way',type=click.Choice(['Pytorch','Paper','Adaptive']),default='Pytorch',help='Gaussian blur way')
@click.option('--recon_way',type=click.Choice(['ordinary','orthogonal']),default='ordinary',help='Reconstruction way')
@click.option('--layer',type=int,default=5,help='Layer number')
@click.option('--kernel',type=int,default=5,help='Kernel size')
def main(**kwargs):
    """_summary_
    Args:
        gau_blur_way (str, optional):
            'Pytorch': Pytorch Gaussian blur.
            'Paper': Gaussian blur as described in the paper.
            'Adaptive': Adaptive Gaussian blur.
        recon_way (str, optional): Reconstruction way.
            'ordinary': Ordinary reconstruction.
            'orthogonal': Orthogonal reconstruction, Especially for Blured Images.
        layer (int, optional): Layer number. Defaults to 5.
        kernel (int, optional): Kernel size. Defaults to 5.
    """
    opts = Options('Contrust Pyramid', kwargs)
    opts.present()
    pyramid = Contrust(
        image=vis,
        gau_blur_way=opts.gau_blur_way,
        recon_way=opts.recon_way,
        layer=opts.layer,
        kernel=opts.kernel,
    )
    glance(pyramid.pyramid,suptitle='Contrust Pyramid')
    glance([vis,pyramid.recon],title=['Original','Reconstructed'],suptitle='Contrust Pyramid')

if __name__ == '__main__':
    main()