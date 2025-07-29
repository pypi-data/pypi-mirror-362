from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'rmse',
    'rmse_approach_loss',
    'rmse_metric'
]

def rmse(y_true: torch.Tensor, y_pred: torch.Tensor, eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Root Mean Squared Error (RMSE) between true and predicted values.

    Args:
        y_true (torch.Tensor): The true values tensor.
        y_pred (torch.Tensor): The predicted values tensor.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The RMSE between true and predicted values.

    Reference:
        [1] P. Jagalingam and A. V. Hegde, "A review of quality metrics for fused image,"
        Aquatic Procedia, vol. 4, no. Icwrcoe, pp. 133-142, 2015.
    """
    mse_loss = torch.mean((y_true - y_pred)**2)
    rmse_loss = torch.sqrt(mse_loss + eps)
    return rmse_loss

rmse_approach_loss = rmse

# 与 VIFB 统一
@fusion_preprocessing
def rmse_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5
    return w0 * rmse(A, F) + w1 * rmse(B, F)

if __name__ == '__main__':
    from cslib.metrics.fusion import vis,ir,fused
    print(rmse_metric(ir,vis,fused).item())
    print(rmse_metric(ir,vis.repeat(1, 3, 1, 1),fused.repeat(1, 3, 1, 1)).item())
    print(rmse_metric(ir,vis.repeat(1, 3, 1, 1),fused).item())
