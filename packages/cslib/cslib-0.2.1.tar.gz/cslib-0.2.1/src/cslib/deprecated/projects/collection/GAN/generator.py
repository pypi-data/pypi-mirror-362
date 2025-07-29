import torch
from torch.autograd import Variable
import numpy as np

from .model import Generator, Discriminator
from ....utils import glance
def generate(opts):
    generator = Generator(opts.latent_dim, opts.img_shape).to(opts.device)
    generator.load_state_dict(torch.load(opts.pre_trained,map_location=opts.device))
    Tensor = torch.FloatTensor if opts.device == 'cpu' else torch.cuda.FloatTensor  # type: ignore
    z = Variable(Tensor(np.random.normal(0, 1, (opts.batch_size, opts.latent_dim))))
    gen_imgs = generator(z)
    glance(gen_imgs[0,:,:,:])
    glance(gen_imgs[1,:,:,:])
    glance(gen_imgs[2,:,:,:])
    glance(gen_imgs[3,:,:,:])
