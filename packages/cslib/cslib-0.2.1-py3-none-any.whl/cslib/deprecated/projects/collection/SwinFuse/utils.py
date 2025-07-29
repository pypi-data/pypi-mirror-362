import torch
import torch.nn as nn

from ....utils import path_to_gray

def get_test_images(image):
    base_size = 224
    _,_,h,w = image.shape
    image = image[0,0,:,:]
    if 1 * base_size < h < 2 * base_size and 1 * base_size < w < 2 * base_size:
        c = 4
        images = get_img_parts1(image, h, w)
    elif 2 * base_size < h < 3 * base_size and 2 * base_size< w < 3 * base_size:
        c = 9
        images = get_img_parts2(image, h, w)
    elif 2 * base_size < h < 3 * base_size and 3 * base_size < w < 4 * base_size:
        c = 12
        images = get_img_parts3(image, h, w)
    elif 1 * base_size < h < 2 * base_size and 2 * base_size < w < 3 * base_size:
        c = 6
        images = get_img_parts4(image, h, w)
    elif 3 * base_size < h < 4 * base_size and 4 * base_size < w < 5 * base_size:
        c = 20
        images = get_img_parts5(image, h, w)
    elif 0 * base_size < h < 1 * base_size and 1 * base_size < w < 2 * base_size:
        c = 2
        images = get_img_parts6(image, h, w)
    elif 0 * base_size < h < 1 * base_size and 2 * base_size < w < 3 * base_size:
        c = 3
        images = get_img_parts7(image, h, w)
    elif h == 1 * base_size and 2 * base_size < w < 3 * base_size:
        c = 3
        images = get_img_parts8(image, h, w)
    else:
        raise ValueError(f"Fail to locate image size: h={h}, w={w}")

    return images, h, w, c


def get_img_parts1(image, h, w):
    pad = nn.ConstantPad2d(padding=(0, 448-w, 0, 448-h), value=0)
    image = pad(image)
    images = []
    img1 = image[0:224, 0: 224]
    img1 = torch.reshape(img1, [1, 1, img1.shape[0], img1.shape[1]])
    img2 = image[0:224, 224: 448]
    img2 = torch.reshape(img2, [1, 1, img2.shape[0], img2.shape[1]])
    img3 = image[224:448, 0: 224]
    img3 = torch.reshape(img3, [1, 1, img3.shape[0], img3.shape[1]])
    img4 = image[224:448, 224: 448]
    img4 = torch.reshape(img4, [1, 1, img4.shape[0], img4.shape[1]])
    images.append(img1.float())
    images.append(img2.float())
    images.append(img3.float())
    images.append(img4.float())
    return images


def get_img_parts2(image, h, w):
    pad = nn.ConstantPad2d(padding=(0, 672-w, 0, 672-h), value=0)
    image = pad(image)
    images = []
    img1 = image[0:224, 0: 224]
    img1 = torch.reshape(img1, [1, 1, img1.shape[0], img1.shape[1]])
    img2 = image[0:224, 224: 448]
    img2 = torch.reshape(img2, [1, 1, img2.shape[0], img2.shape[1]])
    img3 = image[0:224, 448: 672]
    img3 = torch.reshape(img3, [1, 1, img3.shape[0], img3.shape[1]])
    img4 = image[224:448, 0: 224]
    img4 = torch.reshape(img4, [1, 1, img4.shape[0], img4.shape[1]])
    img5 = image[224:448, 224: 448]
    img5 = torch.reshape(img5, [1, 1, img5.shape[0], img5.shape[1]])
    img6 = image[224:448, 448: 672]
    img6 = torch.reshape(img6, [1, 1, img6.shape[0], img6.shape[1]])
    img7 = image[448:672, 0: 224]
    img7 = torch.reshape(img7, [1, 1, img7.shape[0], img7.shape[1]])
    img8 = image[448:672, 224: 448]
    img8 = torch.reshape(img8, [1, 1, img8.shape[0], img8.shape[1]])
    img9 = image[448:672, 448: 672]
    img9 = torch.reshape(img9, [1, 1, img9.shape[0], img9.shape[1]])
    images.append(img1.float())
    images.append(img2.float())
    images.append(img3.float())
    images.append(img4.float())
    images.append(img5.float())
    images.append(img6.float())
    images.append(img7.float())
    images.append(img8.float())
    images.append(img9.float())
    return images


def get_img_parts3(image, h, w):
    pad = nn.ConstantPad2d(padding=(0, 896-w, 0, 672-h), value=0)
    image = pad(image)
    images = []
    img1 = image[0:224, 0: 224]
    img1 = torch.reshape(img1, [1, 1, img1.shape[0], img1.shape[1]])
    img2 = image[0:224, 224: 448]
    img2 = torch.reshape(img2, [1, 1, img2.shape[0], img2.shape[1]])
    img3 = image[0:224, 448: 672]
    img3 = torch.reshape(img3, [1, 1, img3.shape[0], img3.shape[1]])
    img4 = image[0:224, 672: 896]
    img4 = torch.reshape(img4, [1, 1, img4.shape[0], img4.shape[1]])
    img5 = image[224:448, 0: 224]
    img5 = torch.reshape(img5, [1, 1, img5.shape[0], img5.shape[1]])
    img6 = image[224:448, 224: 448]
    img6 = torch.reshape(img6, [1, 1, img6.shape[0], img6.shape[1]])
    img7 = image[224:448, 448: 672]
    img7 = torch.reshape(img7, [1, 1, img7.shape[0], img7.shape[1]])
    img8 = image[224:448, 672: 896]
    img8 = torch.reshape(img8, [1, 1, img8.shape[0], img8.shape[1]])
    img9 = image[448:672, 0: 224]
    img9 = torch.reshape(img9, [1, 1, img9.shape[0], img9.shape[1]])
    img10 = image[448:672, 224: 448]
    img10 = torch.reshape(img10, [1, 1, img10.shape[0], img10.shape[1]])
    img11 = image[448:672, 448: 672]
    img11 = torch.reshape(img11, [1, 1, img11.shape[0], img11.shape[1]])
    img12 = image[448:672, 672: 896]
    img12 = torch.reshape(img12, [1, 1, img12.shape[0], img12.shape[1]])
    images.append(img1.float())
    images.append(img2.float())
    images.append(img3.float())
    images.append(img4.float())
    images.append(img5.float())
    images.append(img6.float())
    images.append(img7.float())
    images.append(img8.float())
    images.append(img9.float())
    images.append(img10.float())
    images.append(img11.float())
    images.append(img12.float())
    return images


def get_img_parts4(image, h, w):
    pad = nn.ConstantPad2d(padding=(0, 672-w, 0, 448-h), value=0)
    image = pad(image)
    images = []
    img1 = image[0:224, 0: 224]
    img1 = torch.reshape(img1, [1, 1, img1.shape[0], img1.shape[1]])
    img2 = image[0:224, 224: 448]
    img2 = torch.reshape(img2, [1, 1, img2.shape[0], img2.shape[1]])
    img3 = image[0:224, 448: 672]
    img3 = torch.reshape(img3, [1, 1, img3.shape[0], img3.shape[1]])
    img4 = image[224:448, 0: 224]
    img4 = torch.reshape(img4, [1, 1, img4.shape[0], img4.shape[1]])
    img5 = image[224:448, 224: 448]
    img5 = torch.reshape(img5, [1, 1, img5.shape[0], img5.shape[1]])
    img6 = image[224:448, 448: 672]
    img6 = torch.reshape(img6, [1, 1, img6.shape[0], img6.shape[1]])
    images.append(img1.float())
    images.append(img2.float())
    images.append(img3.float())
    images.append(img4.float())
    images.append(img5.float())
    images.append(img6.float())
    return images


def get_img_parts5(image, h, w):
    pad = nn.ConstantPad2d(padding=(0, 1120-w, 0, 896-h), value=0)
    image = pad(image)
    images = []
    img1 = image[0:224, 0: 224]
    img1 = torch.reshape(img1, [1, 1, img1.shape[0], img1.shape[1]])
    img2 = image[0:224, 224: 448]
    img2 = torch.reshape(img2, [1, 1, img2.shape[0], img2.shape[1]])
    img3 = image[0:224, 448: 672]
    img3 = torch.reshape(img3, [1, 1, img3.shape[0], img3.shape[1]])
    img4 = image[0:224, 672: 896]
    img4 = torch.reshape(img4, [1, 1, img4.shape[0], img4.shape[1]])
    img5 = image[0:224, 896: 1120]
    img5 = torch.reshape(img5, [1, 1, img5.shape[0], img5.shape[1]])
    img6 = image[224:448, 0: 224]
    img6 = torch.reshape(img6, [1, 1, img6.shape[0], img6.shape[1]])
    img7 = image[224:448, 224: 448]
    img7 = torch.reshape(img7, [1, 1, img7.shape[0], img7.shape[1]])
    img8 = image[224:448, 448: 672]
    img8 = torch.reshape(img8, [1, 1, img8.shape[0], img8.shape[1]])
    img9 = image[224:448, 672: 896]
    img9 = torch.reshape(img9, [1, 1, img9.shape[0], img9.shape[1]])
    img10 = image[224:448, 896: 1120]
    img10 = torch.reshape(img10, [1, 1, img10.shape[0], img10.shape[1]])
    img11 = image[448:672, 0: 224]
    img11 = torch.reshape(img11, [1, 1, img11.shape[0], img11.shape[1]])
    img12 = image[448:672, 224: 448]
    img12 = torch.reshape(img12, [1, 1, img12.shape[0], img12.shape[1]])
    img13 = image[448:672, 448: 672]
    img13 = torch.reshape(img13, [1, 1, img13.shape[0], img13.shape[1]])
    img14 = image[448:672, 672: 896]
    img14 = torch.reshape(img14, [1, 1, img14.shape[0], img14.shape[1]])
    img15 = image[448:672, 896: 1120]
    img15 = torch.reshape(img15, [1, 1, img15.shape[0], img15.shape[1]])
    img16 = image[672:896, 0: 224]
    img16 = torch.reshape(img16, [1, 1, img16.shape[0], img16.shape[1]])
    img17 = image[672:896, 224: 448]
    img17 = torch.reshape(img17, [1, 1, img17.shape[0], img17.shape[1]])
    img18 = image[672:896, 448: 672]
    img18 = torch.reshape(img18, [1, 1, img18.shape[0], img18.shape[1]])
    img19 = image[672:896, 672: 896]
    img19 = torch.reshape(img19, [1, 1, img19.shape[0], img19.shape[1]])
    img20 = image[672:896, 896: 1120]
    img20 = torch.reshape(img20, [1, 1, img20.shape[0], img20.shape[1]])
    images.append(img1.float())
    images.append(img2.float())
    images.append(img3.float())
    images.append(img4.float())
    images.append(img5.float())
    images.append(img6.float())
    images.append(img7.float())
    images.append(img8.float())
    images.append(img9.float())
    images.append(img10.float())
    images.append(img11.float())
    images.append(img12.float())
    images.append(img13.float())
    images.append(img14.float())
    images.append(img15.float())
    images.append(img16.float())
    images.append(img17.float())
    images.append(img18.float())
    images.append(img19.float())
    images.append(img20.float())

    return images


def get_img_parts6(image, h, w):
    pad = nn.ConstantPad2d(padding=(0, 448-w, 0, 224-h), value=0)
    image = pad(image)
    images = []
    img1 = image[0:224, 0: 224]
    img1 = torch.reshape(img1, [1, 1, img1.shape[0], img1.shape[1]])
    img2 = image[0:224, 224: 448]
    img2 = torch.reshape(img2, [1, 1, img2.shape[0], img2.shape[1]])
    images.append(img1.float())
    images.append(img2.float())
    return images


def get_img_parts7(image, h, w):
    pad = nn.ConstantPad2d(padding=(0, 672-w, 0, 224-h), value=0)
    image = pad(image)
    images = []
    img1 = image[0:224, 0: 224]
    img1 = torch.reshape(img1, [1, 1, img1.shape[0], img1.shape[1]])
    img2 = image[0:224, 224: 448]
    img2 = torch.reshape(img2, [1, 1, img2.shape[0], img2.shape[1]])
    img3 = image[0:224, 448: 672]
    img3 = torch.reshape(img3, [1, 1, img3.shape[0], img3.shape[1]])
    images.append(img1.float())
    images.append(img2.float())
    images.append(img3.float())
    return images


def get_img_parts8(image, h, w):
    pad = nn.ConstantPad2d(padding=(0, 672-w, 0, 224), value=0)
    image = pad(image)
    images = []
    img1 = image[0:224, 0: 224]
    img1 = torch.reshape(img1, [1, 1, img1.shape[0], img1.shape[1]])
    img2 = image[0:224, 224: 448]
    img2 = torch.reshape(img2, [1, 1, img2.shape[0], img2.shape[1]])
    img3 = image[0:224, 448: 672]
    img3 = torch.reshape(img3, [1, 1, img3.shape[0], img3.shape[1]])
    images.append(img1.float())
    images.append(img2.float())
    images.append(img3.float())
    return images


def recons_fusion_images1(img_lists, h, w, device, display=False):
    img_f_list = []
    for i in range(len(img_lists[0])):

        img1 = img_lists[0][i]
        img2 = img_lists[1][i]
        img3 = img_lists[2][i]
        img4 = img_lists[3][i]

        img_f = torch.zeros(1, h, w).to(device)
        if display:
            print(img_f.size())

        img_f[:, 0:224, 0: 224] += img1
        img_f[:, 0:224, 224: w] += img2[:, 0:224, 0:w-224]
        img_f[:, 224:h, 0: 224] += img3[:, 0:h-224, 0:224]
        img_f[:, 224:h, 224: w] += img4[:, 0:h-224, 0:w-224]

        img_f_list.append(img_f)
    return img_f_list


def recons_fusion_images2(img_lists, h, w, device, display=False):
    img_f_list = []
    for i in range(len(img_lists[0])):

        img1 = img_lists[0][i]
        img2 = img_lists[1][i]
        img3 = img_lists[2][i]
        img4 = img_lists[3][i]
        img5 = img_lists[4][i]
        img6 = img_lists[5][i]
        img7 = img_lists[6][i]
        img8 = img_lists[7][i]
        img9 = img_lists[8][i]
        img_f = torch.zeros(1, h, w).to(device)
        if display:
            print(img_f.size())

        img_f[:, 0:224, 0: 224] += img1
        img_f[:, 0:224, 224: 448] += img2
        img_f[:, 0:224, 448: w] += img3[:, 0:224, 0:w-448]
        img_f[:, 224:448, 0: 224] += img4
        img_f[:, 224:448, 224: 448] += img5
        img_f[:, 224:448, 448: w] += img6[:, 0:224, 0:w-448]
        img_f[:, 448:h, 0: 224] += img7[:, 0:h-448, 0:224]
        img_f[:, 448:h, 224: 448] += img8[:, 0:h-448, 0:224]
        img_f[:, 448:h, 448: w] += img9[:, 0:h-448, 0:w - 448]
        img_f_list.append(img_f)
    return img_f_list


def recons_fusion_images3(img_lists, h, w, device, display=False):
    img_f_list = []
    for i in range(len(img_lists[0])):

        img1 = img_lists[0][i]
        img2 = img_lists[1][i]
        img3 = img_lists[2][i]
        img4 = img_lists[3][i]
        img5 = img_lists[4][i]
        img6 = img_lists[5][i]
        img7 = img_lists[6][i]
        img8 = img_lists[7][i]
        img9 = img_lists[8][i]
        img10 = img_lists[9][i]
        img11 = img_lists[10][i]
        img12 = img_lists[11][i]
        img_f = torch.zeros(1, h, w).to(device)
        if display:
            print(img_f.size())

        img_f[:, 0:224, 0: 224] += img1
        img_f[:, 0:224, 224: 448] += img2
        img_f[:, 0:224, 448: 672] += img3
        img_f[:, 0:224, 672: w] += img4[:, 0:224, 0:w-672]
        img_f[:, 224:448, 0: 224] += img5
        img_f[:, 224:448, 224: 448] += img6
        img_f[:, 224:448, 448: 672] += img7
        img_f[:, 224:448, 672: w] += img8[:, 0:224, 0:w-672]
        img_f[:, 448:h, 0: 224] += img9[:, 0:h-448, 0:224]
        img_f[:, 448:h, 224: 448] += img10[:, 0:h - 448, 0:224]
        img_f[:, 448:h, 448: 672] += img11[:, 0:h - 448, 0:224]
        img_f[:, 448:h, 672: w] += img12[:, 0:h - 448, 0:w-672]

        img_f_list.append(img_f)
    return img_f_list


def recons_fusion_images4(img_lists, h, w, device, display=False):
    img_f_list = []
    for i in range(len(img_lists[0])):

        img1 = img_lists[0][i]
        img2 = img_lists[1][i]
        img3 = img_lists[2][i]
        img4 = img_lists[3][i]
        img5 = img_lists[4][i]
        img6 = img_lists[5][i]

        img_f = torch.zeros(1, h, w).to(device)
        if display:
            print(img_f.size())

        img_f[:, 0:224, 0: 224] += img1
        img_f[:, 0:224, 224: 448] += img2
        img_f[:, 0:224, 448: w] += img3[:, 0:224, 0:w-448]
        img_f[:, 224:h, 0: 224] += img4[:, 0:h-224, 0:224]
        img_f[:, 224:h, 224: 448] += img5[:, 0:h - 224, 0:224]
        img_f[:, 224:h, 448: w] += img6[:, 0:h - 224, 0:w-448]

        img_f_list.append(img_f)
    return img_f_list


def recons_fusion_images5(img_lists, h, w, device, display=False):
    img_f_list = []
    for i in range(len(img_lists[0])):

        img1 = img_lists[0][i]
        img2 = img_lists[1][i]
        img3 = img_lists[2][i]
        img4 = img_lists[3][i]
        img5 = img_lists[4][i]
        img6 = img_lists[5][i]
        img7 = img_lists[6][i]
        img8 = img_lists[7][i]
        img9 = img_lists[8][i]
        img10 = img_lists[9][i]
        img11 = img_lists[10][i]
        img12 = img_lists[11][i]
        img13 = img_lists[12][i]
        img14 = img_lists[13][i]
        img15 = img_lists[14][i]
        img16 = img_lists[15][i]
        img17 = img_lists[16][i]
        img18 = img_lists[17][i]
        img19 = img_lists[18][i]
        img20 = img_lists[19][i]
        img_f = torch.zeros(1, h, w).to(device)
        if display:
            print(img_f.size())

        img_f[:, 0:224, 0: 224] += img1
        img_f[:, 0:224, 224: 448] += img2
        img_f[:, 0:224, 448: 672] += img3
        img_f[:, 0:224, 672: 896] += img4
        img_f[:, 0:224, 896: w] += img5[:, 0:224, 0:w-896]
        img_f[:, 224:448, 0: 224] += img6
        img_f[:, 224:448, 224: 448] += img7
        img_f[:, 224:448, 448: 672] += img8
        img_f[:, 224:448, 672: 896] += img9
        img_f[:, 224:448, 896: w] += img10[:, 0:224, 0:w-896]
        img_f[:, 448:672, 0: 224] += img11
        img_f[:, 448:672, 224: 448] += img12
        img_f[:, 448:672, 448: 672] += img13
        img_f[:, 448:672, 672: 896] += img14
        img_f[:, 448:672, 896: w] += img15[:, 0:224, 0:w - 896]
        img_f[:, 672:h, 0: 224] += img16[:, 0:h-672, 0:224]
        img_f[:, 672:h, 224: 448] += img17[:, 0:h-672, 0:224]
        img_f[:, 672:h, 448: 672] += img18[:, 0:h-672, 0:224]
        img_f[:, 672:h, 672: 896] += img19[:, 0:h-672, 0:224]
        img_f[:, 672:h, 896: w] += img20[:, 0:h-672, 0:w - 896]

        img_f_list.append(img_f)
    return img_f_list


def recons_fusion_images6(img_lists, h, w, device, display=False):
    img_f_list = []
    for i in range(len(img_lists[0])):

        img1 = img_lists[0][i]
        img2 = img_lists[1][i]

        img_f = torch.zeros(1, h, w).to(device)
        if display:
            print(img_f.size())

        img_f[:, 0:h, 0: 224] += img1[:, 0:h, 0:224]
        img_f[:, 0:h, 224: w] += img2[:, 0:h, 0:w-224]

        img_f_list.append(img_f)
    return img_f_list


def recons_fusion_images7(img_lists, h, w, device, display=False):
    img_f_list = []
    for i in range(len(img_lists[0])):

        img1 = img_lists[0][i]
        img2 = img_lists[1][i]
        img3 = img_lists[2][i]

        img_f = torch.zeros(1, h, w).to(device)
        if display:
            print(img_f.size())

        img_f[:, 0:h, 0: 224] += img1[:, 0:h, 0:224]
        img_f[:, 0:h, 224: 448] += img2[:, 0:h, 0:224]
        img_f[:, 0:h, 448: w] += img3[:, 0:h, 0:w - 448]

        img_f_list.append(img_f)
    return img_f_list


def recons_fusion_images8(img_lists, h, w, device, display=False):
    img_f_list = []
    for i in range(len(img_lists[0])):

        img1 = img_lists[0][i]
        img2 = img_lists[1][i]
        img3 = img_lists[2][i]

        img_f = torch.zeros(1, h, w).to(device)
        if display:
            print(img_f.size())

        img_f[:, 0:h, 0: 224] += img1[:, 0:h, 0:224]
        img_f[:, 0:h, 224: 448] += img2[:, 0:h, 0:224]
        img_f[:, 0:h, 448: w] += img3[:, 0:h, 0:w - 448]

        img_f_list.append(img_f)
    return img_f_list

