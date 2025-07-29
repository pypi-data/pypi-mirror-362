from typing import Optional
import torch
from pathlib import Path
import os
import random
import numpy as np

os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
from torch.utils.tensorboard.writer import SummaryWriter
from torchvision import transforms
from sklearn.model_selection import StratifiedKFold

EPOCH_UNLIMIT = 0
REDUCE_UNLIMIT = 0

class BaseTrainer():
    def __init__(self, opts):
        self.opts = opts
        self._set_seed()
        self._build_folder()
        self._set_components()
        self._valid()
        
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
        torch.manual_seed(self.opts.seed)

        # If CUDA is available, set the random seed for GPU operations
        if torch.cuda.is_available():
            torch.cuda.manual_seed(self.opts.seed)  # Set the seed for the current GPU
            torch.cuda.manual_seed_all(self.opts.seed)  # Set the seed for all GPUs
            torch.backends.cudnn.deterministic = True  # Ensure deterministic behavior for CuDNN algorithms
            torch.backends.cudnn.benchmark = False  # Disable benchmarking to maintain deterministic behavior

        # Set the random seed for NumPy and Python's random module
        np.random.seed(self.opts.seed)
        random.seed(self.opts.seed)

        # Set the seed for DataLoader worker processes
        def seed_worker(worker_id):
            # Derive a worker seed from the initial seed and the worker_id
            worker_seed = torch.initial_seed() % 2**32
            np.random.seed(worker_seed)
            random.seed(worker_seed)
        self.seed_worker = seed_worker

        # Set the Generator for shuffle in DataLoader
        g = torch.Generator()
        g.manual_seed(self.opts.seed)
        self.g = g

    def _set_components(self):
        """
        * Note: All Optional components need to reassign before train.
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
        self.optimizer: Optional[torch.optim.Optimizer] = None
        self.scheduler: Optional[torch.optim.lr_scheduler.LRScheduler|torch.optim.lr_scheduler.ReduceLROnPlateau] = None
        self.criterion: Optional[torch.nn.Module] = None
        self.transform: Optional[transforms.Compose] = None
        self.train_loader: Optional[torch.utils.data.DataLoader] = None
        self.val_loader: Optional[torch.utils.data.DataLoader] = None
        self.test_loader: Optional[torch.utils.data.DataLoader] = None
        self.loss: Optional[torch.Tensor] = None
        self.writer = SummaryWriter(log_dir=self.opts.model_base_path)

    def _build_folder(self):
        """
        * Note 1: The function ensures save results in a new folder. 
        * Note 2: You should use with shell file.
        * Example
        >>> RES_PATH="${BASE_PATH}/Model/RCNN/Flowers17"
        >>> NAME=$(date +'%Y_%m_%d_%H_%M')
        >>> mkdir -p "${RES_PATH}/${NAME}"
        """
        assert hasattr(self.opts, "model_base_path")
        assert Path(self.opts.model_base_path).exists()
        if list(Path(self.opts.model_base_path).iterdir()):
            raise SystemError(f"{self.opts.model_base_path} should be empty")
        (Path(self.opts.model_base_path) / 'checkpoints').mkdir()

    def _valid(self):
        if self.opts.lr_scheduler == 'ReduceLROnPlateau':
            if self.opts.max_epoch == self.opts.max_reduce == EPOCH_UNLIMIT:
                raise ValueError("epoch and reduce can't unlimit both.")
            self._current_lr = self.opts.lr
            self._reduce_count = 0

    def save_opts(self):
        """
        Save opts
        """
        self.opts.save()
    
    def save_checkpoint(self,epoch):#TODO
        """
        Save ckpt
        """
        assert self.model is not None
        assert self.optimizer is not None
        assert self.loss is not None
        checkpoint = {
            'epoch': epoch,
            'model_state_dict': self.model.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'loss': self.loss.item()
        }
        torch.save(checkpoint, Path(self.opts.model_base_path) / f"checkpoints/{epoch}.pt")
        if epoch > 10:
            (Path(self.opts.model_base_path) / f"checkpoints/{epoch-10}.pt").unlink()
    
    def test(self):
        raise RuntimeError("You should implement in subclass")
    
    def get_lr(self):
        if isinstance(self.scheduler,torch.optim.lr_scheduler.ReduceLROnPlateau):
            return self.scheduler.optimizer.param_groups[0]['lr']
        else:
            assert ValueError("Not realized yet!")

    def _is_last_epoch(self,epoch):
        if self.opts.max_epoch != EPOCH_UNLIMIT:
            if epoch == self.opts.max_epoch:
                return True
                
        if isinstance(self.scheduler,torch.optim.lr_scheduler.ReduceLROnPlateau):
            if self._current_lr != self.get_lr():
                self._current_lr = self.get_lr()
                self._reduce_count += 1
                if self._reduce_count == self.opts.max_reduce:
                    return True
            
        else:
            assert ValueError("Not realized yet!")
        
        return False
    
    def holdout(self):
        epoch = 1
        while True:
            self.holdout_train(epoch)
            self.holdout_validate(epoch)
            self.save_checkpoint(epoch)
            if self._is_last_epoch(epoch):
                print("Training has converged. Stopping...")
                break
            epoch+=1

    def holdout_train(self, epoch):
        raise RuntimeError("You should implement in subclass")

    def holdout_validate(self, epoch):
        raise RuntimeError("You should implement in subclass")

    def k_fold(self):
        self.skf = StratifiedKFold(n_splits=self.opts.fold_num)

    def train(self):
        self.opts.presentParameters()
        assert self.model is not None
        self.model.to(self.opts.device)
        if self.opts.train_mode == "Holdout":
            self.holdout()
        elif self.opts.train_mode == "K-fold":
            self.k_fold()
        else:
            self.holdout()
        self.test()
        self.save_opts()
