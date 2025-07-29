from functools import wraps
import torch

def fusion_preprocessing(func):
    @wraps(func)
    def wrapper(A: torch.Tensor, B: torch.Tensor, F: torch.Tensor):
        # Ensure the dimension is (B, C, H, W)
        if A.ndim == 3:
            [A, B, F] = [I.unsqueeze(0) for I in [A, B, F]]
        assert A.ndim == 4

        # Ensure the channel is 1 or 3
        [c1, c2, c3] = [I.shape[1] for I in [A, B, F]]
        if max(c1,c2,c3) == 3 and min(c1,c2,c3) == 1:
            [A, B, F] = [I.repeat(1, 3, 1, 1) if I.shape[1] == 1 else I for I in [A, B, F]]
        assert A.shape == B.shape == F.shape
        assert A.shape[1] == 3 or A.shape[1] == 1
        
        # Calculate fusion metrics based on batch size and channel number
        [a,b,f] = [[I[i:i+1,...] for i in range(I.shape[0])] for I in [A,B,F]]
        res = []
        for ai,bi,fi in zip(a,b,f):
            if ai.shape[1] == 3:
                res.append(torch.stack([func(ai[:,i:i+1,:,:],bi[:,i:i+1,:,:],fi[:,i:i+1,:,:]) for i in range(F.shape[1])]).mean())
            else:
                res.append(func(ai,bi,fi))
        
        return res[0] if A.shape[0] == 1 else res
        
    return wrapper