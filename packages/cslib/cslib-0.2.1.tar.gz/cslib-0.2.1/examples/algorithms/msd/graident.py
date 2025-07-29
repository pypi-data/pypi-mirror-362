import click
from cslib.algorithms.msd import Graident
from cslib.utils import glance, Options
from cslib.metrics.fusion import vis

@click.command()
@click.option('--gau_blur_way',type=click.Choice(['Pytorch','Paper','Adaptive']),default='Pytorch',help='Gaussian blur way')
@click.option('--recon_way',type=click.Choice(['ordinary','orthogonal']),default='ordinary',help='Reconstruction way')
@click.option('--layer',type=int,default=5,help='Layer number')
@click.option('--kernel',type=int,default=5,help='Kernel size')
@click.option('--sigma',type=float,default=1.0,help='Sigma')
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
        sigma (float, optional): Sigma. Defaults to 1.0.
    """
    opts = Options('Graident Pyramid', kwargs)
    opts.present()
    pyramid = Graident(
        image=vis,
        gau_blur_way=opts.gau_blur_way,
        recon_way=opts.recon_way,
        layer=opts.layer,
        kernel=opts.kernel,
        sigma=opts.sigma
    )
    temp = []
    for i in range(pyramid.layer):
        temp+=pyramid.pyramid[i]
    glance(temp,suptitle='Graident Pyramid',shape=(4, opts.layer))
    glance([vis,pyramid.recon],title=['Original','Reconstructed'],suptitle='Graident Pyramid')

if __name__ == '__main__':
    main()