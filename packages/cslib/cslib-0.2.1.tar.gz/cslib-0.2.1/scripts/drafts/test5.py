from PIL import Image
from skimage import data
import matplotlib.pyplot as plt
import cv2
import numpy as np

def show(images, titles):
    num_images = len(images)
    fig, axes = plt.subplots(1, num_images, figsize=(15, 5))
    
    for ax, img, title in zip(axes, images, titles):
        ax.imshow(img, cmap='gray')
        ax.set_title(title)
        ax.axis('off')
    
    plt.tight_layout()
    plt.show()

def guided_filter_cv2(): 
    # 获取原始图像
    image = data.camera()
    
    # 应用 OpenCV 的引导滤波
    guided_filtered = cv2.ximgproc.guidedFilter(guide=image, src=image, radius=5, eps=0.01)
    
    # 使用 Canny 边缘检测显示边缘细节
    edges = cv2.Canny(guided_filtered.astype(np.uint8), 50, 150)

    images = [image, guided_filtered, edges] 
    titles = ['Original Image', 'Guided Filtered Image', 'Edge Details'] 
    show(images, titles) 

if __name__ == "__main__":
    guided_filter_cv2()