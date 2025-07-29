import torch
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
import config

# 设置数据加载器
batch_size = 64
transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

# MNIST
train_data = datasets.MNIST(root=config.TorchVisionPath, train=True, download=True, transform=transform)

# EMNIST
# 'byclass': 814,255 张图像，62 类字符，包括数字和字母（大小写不区分）。
# 'bymerge': 814,255 张图像，47 类字符，包括数字和大小写字母，但合并了相似的字符（如 'C' 和 'c'）。
# 'balanced': 131,600 张图像，47 类字符，较平衡的样本分布。
# 'letters': 145,600 张图像，26 类字符，仅包含字母（大小写不区分）。
# 'digits': 280,000 张图像，10 类字符，仅包含数字。
# 'mnist': 70,000 张图像，10 类字符，仅包含数字，类似于原始 MNIST 数据集。
# train_data = datasets.EMNIST(root='/Volumes/Charles/DateSets/torchvision', split='byclass',train=True, download=True, transform=transform)
# train_data = datasets.EMNIST(root='/Volumes/Charles/DateSets/torchvision', split='bymerge',train=True, download=True, transform=transform)
# train_data = datasets.EMNIST(root='/Volumes/Charles/DateSets/torchvision', split='balanced',train=True, download=True, transform=transform)
# train_data = datasets.EMNIST(root='/Volumes/Charles/DateSets/torchvision', split='letters',train=True, download=True, transform=transform)
# train_data = datasets.EMNIST(root='/Volumes/Charles/DateSets/torchvision', split='digits',train=True, download=True, transform=transform)
# train_data = datasets.EMNIST(root='/Volumes/Charles/DateSets/torchvision', split='mnist',train=True, download=True, transform=transform)

# FashionMNIST
# train_data = datasets.FashionMNIST(root='/Volumes/Charles/DateSets/torchvision',train=True, download=True, transform=transform)

# QMNIST
# train_data = datasets.QMNIST(root='/Volumes/Charles/DateSets/torchvision',train=True, download=True, transform=transform)

# KMNIST
# train_data = datasets.KMNIST(root='/Volumes/Charles/DateSets/torchvision',train=True, download=True, transform=transform)

train_loader = torch.utils.data.DataLoader(dataset=train_data, batch_size=batch_size, shuffle=True)

# 加载数据
num_images = 10
count = 0
for images, labels in train_loader:
    if count >= num_images:
        break
    count += 1
    plt.subplot(2, 5, count)
    plt.imshow(images[0].squeeze(), cmap='gray') # 每个 batch 里边的第一个
    plt.xlabel(labels[0].item())

plt.show()
