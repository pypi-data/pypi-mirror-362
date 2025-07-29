from PIL import Image
import os

def convert_images_to_png(folder_path):
    """
    将指定文件夹下的所有 .jpg 和 .bmp 文件转换为 .png 格式。
    :param folder_path: 文件夹路径。
    """
    # 遍历文件夹中的所有文件
    for filename in os.listdir(folder_path):
        # 获取文件的完整路径
        file_path = os.path.join(folder_path, filename)
        
        # 检查文件扩展名
        if filename.lower().endswith(('.tif','.jpg', '.bmp')):
            # 打开图像
            image = Image.open(file_path)
            
            # 构造新的文件名（替换扩展名为 .png）
            new_filename = os.path.splitext(filename)[0] + '.png'
            new_file_path = os.path.join(folder_path, new_filename)
            
            # 保存为 .png 格式
            image.save(new_file_path, 'PNG')
            print(f"Converted {filename} to {new_filename}")
            
            # 可选：删除原文件
            os.remove(file_path)

# 示例用法
if __name__ == "__main__":
    # 指定文件夹路径
    folder_path = "/Users/kimshan/Public/data/vision/torchvision/tno/tno/vis"  # 替换为你的文件夹路径
    
    # 转换文件
    convert_images_to_png(folder_path)