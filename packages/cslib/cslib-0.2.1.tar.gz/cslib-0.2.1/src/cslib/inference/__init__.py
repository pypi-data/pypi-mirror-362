from typing import Optional
import torch
import os
import random
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from torchvision import transforms

EPOCH_UNLIMIT = 0
REDUCE_UNLIMIT = 0

class BaseInferencer():
    def __init__(self, opts):
        self.opts = opts
        self._set_seed()
        self._set_components()
        
    def _set_seed(self):
        """
        * Note: The seed_worker function should be used as the 
                worker_init_fn argument when creating a DataLoader
        * Example usage:
        >>> trainer = ClassifyTrainer(opts)
        >>> trainer.train_loader = DataLoader(
        ...     dataset=train_dataset,
        ...     batch_size=opts.batch_size,
        ...     shuffle=True,
        ...     worker_init_fn=trainer.seed_worker,
        ...     generator=trainer.g
        ... )
        """
        # Set the random seed for CPU operations
        torch.manual_seed(42)

        # If CUDA is available, set the random seed for GPU operations
        if torch.cuda.is_available():
            torch.cuda.manual_seed(42)  # Set the seed for the current GPU
            torch.cuda.manual_seed_all(42)  # Set the seed for all GPUs
            torch.backends.cudnn.deterministic = True  # Ensure deterministic behavior for CuDNN algorithms
            torch.backends.cudnn.benchmark = False  # Disable benchmarking to maintain deterministic behavior

        # Set the random seed for NumPy and Python's random module
        np.random.seed(42)
        random.seed(42)

        # Set the seed for DataLoader worker processes
        def seed_worker(worker_id):
            # Derive a worker seed from the initial seed and the worker_id
            worker_seed = torch.initial_seed() % 2**32
            np.random.seed(worker_seed)
            random.seed(worker_seed)
        self.seed_worker = seed_worker

        # Set the Generator for shuffle in DataLoader
        g = torch.Generator()
        g.manual_seed(42)
        self.g = g

    def _set_components(self):
        """
        * Note: All Optional components need to reassign before inference.
        * Example usage:
        >>> trainer = ClassifyTrainer(opts)
        >>> trainer.model = AlexNet(
        ...     num_classes=opts.num_classes,
        ...     classify=True,
        ...     fine_tuning=False
        ... )
        ... ... 
        """
        self.model: Optional[torch.nn.Module] = None
        self.criterion: Optional[torch.nn.Module] = None
        self.transform: Optional[transforms.Compose] = None
        self.test_loader: Optional[torch.utils.data.DataLoader] = None
        self.loss: Optional[torch.Tensor] = None
    
    def load_checkpoint(self):#TODO
        """
        Load ckpt
        """
        assert self.model is not None
        params = torch.load(
            self.opts.model_path, 
            map_location=self.opts.device,
            weights_only=True
        )
        self.model.load_state_dict(params['model_state_dict'])
    
    def test(self):
        raise RuntimeError("You should implement in subclass")
