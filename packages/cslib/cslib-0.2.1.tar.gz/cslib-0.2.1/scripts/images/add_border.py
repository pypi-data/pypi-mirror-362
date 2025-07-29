from PIL import Image

def add_transparent_border(
    input_path, 
    output_path, 
    left=0, 
    right=0, 
    top=0, 
    bottom=0
):
    """
    为透明背景的图片添加不同大小的透明边框（可分别设置左、右、上、下）
    
    参数:
        input_path (str): 输入图片路径
        output_path (str): 输出图片路径
        left (int): 左边框宽度（像素）
        right (int): 右边框宽度（像素）
        top (int): 上边框宽度（像素）
        bottom (int): 下边框宽度（像素）
    """
    try:
        # 打开原始图片
        original = Image.open(input_path)
        
        # 确保图片有alpha通道（透明度）
        if original.mode != 'RGBA':
            original = original.convert('RGBA')
        
        # 计算新图片尺寸
        width, height = original.size
        new_width = width + left + right
        new_height = height + top + bottom
        
        # 创建新图片（全透明）
        bordered = Image.new('RGBA', (new_width, new_height), (0, 0, 0, 0))
        
        # 将原始图片粘贴到正确位置（考虑左、上边框）
        bordered.paste(original, (left, top), original)
        
        # 保存结果
        bordered.save(output_path)
        print(f"成功添加透明边框，已保存到: {output_path}")
        
    except Exception as e:
        print(f"处理图片时出错: {e}")

# 使用示例
if __name__ == "__main__":
    input_image = "/Users/kimshan/Public/project/IIA/client/src/assets/images/logo-light.png"    # 替换为你的输入图片路径
    output_image = "/Users/kimshan/Public/project/IIA/client/src/assets/images/logo-light-border.png"  # 替换为你想要的输出路径
    
    # 分别设置左、右、上、下的边框宽度（像素）
    add_transparent_border(
        input_image, 
        output_image, 
        left=139,    # 左边框 50px
        right=139,   # 右边框 30px
        top=0,     # 上边框 20px
        bottom=0   # 下边框 40px
    )