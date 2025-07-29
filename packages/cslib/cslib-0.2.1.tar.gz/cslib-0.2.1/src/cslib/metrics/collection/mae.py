from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'mae',
    'mae_approach_loss',
    'mae_metric'
]

def mae(y_true: torch.Tensor, y_pred: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Mean Absolute Error (MAE) between true and predicted values.

    Args:
        y_true (torch.Tensor): The true values tensor.
        y_pred (torch.Tensor): The predicted values tensor.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The MAE between true and predicted values.
    """
    return torch.mean(torch.abs(y_true - y_pred + eps))

mae_approach_loss = mae

@fusion_preprocessing
def mae_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5
    return w0 * mae(A, F) + w1 * mae(B, F)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(mae_metric(ir,vis,fused).item())

