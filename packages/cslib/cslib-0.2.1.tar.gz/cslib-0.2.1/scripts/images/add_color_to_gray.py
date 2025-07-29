import os
import numpy as np
from PIL import Image
import imageio
import click

@click.command()
@click.option("--src_color", default="/Users/kimshan/Public/data/vision/torchvision/m3fd/fusion/vis", type=click.Path(exists=True, file_okay=False, resolve_path=True), help="彩色图片文件夹路径，默认为 './color_images'")
@click.option("--src_gray", default="/Users/kimshan/Public/data/vision/torchvision/m3fd/lunwen/DATFuse1", type=click.Path(exists=True, file_okay=False, resolve_path=True), help="灰度图片文件夹路径，默认为 './gray_images'")
@click.option("--dst", default="/Users/kimshan/Public/data/vision/torchvision/m3fd/lunwen/DATFuse", type=click.Path(file_okay=False, resolve_path=True), help="目标文件夹路径，默认为 './output_images'")
def replace_y_channel(src_color, src_gray, dst):
    """
    批量处理图片：将彩色图片的 Y 通道替换为灰度图片的 Y 通道，并保存为新的 RGB 图片。
    """
    # 确保目标文件夹存在
    if not os.path.exists(dst):
        os.makedirs(dst)
        print(f"创建目标文件夹：{dst}")

    # 获取两个文件夹中的文件列表
    color_files = sorted([f for f in os.listdir(src_color) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])
    gray_files = sorted([f for f in os.listdir(src_gray) if f.lower().endswith(('.png', '.jpg', '.jpeg'))])

    # 检查文件数量是否一致
    if len(color_files) != len(gray_files):
        raise ValueError("彩色图片文件夹和灰度图片文件夹中的文件数量不一致！")

    for color_file, gray_file in zip(color_files, gray_files):
        # 构建完整的文件路径
        color_path = os.path.join(src_color, color_file)
        gray_path = os.path.join(src_gray, gray_file)

        # 检查文件扩展名
        if not (color_file.lower().endswith(('.png', '.jpg', '.jpeg')) and
                gray_file.lower().endswith(('.png', '.jpg', '.jpeg'))):
            print(f"跳过非图片文件：{color_file} 或 {gray_file}")
            continue

        try:
            # 读取彩色图片为 YCbCr 格式
            color_image = imageio.imread(color_path, mode='YCbCr').astype(np.float32)

            # 读取灰度图片为灰度图
            gray_image = imageio.imread(gray_path, mode='L').astype(np.float32)

            # 检查图片尺寸是否一致
            if color_image.shape[:2] != gray_image.shape:
                raise ValueError(f"图片尺寸不一致：{color_file} 和 {gray_file}")

            # 替换 Y 通道
            color_image[:, :, 0] = gray_image

            # 转换回 RGB 格式
            temp = np.clip(color_image, 0, 255).astype(np.uint8)
            result_image = np.asarray(Image.fromarray(temp, 'YCbCr').convert('RGB'))

            # 保存结果图片
            dst_path = os.path.join(dst, color_file)
            imageio.imwrite(dst_path, result_image)
            print(f"处理完成：{color_file} -> {dst_path}")

        except Exception as e:
            print(f"处理图片 {color_file} 和 {gray_file} 时出错：{e}")

if __name__ == "__main__":
    replace_y_channel()