from cslib.metrics.fusion import ce,ce_metric,ir,vis,fused
import matplotlib.pyplot as plt
import torch

def visualize_image_entropy(size):
    # 生成完全覆盖所有像素的张量
    full_tensor = (torch.arange(256*(size**2/256)).view(1, 1, size, size) / (size**2/256)).to(torch.uint8)
    # 生成随机张量
    random_tensor = torch.randint(0, 256, size=(1, 1, size, size), dtype=torch.uint8)
    # 生成纯色张量
    white_tensor = torch.full((1, 1, size, size), 255, dtype=torch.uint8)
    grey_tensor = torch.full((1, 1, size, size), 127, dtype=torch.uint8)
    black_tensor = torch.full((1, 1, size, size), 0, dtype=torch.uint8)
    # 绘制图像
    tensor_colors = ['Uniform', 'Random', 'Grey', 'White', 'Black']
    tensor_list = [full_tensor, random_tensor, grey_tensor, white_tensor, black_tensor]
    entropy_list = [ce(full_tensor/255.0,i/255.0) for i in tensor_list]

    fig, axs = plt.subplots(1, len(tensor_list), figsize=(20, 4))

    for i, (tensor, entropy) in enumerate(zip(tensor_list, entropy_list)):
        axs[i].imshow(tensor.view(size, size).numpy(), cmap='gray', vmin=0, vmax=255)
        axs[i].set_title(f'{tensor_colors[i]}\nEntropy: {entropy:.2f}')

    plt.show()


rand = torch.randint(0, 255, size=fused.shape, dtype=torch.uint8)/255.0

size = 64
# 生成完全覆盖所有像素的张量
full_tensor = (torch.arange(256*(size**2/256)).view(1, 1, size, size) / (size**2/256)).to(torch.uint8)/255.0
# 生成随机张量
random_tensor = torch.randint(0, 256, size=(1, 1, size, size), dtype=torch.uint8)/255.0
# 生成纯色张量
white_tensor = torch.full((1, 1, size, size), 255, dtype=torch.uint8)/255.0
grey_tensor = torch.full((1, 1, size, size), 127, dtype=torch.uint8)/255.0
black_tensor = torch.full((1, 1, size, size), 0, dtype=torch.uint8)/255.0

print("'Distance' with x and ir")
print(f'CE(ir,ir):   {ce(ir,ir)}')
print(f'CE(ir,vis):  {ce(ir,vis)}')
print(f'CE(ir,fused):{ce(ir,fused)}')

# visualize_image_entropy(64)

print("\nIf fused is fused | ir | vis  | average | rand")
print(f'[Fused = fused]   CE(ir,fused)  + CE(vis,fused):  {ce(ir,fused)+ce(vis,fused)}')
print(f'[Fused = ir]      CE(ir,ir)     + CE(vis,ir):     {ce(ir,ir)+ce(vis,ir)}')
print(f'[Fused = vis]     CE(ir,vis)    + CE(vis,vis):    {ce(ir,vis)+ce(vis,vis)}')
print(f'[Fused = average] CE(ir,arverge)+ CE(vis,arverge):{ce(ir,(vis+ir)/2)+ce(vis,(vis+ir)/2)}')
print(f'[Fused = rand]    CE(ir,rand)   + CE(vis,rand):   {ce(ir,rand)+ce(vis,rand)}')

print("\n")
print(f"{ce(full_tensor,full_tensor)}")
print(f"{ce(full_tensor,white_tensor)}")
print(f"{ce(full_tensor,black_tensor)}")
print(f"{ce(random_tensor,white_tensor)}")
print(f"{ce(random_tensor,black_tensor)}")
print(f"{ce(full_tensor,random_tensor)}")
print(f"{ce(white_tensor,black_tensor)}")
print(f"CE metric: {ce_metric(ir,vis,fused)}")
