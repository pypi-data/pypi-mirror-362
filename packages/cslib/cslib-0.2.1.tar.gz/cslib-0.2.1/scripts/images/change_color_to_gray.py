import os
from PIL import Image
import click

@click.command()
@click.option("--src", default="/Volumes/Charles/data/vision/torchvision/tno/tno/fused/cpfusion_origin", type=click.Path(exists=True, file_okay=False, resolve_path=True), help="源图片文件夹路径，默认为当前目录下的 'src' 文件夹")
@click.option("--dst", default="/Volumes/Charles/data/vision/torchvision/tno/tno/fused/cpfusion", type=click.Path(file_okay=False, resolve_path=True), help="目标文件夹路径，默认为当前目录下的 'dst' 文件夹")
def convert_images_to_grayscale(src, dst):
    """
    将指定文件夹中的图片转换为黑白图片并保存到目标文件夹。
    """
    # 确保目标文件夹存在
    if not os.path.exists(dst):
        os.makedirs(dst)
        print(f"创建目标文件夹：{dst}")
    
    # 遍历源文件夹中的所有文件
    for filename in os.listdir(src):
        # 构建完整的文件路径
        src_path = os.path.join(src, filename)
        
        # 检查是否为图片文件（简单检查扩展名）
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
            try:
                # 打开图片
                with Image.open(src_path) as img:
                    # 转换为灰度图（使用L模式）
                    grayscale_img = img.convert('L')
                    
                    # 构建目标路径
                    dst_path = os.path.join(dst, filename)
                    
                    # 保存灰度图
                    grayscale_img.save(dst_path)
                    print(f"转换并保存图片：{filename}")
            except Exception as e:
                print(f"处理图片 {filename} 时出错：{e}")
        else:
            print(f"跳过非图片文件：{filename}")

if __name__ == "__main__":
    convert_images_to_grayscale()