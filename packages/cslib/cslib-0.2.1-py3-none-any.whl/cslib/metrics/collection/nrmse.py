from cslib.metrics.utils import fusion_preprocessing
import torch

__all__ = [
    'nrmse',
    'nrmse_approach_loss',
    'nrmse_metric'
]

def nrmse(y_true: torch.Tensor, y_pred: torch.Tensor, normalization='euclidean', eps: float = 1e-10) -> torch.Tensor:
    """
    Calculate the Normalized Root Mean Squared Error (NRMSE) between true and predicted values.

    Args:
        y_true (torch.Tensor): The true values tensor.
        y_pred (torch.Tensor): The predicted values tensor.
        eps (float, optional): A small value to avoid numerical instability. Default is 1e-10.

    Returns:
        torch.Tensor: The NRMSE between true and predicted values.

    Reference:
        [1] https://scikit-image.org/docs/stable/api/skimage.metrics.html#skimage.metrics.normalized_root_mse
        [2] https://blog.csdn.net/weixin_43465015/article/details/105524728 
    """
    mse = torch.nn.functional.mse_loss(target=y_true, input=y_pred)
    if normalization == 'euclidean':
        denom = torch.sqrt(torch.mean(y_true ** 2))
    elif normalization == 'min-max':
        denom = y_true.max() - y_true.min()
    elif normalization == 'mean':
        denom = y_true.mean()
    else:
        raise ValueError("Unsupported normalization method. Choose from 'euclidean', 'min-max', or 'mean'.")
    return torch.sqrt(mse + eps) / denom

nrmse_approach_loss = nrmse

# 与 skimage 保持一致
@fusion_preprocessing
def nrmse_metric(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor) -> torch.Tensor:
    w0 = w1 = 0.5 # skimage is default normalization='euclidean'
    return w0 * nrmse(A, F, normalization='euclidean') + w1 * nrmse(B, F, normalization='euclidean')

def main():
    from cslib.metrics.fusion import ir,vis,fused
    from cslib.utils import to_numpy
    from skimage.metrics import normalized_root_mse

    [ir_array, vis_array, fused_array] = [to_numpy(i) for i in [ir,vis,fused]]

    print(f'NRMSE(ir,ir):{nrmse(ir,ir)}')
    print(f'NRMSE(ir,vis):{nrmse(ir,vis)}')
    print(f'NRMSE(ir,fused):{nrmse(ir,fused)}\n')

    print(f'NRMSE(ir,ir) skimage euclidean:{normalized_root_mse(ir_array,ir_array, normalization='euclidean')}')
    print(f'NRMSE(ir,vis) skimage euclidean:{normalized_root_mse(ir_array,vis_array, normalization='euclidean')}')
    print(f'NRMSE(ir,fused) skimage euclidean:{normalized_root_mse(ir_array,fused_array, normalization='euclidean')}\n')

    print(f'NRMSE(ir,ir) skimage min-max:{normalized_root_mse(ir_array,ir_array, normalization='min-max')}')
    print(f'NRMSE(ir,vis) skimage min-max:{normalized_root_mse(ir_array,vis_array, normalization='min-max')}')
    print(f'NRMSE(ir,fused) skimage min-max:{normalized_root_mse(ir_array,fused_array, normalization='min-max')}\n')
    
    print(f'NRMSE(ir,ir) skimage mean:{normalized_root_mse(ir_array,ir_array, normalization='mean')}')
    print(f'NRMSE(ir,vis) skimage mean:{normalized_root_mse(ir_array,vis_array, normalization='mean')}')
    print(f'NRMSE(ir,fused) skimage mean:{normalized_root_mse(ir_array,fused_array, normalization='mean')}\n')

    print(f'NRMSE metric:{nrmse_metric(vis, ir, fused)}')

if __name__ == '__main__':
    main()
