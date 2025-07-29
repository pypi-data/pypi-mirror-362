from PIL import Image, ImageFilter

def gaussian_blur(input_path, output_path, radius=5):
    try:
        # 打开图片
        image = Image.open(input_path)
        
        # 应用高斯模糊滤镜
        blurred_image = image.filter(ImageFilter.GaussianBlur(radius=radius))
        
        # 保存处理后的图片
        blurred_image.save(output_path)
        print(f"高斯模糊图片已保存至 {output_path}")
    except Exception as e:
        print(f"处理图片时出错: {e}")

if __name__ == "__main__":
    input_image_path = input("请输入输入图片的路径: ")
    output_image_path = input("请输入输出图片的路径: ")
    gaussian_blur(input_image_path, output_image_path)