import os
from PIL import Image
import click
import numpy as np

@click.command()
@click.option("--src", default="/Users/kimshan/Public/project/cvplayground/scenefuse/samples/glance_outputs",required=True, type=click.Path(exists=True, file_okay=False),
              help="包含图片的源文件夹路径")
@click.option("--dst", default="/Users/kimshan/Public/project/cvplayground/scenefuse/samples/adjusted_images", type=click.Path(file_okay=False),
              help="输出文件夹路径，默认为'./adjusted_images'")
@click.option("--factor", default=2.2, type=float,
              help="亮度调整系数(0.0-2.0)，1.0表示不调整")
def adjust_brightness(src, dst, factor):
    """
    调整文件夹中所有图片的亮度，并保存为brightness_{factor}_{原文件名}
    """
    # 确保输出目录存在
    os.makedirs(dst, exist_ok=True)
    
    # 支持的图片格式
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    # 遍历源文件夹
    for filename in os.listdir(src):
        if filename.lower().endswith(valid_extensions):
            try:
                # 构建完整路径
                src_path = os.path.join(src, filename)
                dst_path = os.path.join(dst, f"brightness_{factor:.1f}_{filename}")
                
                # 打开图片并调整亮度
                with Image.open(src_path) as img:
                    # 转换为RGB/RGBA数组
                    arr = np.array(img)
                    
                    # 调整亮度并限制在0-255范围
                    adjusted = np.clip(arr * factor, 0, 255).astype(np.uint8)
                    
                    # 转换回图片对象
                    result = Image.fromarray(adjusted)
                    
                    # 保存处理后的图片
                    result.save(dst_path)
                    print(f"处理完成: {filename} -> brightness_{factor:.1f}_{filename}")
                    
            except Exception as e:
                print(f"处理图片 {filename} 时出错: {e}")

if __name__ == "__main__":
    adjust_brightness()