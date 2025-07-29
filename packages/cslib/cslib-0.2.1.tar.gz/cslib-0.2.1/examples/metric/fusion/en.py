from cslib.metrics.fusion import en,en_metric,ir,vis,fused

import numpy as np
import matplotlib.pyplot as plt
import torch

def en_loss(grey_tensor,grey_scale=256):
    return np.log2(grey_scale)-en(grey_tensor)

def vis_entropy():
    def vis_entropy_with_one_var_1D():
        # 生成 p(x) 值
        x_values = np.linspace(0, 1, 100)

        # 计算 {p(x), 1-p(x)} 的信息熵
        entropies = [en(torch.tensor([x,1-x]),is_pdf=True) for x in x_values]

        # 生成曲线图
        plt.subplot(2, 2, 1)
        plt.plot(x_values, entropies)
        plt.xlabel('x')
        plt.ylabel('entropy')
        plt.title('Entropy of (x, 1-x)')

    def vis_entropy_with_one_var_2D():
        # 生成 x 和 y 的网格
        x_values = np.linspace(0, 1, 200)
        y_values = np.linspace(0, 1, 200)
        x, y = np.meshgrid(x_values, y_values)

        # 计算信息熵
        entropies = np.zeros_like(x)
        for i in range(len(x_values)):
            for j in range(len(y_values)):
                entropies[i, j] = en(torch.tensor([x[i, j], y[i, j]]),is_pdf=True)

        #  绘制热图
        plt.subplot(2, 2, 2)
        alpha_values = np.where(np.isclose(x + y, 1, atol=1e-2), 1, 0.2)    # x+y!=的区域设置半透明
        plt.pcolormesh(x, y, entropies, cmap='viridis', alpha=alpha_values)
        plt.colorbar()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Entropy of (x, y)')

    def vis_entropy_with_two_var_2D():
        # 生成 x 和 y 的网格
        x_values = np.linspace(0, 1, 200)
        y_values = np.linspace(0, 1, 200)
        x, y = np.meshgrid(x_values, y_values)

        # 计算信息熵
        z_values = 1 - x - y
        entropies = np.zeros_like(z_values)
        alpha = np.zeros_like(z_values)
        for i in range(len(x_values)):
            for j in range(len(y_values)):
                # 如果 x + y 大于 1，透明度为 0，否则透明度为 1
                alpha[i,j] = 0 if x[i, j] + y[i, j] > 1 else 1
                entropies[i, j] = en(torch.tensor([x[i, j], y[i, j], z_values[i, j]]),is_pdf=True)

        # 绘制热图
        plt.subplot(2, 2, 3)
        plt.pcolormesh(x, y, entropies, cmap='viridis', alpha=alpha)
        plt.colorbar()
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title('Entropy of (x, y, 1-x-y)')

    def vis_entropy_with_two_var_3D():
        # 生成 x, y 的坐标网格
        x_values = np.linspace(0, 1, 200)
        y_values = np.linspace(0, 1, 200)
        xx, yy = np.meshgrid(x_values, y_values)

        # 计算 z 坐标，满足 x + y + z = 1 且 z 大于零
        zz = np.maximum(0, 1 - xx - yy)

        # 过滤掉 z=0 的部分
        mask = zz > 0
        xx = np.where(mask, xx, np.nan)
        yy = np.where(mask, yy, np.nan)
        zz = np.where(mask, zz, np.nan)

        # 计算每个点的信息熵
        entropies = np.array([[en(torch.tensor([x, y, z]), is_pdf=True) for x, y, z in zip(row_x, row_y, row_z)] for row_x, row_y, row_z in zip(xx, yy, zz)])

        # 创建 3D 子图
        ax = plt.subplot(2, 2, 4, projection='3d')
        ax.set_title("Entropy of (x, y, z)")

        # 绘制平面，使用信息熵来确定颜色
        surf = ax.plot_surface(xx, yy, zz, facecolors=plt.cm.viridis(entropies), rstride=5, cstride=5, alpha=0.8)
        surf.set_facecolor((0, 0, 0, 0))

        # 设置坐标轴标签
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

    # 调整子图之间的间距
    plt.subplots_adjust(hspace=0.4, wspace=0.2)

    # 调用各个子图的函数绘制图形
    vis_entropy_with_one_var_1D()
    vis_entropy_with_one_var_2D()
    vis_entropy_with_two_var_2D()
    vis_entropy_with_two_var_3D()

    # 显示图形
    plt.show()

def analyze_entropy_discrepancy():
    def calculate_entropy_uniform(n):
        # 生成 n 个值为 1 的一维数组
        x = np.ones(n)

        # 归一化，使得和为 1
        x_normalized = x / np.sum(x)

        # 计算信息熵
        entropy_value = en(torch.tensor(x_normalized),is_pdf=True)

        return entropy_value

    def calculate_entropy_single_one(n):
        # 生成 n 个值为 0 的一维数组
        x = np.zeros(n)

        # 将其中一个值设为 1
        x[0] = 1

        # 计算信息熵
        entropy_value = en(torch.tensor(x),is_pdf=True)

        return entropy_value

    def calculate_entropy_mid(n):
        x0 = np.zeros(n)
        x0[0] = 1
        x1 = np.ones(n)
        x1 = x1 / x1.sum()
        x = (x0 + x1) / 2

        # 计算信息熵
        entropy_value = en(torch.tensor(x),is_pdf=True)

        return entropy_value

    # 参数范围
    n_values = np.arange(1, 64*64)
    max_entropy = [calculate_entropy_uniform(n) for n in n_values]
    mix_entropy = [calculate_entropy_single_one(n) for n in n_values]
    mid_dis_entropy = [calculate_entropy_mid(n) for n in n_values]
    per = [mid_value / max_value for (mid_value, max_value) in zip(mid_dis_entropy, max_entropy)]

    # 绘制图表
    plt.figure(figsize=(5, 12))

    plt.subplot(2, 1, 1)
    plt.plot(n_values, max_entropy, label='Uniform Distribution')
    plt.plot(n_values, mix_entropy, label='Single 1, Rest 0s')
    plt.plot(n_values, mid_dis_entropy, label='Mid of Center and Single 1')
    plt.xlabel('Parameter n')
    plt.ylabel('Entropy')
    plt.title('Entropy vs. n for Different Sequences')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(n_values, per)
    plt.xlabel('Parameter n')
    plt.ylabel('Entropy Ratio')
    plt.title(f'Entropy Ratio vs. n for 1/2 Distance')

    plt.tight_layout()
    plt.show()

def visualize_image_entropy(size):
    # 计算理论最大值
    theoretical_max_entropy = np.log2(256)
    print("理论最大值(log2 n)：", theoretical_max_entropy)

    # 生成完全覆盖所有像素的张量
    full_tensor = (torch.arange(256*(size**2/256)).view(1, 1, size, size) / (size**2/256)).to(torch.uint8)
    full_tensor_entropy = en(full_tensor)
    print("均匀张量的信息熵：", full_tensor_entropy)

    # 生成随机张量
    random_tensor = torch.randint(0, 256, size=(1, 1, size, size), dtype=torch.uint8)
    random_tensor_entropy = en(random_tensor)
    print("随机张量的信息熵：", random_tensor_entropy)

    # 生成纯色张量
    white_tensor = torch.full((1, 1, size, size), 255, dtype=torch.uint8)
    white_tensor_entropy = en(white_tensor)
    print("白色张量的信息熵：", white_tensor_entropy)

    grey_tensor = torch.full((1, 1, size, size), 127, dtype=torch.uint8)
    grey_tensor_entropy = en(grey_tensor)
    print("灰色张量的信息熵：", grey_tensor_entropy)

    black_tensor = torch.full((1, 1, size, size), 0, dtype=torch.uint8)
    black_tensor_entropy = en(black_tensor)
    print("黑色张量的信息熵：", black_tensor_entropy)

    # 绘制图像
    tensor_colors = ['Uniform', 'Random', 'Grey', 'White', 'Black']
    tensor_list = [full_tensor, random_tensor, grey_tensor, white_tensor, black_tensor]
    entropy_list = [full_tensor_entropy, random_tensor_entropy, grey_tensor_entropy, white_tensor_entropy, black_tensor_entropy]

    fig, axs = plt.subplots(1, len(tensor_list), figsize=(20, 4))

    for i, (tensor, entropy) in enumerate(zip(tensor_list, entropy_list)):
        axs[i].imshow(tensor.view(size, size).numpy(), cmap='gray', vmin=0, vmax=255)
        axs[i].set_title(f'{tensor_colors[i]}\nEntropy: {entropy:.2f}')

    plt.show()

def histogram_compare(tensor,title):
    image = np.clip(tensor.squeeze().detach().numpy() * 255, 0, 255).astype(np.uint8)
    tensor = tensor.view(1, -1) * 255
    # 使用 numpy 统计直方图
    hist_np, bin_edges_np = np.histogram(tensor.numpy(), bins=256, range=[0, 256], density=True)
    en_count = -np.sum(hist_np * np.log2(hist_np + 1e-10))
    # 使用 kornia 核密度直方图
    bins = torch.linspace(0, 255, 256).to(tensor.device)
    sigma_values = [0.01, 0.1, 0.4, 1,8]
    histogram = [kornia.enhance.histogram(tensor, bins=bins, bandwidth=torch.tensor(s)) for s in sigma_values]
    en_kernel = [-torch.sum(h * torch.log2(h + 1e-10)) for h in histogram]
    # 作图
    plt.subplot(2,3,1)
    plt.imshow(image,cmap='grey')
    plt.title(title)
    plt.xticks([]);plt.yticks([])
    for i in range(len(sigma_values)):
        plt.subplot(2,3,i+2)
        plt.title(f"Numpy, EN={format(en_count, '.4f')}\nKornia ("+r"$\sigma$"+f" = {sigma_values[i]}), EN={format(en_kernel[i], '.4f')}")
        plt.plot(bin_edges_np[:-1], hist_np, color='blue', label='Numpy Histogram')
        plt.plot(histogram[i].squeeze().detach().numpy(), color='orange', label='Kornia Histogram')
        plt.xticks([]);plt.yticks([])
    plt.legend()
    plt.show()

def main():
    # Demo
    print(f'EN(ir):{en(ir)}')
    print(f'EN(vis):{en(vis)}')
    print(f'EN(fused):{en(fused)}')
    print(f'EN metric: {en_metric(ir,vis,fused)}')

    # 假设有一个离散随机变量X，给定它的概率分布p(X)
    # p_x = np.array([0.5, 0.5])
    # p_y = np.array([0.3, 0.7])
    # p_z = np.array([0.0, 1.0])
    # print(f"E(X={p_x}) = {en(torch.tensor(p_x),is_pdf=True)}")
    # print(f"E(Y={p_y}) = {en(torch.tensor(p_y),is_pdf=True)}")
    # print(f"E(Z={p_z}) = {en(torch.tensor(p_z),is_pdf=True)}")

    # 信息熵可视化，包含有四个小图
    # 1. 生成 p(x) 值的一维空间，计算(x, 1-x)的信息熵，曲线图展示信息熵随着 x 变化的趋势
    # 2. 在二维空间生成 x 和 y 的网格，计算(x, 1-x)的信息熵，通过热图展示信息熵在不同 x 和 y 值的变化
    # 3. 在二维空间生成 x 和 y 的网格，计算(x, y, 1-x-y)的信息熵，通过热图展示信息熵在不同 x 和 y 值的变化，透明度区分满足条件 x + y = 1 的区域
    # 4. 在三维空间生成 x、y 的坐标网格，计算(x, y, 1-x-y)的信息熵，绘制三维平面，使用信息熵来确定颜色，展示信息熵在三个变量上的分布情况
    # vis_entropy()

    # 根据上面的信息熵可视化，我们发现三维的空间中，值比较高的部分似乎二维的更多
    # 我们计算不同维度的信息熵的最大值最小值，以及在可视化中“中间”位置的点的信息熵
    # analyze_entropy_discrepancy()

    # 下面的例子演示图像信息熵在不同类型图像之间的变化。
    # 通过生成均匀分布、随机分布、纯色、黑白分割等不同特性的图像，
    # 函数展示了这些图像在信息熵上的差异。
    # visualize_image_entropy(16)
    # visualize_image_entropy(64)

    # 下面的例子演示了通过核密度估计与统计的直方图的区别
    # histogram_compare(ir,'IR Image')
    # histogram_compare(vis,'VIS Image')
    # histogram_compare(fused,'Fused Image')

if __name__ == '__main__':
    main()
