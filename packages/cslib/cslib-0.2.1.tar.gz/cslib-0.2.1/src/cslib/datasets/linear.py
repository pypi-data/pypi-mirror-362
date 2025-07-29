import torch
from torch.utils.data import Dataset

def linear_points(w, b, num_examples, noise=True):
    """Generate linear data based on input dimension from w's shape and noise option.
    
    Args:
    - w (tensor): Coefficients for the linear function.
    - b (float): Bias term.
    - num_examples (int): Number of data points to generate.
    - noise (bool): Whether to add noise to the output.
    
    Returns:
    - X (tensor): Input features of shape (num_examples, dim).
    - y (tensor): Output labels of shape (num_examples, 1).

    Example:
    ```
    true_w = torch.tensor([2, -3.4])
    true_b = 4.2
    features, labels = linear_points(true_w, true_b, 1000, noise=True)

    print(features[:5])
    print(labels[:5])
    ```
    """
    
    # Get the dimension of w
    dim = len(w)
    
    # Generate input features
    X = torch.normal(0, 1, (num_examples, dim))
    
    # Generate output labels
    y = torch.matmul(X, w) + b
    
    # Optionally add noise
    if noise:
        y += torch.normal(0, 0.01, y.shape)
    
    return X, y.reshape((-1, 1))

class LinearDataset(Dataset):
    """ Dataset of Linear Points with function linear_points
    Example:
    ```
    true_w = torch.tensor([2, -3.4])
    true_b = 4.2
    dataset = LinearDataset(true_w, true_b, 1000, noise=True)
    for i in range(5):
        print(dataset[i])
    ```
    """
    def __init__(self, w, b, num_examples, noise=True):
        super(LinearDataset, self).__init__()
        self.features, self.labels = linear_points(w, b, num_examples, noise)
        
    def __len__(self):
        return len(self.labels)
    
    def __getitem__(self, index):
        return self.features[index], self.labels[index]
