import cv2
import numpy as np

def apply_guided_filter(image_path, radius=5, eps=0.01):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图像，请检查文件路径。")
        return
    
    # 将图像转换为灰度图（如果需要）
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # 应用引导滤波
    filtered_image = cv2.ximgproc.guidedFilter(guide=gray_image, src=gray_image, radius=radius, eps=eps)
    
    # 显示原始图像和滤波后的图像
    cv2.imshow('Original Image', gray_image)
    cv2.imshow('Guided Filtered Image', filtered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    image_path = input("请输入图像的路径: ")
    apply_guided_filter(image_path)