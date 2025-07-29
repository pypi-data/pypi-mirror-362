import os
from PIL import Image

# 指定包含.jpg文件的文件夹路径
input_folder = '/Users/kimshan/Public/data/vision/torchvision/tno/tno/lwir'

# 指定转换后的文件夹路径
output_folder = '/Users/kimshan/Public/data/vision/torchvision/tno/tno/ir'

# 创建输出文件夹（如果它不存在）
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的所有文件
for filename in os.listdir(input_folder):
    # 检查文件是否以.jpg结尾
    if filename.lower().endswith('.jpg'):
        # 构建原始文件和目标文件的路径
        original_path = os.path.join(input_folder, filename)
        target_path = os.path.join(output_folder, filename.replace('.jpg', '.png'))

        # 打开图片并保存为.png格式
        img = Image.open(original_path)
        img.save(target_path, 'PNG')
        print(f'Converted {filename} to {target_path}')

print('Conversion completed.')
