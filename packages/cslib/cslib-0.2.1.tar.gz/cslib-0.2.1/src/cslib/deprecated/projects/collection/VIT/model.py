import torch
import torch.nn as nn

def load_model(opts):
    model = VIT().to(opts.device)
    params = torch.load(opts.pre_trained, map_location=opts.device)
    model.load_state_dict(params)
    return model

class VIT(nn.Module):
    def __init__(self):
        super(VIT, self).__init__()
    
    def forward(self, x):
        return x
