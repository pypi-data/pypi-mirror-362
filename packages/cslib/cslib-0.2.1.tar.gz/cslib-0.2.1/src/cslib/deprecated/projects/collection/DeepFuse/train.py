import torch
from torch.optim import Adam
import torchvision.transforms as transforms
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

from .loss import MEF_SSIM_Loss
from ....transforms import to_rgb,rgb_to_ycbcr

def train_trans(opts):
    return transforms.Compose([
                transforms.ToTensor(),
                transforms.Resize((opts.W, opts.H), antialias=True), # type: ignore
                transforms.Lambda(to_rgb),
                transforms.Lambda(rgb_to_ycbcr),
                transforms.Normalize(mean = [0.485, 0.456, 0.406], std = [0.229, 0.224, 0.225])
            ])

def train(model,dataloader,opts):
    # Create the model
    criterion = MEF_SSIM_Loss().to(opts.device)
    optimizer = Adam(model.parameters(), lr = 0.0002)
    Loss_list = []

    # train
    bar = tqdm(range(opts.epoch))
    for ep in bar:
        loss_list = []
        for batch in dataloader:                
            # Extract the luminance and move to computation device
            patch1, patch2 = batch['ir'].to(opts.device), batch['ir'].to(opts.device)
            patch1_lum = patch1[:, 0:1]
            patch2_lum = patch2[:, 0:1]

            # Forward and compute loss
            model.setInput(patch1_lum, patch2_lum)
            y_f  = model.forward()
            loss, y_hat = criterion(y_1 = patch1_lum, y_2 = patch2_lum, y_f = y_f)
            loss_list.append(loss.item())
            bar.set_description("Epoch: %d   Loss: %.6f" % (ep, loss_list[-1]))

            # Update the parameters
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        Loss_list.append(np.mean(loss_list))

        # # Save the training image
        # if ep % opts.record_epoch == 0:
        #     img = fusePostProcess(y_f, y_hat, patch1, patch2, single = False)
        #     cv2.imwrite(Path(opts.det,'image', str(ep) + ".png"), img[0, :, :, :])

        # # Save the training model
        # if ep % (opts.epoch // 5) == 0:
        #     model_name = str(ep) + ".pth"
        # else:
        #     model_name = "latest.pth"
        # state = {
        #     'model': model.state_dict(),
        #     'loss' : Loss_list
        # }
        # torch.save(state, os.path.join(opts.det, 'model', model_name))

    # Plot the loss curve
    plt.clf()
    plt.plot(Loss_list, '-')
    plt.title("loss curve")
    plt.savefig(Path(opts.det, 'image', "curve.png"))