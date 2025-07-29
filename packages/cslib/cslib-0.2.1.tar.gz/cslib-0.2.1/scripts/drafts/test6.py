import numpy as np
from scipy.signal import convolve2d

def guidedfilter(I, p, r, eps):
    """
    GUIDEDFILTER   O(1) time implementation of guided filter.

    - guidance image: I (should be a gray-scale/single channel image)
    - filtering input image: p (should be a gray-scale/single channel image)
    - local window radius: r
    - regularization parameter: eps
    """
    hei, wid = I.shape
    # 定义盒式滤波核
    box_kernel = np.ones((2 * r + 1, 2 * r + 1))
    # 每个局部窗口的大小
    N = convolve2d(np.ones((hei, wid)), box_kernel, mode='same', boundary='symm')
    # I 的局部均值
    mean_I = convolve2d(I, box_kernel, mode='same', boundary='symm') / N
    # p 的局部均值
    mean_p = convolve2d(p, box_kernel, mode='same', boundary='symm') / N
    # I * p 的局部均值
    mean_Ip = convolve2d(I * p, box_kernel, mode='same', boundary='symm') / N
    # 局部协方差
    cov_Ip = mean_Ip - mean_I * mean_p
    # I 的局部方差
    mean_II = convolve2d(I * I, box_kernel, mode='same', boundary='symm') / N
    var_I = mean_II - mean_I * mean_I
    # 计算 a，对应论文中的公式 (5)
    a = cov_Ip / (var_I + eps)
    # 计算 b，对应论文中的公式 (6)
    b = mean_p - a * mean_I
    # a 的局部均值
    mean_a = convolve2d(a, box_kernel, mode='same', boundary='symm') / N
    # b 的局部均值
    mean_b = convolve2d(b, box_kernel, mode='same', boundary='symm') / N
    # 计算输出 q，对应论文中的公式 (8)
    q = mean_a * I + mean_b
    return q

# 示例调用
if __name__ == "__main__":
    from skimage import data
    import matplotlib.pyplot as plt

    # 读取灰度图像
    image = data.camera()
    # 引导图像和输入图像相同
    guidance = image
    radius = 5
    eps = 0.01
    # 应用引导滤波
    filtered_image = guidedfilter(guidance, image, radius, eps)
    # 计算原图减去引导滤波后的图像
    diff_image = image - filtered_image

    # 显示结果
    plt.figure(figsize=(18, 6))
    plt.subplot(1, 3, 1)
    plt.imshow(image, cmap='gray')
    plt.title('Original Image')
    plt.axis('off')

    plt.subplot(1, 3, 2)
    plt.imshow(filtered_image, cmap='gray')
    plt.title('Guided Filtered Image')
    plt.axis('off')

    plt.subplot(1, 3, 3)
    plt.imshow(diff_image, cmap='gray')
    plt.title('Original - Guided Filtered')
    plt.axis('off')

    plt.show()