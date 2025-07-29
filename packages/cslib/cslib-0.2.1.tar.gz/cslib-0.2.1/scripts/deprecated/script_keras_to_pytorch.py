# from keras.models import Sequential
# from keras.layers import Conv2D
# from keras.optimizers import Adam

# def predict_model(input_shape):
#     model = Sequential()
#     model.add(Conv2D(filters=128, kernel_size=(9, 9), activation='relu', padding='valid', input_shape=input_shape))
#     model.add(Conv2D(filters=64, kernel_size=(3, 3), activation='relu', padding='same'))
#     model.add(Conv2D(filters=1, kernel_size=(5, 5), activation='linear', padding='valid'))
#     adam = Adam(learning_rate=0.0003)
#     model.compile(optimizer=adam, loss='mean_squared_error', metrics=['mean_squared_error'])
#     return model

# # 定义输入形状
# input_shape = (None, None, 1)  # 根据实际情况修改

# # 创建模型实例
# keras_model = predict_model(input_shape)

# # 加载权重
# keras_model.load_weights("/Users/kimshan/Downloads/3051crop_weight_200.h5")



# import math

# import torch
# from torch import nn

# def load_model(opts):
#     # # Initialize the super-resolution model
#     model = SRCNN().to(device=opts.device)
#     for layer in model.modules():
#         if hasattr(layer, 'weight'):
#             layer.weight = layer.weight.to(memory_format=torch.channels_last)
#         if hasattr(layer, 'bias'):
#             layer.bias = layer.bias.to(memory_format=torch.channels_last)
    
#     # Load the super-resolution model weights
#     checkpoint = torch.load(opts.pre_trained, map_location=lambda storage, loc: storage)
#     model.load_state_dict(checkpoint["state_dict"])
    
#     return model

# from clib.projects.sr.SRCNN.model import SRCNN

# # 创建PyTorch模型实例
# torch_model = SRCNN().to(torch.device('cpu'))

# # 获取Keras模型的权重
# keras_weights = keras_model.get_weights()

# # 将Keras权重转换为PyTorch格式并加载到PyTorch模型
# # 注意：以下代码假设Keras模型和PyTorch模型层的顺序和结构是一致的
# torch_model.features[0].weight.data = torch.tensor(keras_weights[0].transpose(3, 2, 0, 1))
# torch_model.features[0].bias.data = torch.tensor(keras_weights[1].reshape(-1))
# torch_model.map[0].weight.data = torch.tensor(keras_weights[2].transpose(3, 2, 0, 1))
# torch_model.map[0].bias.data = torch.tensor(keras_weights[3].reshape(-1))
# torch_model.reconstruction.weight.data = torch.tensor(keras_weights[4].transpose(3, 2, 0, 1))
# torch_model.reconstruction.bias.data = torch.tensor(keras_weights[5].reshape(-1))

# # 或者只保存模型权重
# torch.save(torch_model.state_dict(), '/Users/kimshan/Downloads/keras_to_torch_SRCNN.pth')

# new_model = SRCNN().to(torch.device('cpu'))
# torch_model.load_state_dict(torch.load('/Users/kimshan/Downloads/keras_to_torch_SRCNN.pth'))
# new_model.load_state_dict(torch.load('/Users/kimshan/Downloads/keras_to_torch_SRCNN.pth'))