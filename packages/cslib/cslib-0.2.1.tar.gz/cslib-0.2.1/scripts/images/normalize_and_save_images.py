import os
import numpy as np
from PIL import Image

def normalize_and_save_images(input_folder, output_folder):
    """
    将 input_folder 下的所有 PNG 图片（灰度图像）进行线性归一化，并保存到 output_folder。
    :param input_folder: 包含原始 PNG 图片的文件夹路径
    :param output_folder: 保存归一化后 PNG 图片的文件夹路径
    """
    # 确保输出文件夹存在
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 遍历输入文件夹中的所有 PNG 文件
    for filename in os.listdir(input_folder):
        if filename.endswith(".png"):
            # 构造完整的文件路径
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)

            # 打开图片并转换为灰度模式
            img = Image.open(input_path).convert("L")  # "L" 表示灰度模式
            img_array = np.array(img, dtype=np.float32) / 255.0  # 将像素值归一化到 [0, 1]

            # 线性归一化到 [0, 1]（如果需要进一步归一化，可以取消注释以下代码）
            min_val = img_array.min()
            max_val = img_array.max()
            img_array = (img_array - min_val) / (max_val - min_val)

            # 保存归一化后的图片
            normalized_img = Image.fromarray((img_array * 255).astype(np.uint8))
            normalized_img.save(output_path)

            print(f"Processed and saved: {filename}")

    print("All images have been normalized and saved.")

# 示例用法
if __name__ == "__main__":
    input_folder = "/Users/kimshan/Downloads/kepa/STDFusionNet_Results2"  # 替换为你的输入文件夹路径
    output_folder = "/Users/kimshan/Downloads/kepa/STDFusionNet_Results"  # 替换为你的输出文件夹路径
    normalize_and_save_images(input_folder, output_folder)