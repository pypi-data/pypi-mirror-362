import torch

def rgb_to_ycbcr(tensor):
    transform_matrix = torch.tensor([
        [0.299, 0.587, 0.114],
        [-0.168736, -0.331264, 0.5],
        [0.5, -0.418688, -0.081312]
    ]).float()

    return torch.einsum('kc,cij->kij', transform_matrix,tensor)

def ycbcr_to_rgb(tensor):
    transform_matrix = torch.tensor([
        [0.299, 0.587, 0.114],
        [-0.168736, -0.331264, 0.5],
        [0.5, -0.418688, -0.081312]
    ]).float().inverse()

    return torch.einsum('kc,cij->kij', transform_matrix,tensor)

def to_rgb(image):
    if image.shape[0] == 1:
        image = image.repeat(3, 1, 1)
    return image
