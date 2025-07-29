from pathlib import Path
from cslib.utils.image import *

''' Load Image

    1. The return type of the image is `np.ndarray`, 
       to be compatible with the `skimage.color`.
    2. Range in [0, 1], compatible with the `torch.Tensor`.
    3. Can read as gray or rgb.
    4. Shape is [width, height, channel]
'''
# load a rgb image
rgb_path = Path(Path(__file__).parent, "image/rgb.png")
rgb_as_rgb = path_to_rgb(rgb_path)
rgb_as_gray = path_to_gray(rgb_path)

# load a gray image
gray_path = Path(Path(__file__).parent, "image/gray.png")
gray_as_rgb = path_to_rgb(gray_path)
gray_as_gray = path_to_gray(gray_path)

# breakpoint()
# (Pdb) print(rgb_as_rgb[0][0][:],rgb_as_rgb[0][0][:]*255)
# [0.85490196 0.91764706 0.98039216] [218. 234. 250.]
# (Pdb) print(rgb_as_gray[0][0],rgb_as_gray[0][0]*255)
# 0.9088376470588235 231.7536
# (Pdb) print(gray_as_rgb[0][0][:],gray_as_rgb[0][0][:]*255)
# [0.90588235 0.90588235 0.90588235] [231. 231. 231.]
# (Pdb) print(gray_as_gray[0][0],gray_as_gray[0][0]*255)
# 0.9058823529411765 231.0


''' View Image | Change Types

    1. You can input many images as a list.
    2. You can input `torch.Tensor`, `Image.Image` or `np.ndaray`

    1. `torch.Tensor`: ranged in [0,1], shaped of [c,w,h]
    2. `np.ndarray`: ranged in [0,1], shaped of [w,h,c]
    3. `Image.Image`: ranged in [0, 255], shaped of [w,h,c]
    4. Use `to_tensor()`, `to_image()` and `to_numpy()` to convert
'''
# glance a image
# glance(rgb_as_rgb) # Just drop the image into `glance`
# glance(rgb_as_rgb,title="RGB as RGB",hide_axis=False) # More params

# glance multiple images
images = [rgb_as_rgb,rgb_as_gray,gray_as_rgb,gray_as_gray]
title = ['RGB -> RGB', 'RGB -> Gray','Gray -> RGB', 'Gray -> Gray']
# glance(images,shape=(2,2),title=title) # <- use matplotlib

# glance torch.Tensor, np.ndaray. PIL.Image
image_np = rgb_as_rgb
image_tensor_3 = to_tensor(image_np)
image_tensor_4 = image_tensor_3.unsqueeze(0)
image_pil = to_image(image_tensor_3)
image_np = to_numpy(image_pil)
images = [image_np,image_pil,image_tensor_3,image_tensor_4]
title = ['np.ndarray','Image.Image','torch.Tensor(3,w,h)', 'torch.Tensor(1,3,w,h)']
# glance(images,shape=(2,2),title=title)


''' Change Color Mode

    we use skimage to realise ycbcr and rgb convertion
'''
image_np_ycbcr = rgb_to_ycbcr(image_np)
image_np_rgb = ycbcr_to_rgb(image_np_ycbcr)
images = [image_np,rgb_as_rgb,abs(image_np-image_np_rgb)]
titles = ['Origin', 'Recovered', 'Loss']
glance(images,shape=(1,3),title=titles)


''' Save Image

    1. save as image
'''
# 1. save as image
save_array_to_img(image_np_rgb,filename = Path(Path(__file__).parent, "image/res.png"))
# 2. save as mat
save_array_to_mat(image_np_rgb,base_filename = Path(Path(__file__).parent, "image/res").__str__())

