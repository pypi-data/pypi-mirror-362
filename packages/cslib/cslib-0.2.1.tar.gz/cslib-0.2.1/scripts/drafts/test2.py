import torch
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.transforms as transforms

def compute_saliency_map(image_path):
    """
    输入: 图片路径 (支持jpg/png等)
    输出: 显示显著图并保存结果
    """
    # 1. 读取图像 -> 灰度 -> 张量
    img = Image.open(image_path).convert('L')
    tensor = transforms.ToTensor()(img) * 255  # [1,H,W], 范围[0,255]
    print(tensor.shape)
    # 2. 计算直方图 (Mj)
    hist = torch.histc(tensor, bins=256, min=0, max=255)  # Mj
    
    # 3. 预计算显著性表 (公式9: V(p)=Σ Mj*|Ip-Ij|)
    bins = torch.arange(256, device=tensor.device)
    sal_tab = torch.sum(hist * torch.abs(bins.unsqueeze(1) - bins), dim=1)
    
    # 4. 映射回原图
    saliency = sal_tab[tensor.long().flatten()].view_as(tensor)
    saliency = (saliency - saliency.min()) / (saliency.max() - saliency.min())  # 归一化
    
    # 5. 可视化
    plt.figure(figsize=(12, 6))
    plt.subplot(121), plt.imshow(img, cmap='gray'), plt.title('Original')
    plt.subplot(122), plt.imshow(saliency.squeeze(), cmap='hot'), plt.title('Saliency Map')
    plt.colorbar()
    # plt.savefig('saliency_result.jpg', bbox_inches='tight')
    plt.show()

# 使用示例（只需修改这里！）
if __name__ == "__main__":
    compute_saliency_map("/Users/kimshan/Public/data/vision/torchvision/m3fd/fusion/vis/00825.png")  # ← 替换为你的图片路径