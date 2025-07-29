import os
from PIL import Image
import click

@click.command()
@click.option("--src", default="/Users/kimshan/Public/project/cvplayground/scenefuse/samples/glance_outputs", type=click.Path(file_okay=False),
              help="输出文件夹路径，默认为'./reversed_images'")
def reverse_images(src):
    """
    将指定文件夹中的所有图片反色处理，并保存为reverse_前缀的新文件
    """
    # 确保输出目录存在
    os.makedirs(src, exist_ok=True)
    
    # 支持的图片格式
    valid_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff')
    
    # 遍历源文件夹
    for filename in os.listdir(src):
        if filename.lower().endswith(valid_extensions):
            try:
                # 构建完整路径
                src_path = os.path.join(src, filename)
                dst_path = os.path.join(src, f"reverse_{filename}")
                
                # 打开图片并反色处理
                with Image.open(src_path) as img:
                    # 转换为RGB模式（如果是RGBA会丢失透明度）
                    if img.mode == 'RGBA':
                        r, g, b, a = img.split()
                        rgb = Image.merge('RGB', (r, g, b))
                        inverted = Image.eval(rgb, lambda x: 255 - x)
                        r, g, b = inverted.split()
                        inverted_img = Image.merge('RGBA', (r, g, b, a))
                    else:
                        inverted_img = Image.eval(img.convert('RGB'), lambda x: 255 - x)
                    
                    # 保存处理后的图片
                    inverted_img.save(dst_path)
                    print(f"处理完成: {filename} -> reverse_{filename}")
                    
            except Exception as e:
                print(f"处理图片 {filename} 时出错: {e}")

if __name__ == "__main__":
    reverse_images()