import os
import numpy as np
from pathlib import Path
import torch
import torch.nn as nn
from torch.autograd import Variable
import torchvision.transforms as transforms
from torchvision import datasets
from torchvision.utils import save_image

from .model import Generator, Discriminator

def train(opts):
    # Configure data loader
    os.makedirs(opts.images_path, exist_ok=True)
    os.makedirs(opts.dataset_path, exist_ok=True)
    os.makedirs(opts.models_path, exist_ok=True)
    dataloader = torch.utils.data.DataLoader(
        datasets.MNIST(
            opts.dataset_path,
            train=True,
            download=True,
            transform=transforms.Compose([
                transforms.Resize(opts.img_size), 
                transforms.ToTensor(), 
                transforms.Normalize([0.5], [0.5])
            ]),
        ),
        batch_size=opts.batch_size,
        shuffle=True,
    )

    # Loss function
    adversarial_loss = nn.BCELoss().to(opts.device)

    # Initialize generator and discriminator
    generator = Generator(opts.latent_dim, opts.img_shape).to(opts.device)
    discriminator = Discriminator(opts.img_shape).to(opts.device)

    # Optimizers
    optimizer_G = torch.optim.Adam(generator.parameters(), lr=opts.lr, betas=(opts.b1, opts.b2))
    optimizer_D = torch.optim.Adam(discriminator.parameters(), lr=opts.lr, betas=(opts.b1, opts.b2))
    Tensor = torch.FloatTensor if opts.device == 'cpu' else torch.cuda.FloatTensor  # type: ignore

    # ----------
    #  Training
    # ----------

    for epoch in range(opts.n_epochs):
        for i, (imgs, _) in enumerate(dataloader):

            # Adversarial ground truths
            valid = Variable(Tensor(imgs.size(0), 1).fill_(1.0), requires_grad=False)
            fake = Variable(Tensor(imgs.size(0), 1).fill_(0.0), requires_grad=False)

            # Configure input
            real_imgs = Variable(imgs.type(Tensor))

            # -----------------
            #  Train Generator
            # -----------------

            optimizer_G.zero_grad()

            # Sample noise as generator input
            z = Variable(Tensor(np.random.normal(0, 1, (imgs.shape[0], opts.latent_dim))))

            # Generate a batch of images
            gen_imgs = generator(z)

            # Loss measures generator's ability to fool the discriminator
            g_loss = adversarial_loss(discriminator(gen_imgs), valid)

            g_loss.backward()
            optimizer_G.step()

            # ---------------------
            #  Train Discriminator
            # ---------------------

            optimizer_D.zero_grad()

            # Measure discriminator's ability to classify real from generated samples
            real_loss = adversarial_loss(discriminator(real_imgs), valid)
            fake_loss = adversarial_loss(discriminator(gen_imgs.detach()), fake)
            d_loss = (real_loss + fake_loss) / 2

            d_loss.backward()
            optimizer_D.step()

            print(
                "[Epoch %d/%d] [Batch %d/%d] [D loss: %f] [G loss: %f]"
                % (epoch, opts.n_epochs, i, len(dataloader), d_loss.item(), g_loss.item())
            )

            batches_done = epoch * len(dataloader) + i
            if batches_done % opts.sample_interval == 0:
                save_image(gen_imgs.data[:25], Path(opts.images_path, f"{batches_done}.png"), nrow=5, normalize=True)

        if epoch == opts.n_epochs - 1:
            print("Saving the model at the end of the last epoch")
            torch.save(generator.state_dict(), Path(opts.models_path, "generator.pth"))
            torch.save(discriminator.state_dict(), Path(opts.models_path, "discriminator.pth"))
