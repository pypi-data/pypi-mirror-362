from cslib.metrics.utils import fusion_preprocessing
import torch
import torch.nn.functional as F

__all__ = [
    'mse',
    'mse_approach_loss',
    'mse_metric'
]

def mse(y_true: torch.Tensor, y_pred: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Mean Squared Error (MSE) between true and predicted values.

    Args:
        y_true (torch.Tensor): The true values tensor.
        y_pred (torch.Tensor): The predicted values tensor.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The MSE between true and predicted values.
    """
    return torch.mean((y_true - y_pred)**2)

mse_approach_loss = mse

@fusion_preprocessing
def mse_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5
    return w0 * mse(A, F) + w1 * mse(B, F)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(mse_metric(ir,vis,fused).item())
