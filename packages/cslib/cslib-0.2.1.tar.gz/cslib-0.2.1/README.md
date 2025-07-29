# CVPlayground

## 项目结构

- ./samples 存放 shell 脚本, 调用 ./scripts 里边的 python 文件
- ./scripts 里边存放调用 cslib 的 python 脚本
- ./src 里边是 cslib 库, 使用 pyproject 配置文件, 构建包的方案见下面
- ./src/cslib/data 主要是一些数据集的 Dataset
- ./src/cslib/metrics 存放不同领域算法的指标
- ./src/cslib/train 存放训练方法, 让具体模型文件夹的 train.py 可以更方便
- ./src/cslib/transfroms 用于扩展 pytorch 自己的 transfroms, 不推荐用
- ./src/cslib/utils 用于存放工具, 现在有每一个配置函数的基类和实验平台配置的类
- ./src/cslib/model 用于存放具体模型
- ./src/cslib/model/collections/some_model 这是具体的某一个模型

## 数据集结构

数据集文件夹结构(举例):

- DataSets
  - torchvision: pytorch 自己的数据集文件夹
    - MNIST
    - ...
  - Fusion: 融合数据集
    - TNO
      - fused
        - DenseFuse
        - ...
      - ir
      - vis
    - ...
  - SR: 超分辨率重建数据集
    - Set5
    - ...
  - Model: 这个不是数据集, 这个保存每个算法的训练好的模型以及预训练模型
    - AUIF
    - DeepFuse
    - LeNet (其中每个自己训练的模型现在可以保存 model.pth、config.json 和基于 tensorboard 的训练过程)

## 配置文件
(sh 文件 --> ./scripts/config.py --> ./model/.../config.py)

- 每一个算法都有自己的配置文件, 在`./src/cslib/model/collections/some_model/config.py`, 这里是默认的, 原论文中的参数
- 每一个算法都可以在`./samples`里边的 shell 脚本中再写入调用时候的参数, 这些参数会覆盖默认参数
- 在`./scripts/config.py`中定义所有模型公共的参数, 比如数据集存放的文件夹，另外一些通用脚本比如跑模型等等不能没给算法穿一遍参数的，也要在这里统一规定参数


## 项目构建

- （自用）git-ssh 配置  
  - 开发环境中生成 ssh 密钥：`ssh-keygen -t rsa -b 4096 -C "your_email@example.com"`。这里的 your_email@example.com 应该替换成您的 GitHub 注册邮箱。当系统提示您“Enter a file in which to save the key”（输入保存密钥的文件名）时，您可以按 Enter 键接受默认文件位置。然后，它会要求您输入一个密码（passphrase），这是可选的，但为了安全起见，建议设置一个。
  - 查看密钥：`cat ~/.ssh/id_rsa.pub`，然后复制密钥到 github 官网 - setting - ssh - 添加ssh 里边。
  - 使用 ssh 下载本仓库： `git clone git@github.com:CharlesShan-hub/CVPlayground.git`
- 构建虚拟环境
  - 安装miniconda：https://docs.anaconda.com/miniconda/
  - 创建虚拟环境：`conda create --name cslib python=3.11`
  - 初始化环境：`conda init`
  - 刷新终端：`source ~/.bashrc`，或者到你的bashrc的位置
  - 进入环境：`conda acticate cslib`
  - 添加 conda-forge：`conda config --add channels conda-forge`
  - conda-forge换源
    ```bash
    # .condarc
    channels:
      - conda-forge
      - defaults
    show_channel_urls: true
    custom_channels:
      conda-forge: https://mirrors.tuna.tsinghua.edu.cn/anaconda/cloud
    ```
- 构建包
  - CVPlayground 下边的 src 文件夹中存放包，构建的时候会自动搜索 src 下的内容  
  - 临时添加 cslib 库：`pip install -e /Users/kimshan/workplace/CVPlayground`
  - 查看 GPU 版本：`nvcc --version`，然后去 environment.yml 里边修改 pytorch 的 cuda 版本号
  - 安装 requriements：`conda install --yes --file requirements.txt`
- git 开发
  - **开发前一定要先：`git pull`!!**
  - 初始化：`git init`
  - 如果用 http 链连接才需要，否则可以跳过：`git config --global user.email "charles.shht@gmail.com"`
  - 如果用 http 链连接才需要，否则可以跳过：`git config --global user.name "CharlesShan-hub"`
  - 提交1/3（记录文件变化）：`git add .`
  - 提交2/3（所有变化提交到本地仓库）`git commit -m "My feature implementation"`
  - 提交3/3（本地仓库退到远程仓库）：`git push`
- 打包上传
  - 打包：`python -m build`
  - 上传：`python -m twine upload dist/*`
  - 打包 conda 包：`conda build .`

## CV领域梳理

1. Image Classification 图像分类

   > https://paperswithcode.com/area/computer-vision/image-classification

   1. Out of Distribution (OOD) Detection：**分布外（OOD）检测**是检测不属于分类器已被训练的分布的实例的任务。OOD数据通常被称为“看不见的”数据，因为模型在训练期间没有遇到它。
   2. Few-Shot Image Classification：**少镜头图像分类**是一项计算机视觉任务，涉及训练机器学习模型，仅使用每个类别的少数标记示例（通常< 6个示例）将图像分类到预定义的类别中。

   3. Fine-Grained Image Classification：**细粒度图像分类**是计算机视觉中的一项任务，其目标是将图像分类为更大类别中的子类别。例如，对不同种类的鸟或不同类型的花进行分类。
   4. Learning with noisy labels：使用**噪声标签**学习意味着当我们说“噪声标签”时，我们的意思是对手故意弄乱了标签，否则这些标签将来自“干净”的分布。此设置还可用于仅从正数据和未标记数据进行投射学习。

2. Object Detection 目标检测

   > https://paperswithcode.com/area/computer-vision/object-detection
   >
   > https://paperswithcode.com/area/computer-vision/2d-object-detection

   1. 3D Object Detection 3D目标检测：在3D环境中识别和定位物体
   2. Real-Time Object Detection 实时对象检测
   3. RGB Salient Object Detection RGB显著目标检测
   4. Few-Shot Object Detection 少镜头目标检测

3. Semantic Segmentation 语义分割

   > https://paperswithcode.com/area/computer-vision/semantic-segmentation
   >
   > https://paperswithcode.com/area/computer-vision/2d-semantic-segmentation

   	1. 3D Semantic Segmentation 三维语义分割：涉及将3D点云或3D网格划分为语义上有意义的部分或区域
   	1. Real-Time Semantic Segmentation 实时语义分割
   	1. Scene Segmentation 场景分割
   	1. Road Segmentation 道路分割
   	1. Crack Segmentation 裂缝分割

4. Image Generation 图像生成

   > https://paperswithcode.com/area/computer-vision/image-generation

   1. Image Inpainting 图像修复：**图像修复**是一个重建图像中丢失区域的任务。它是计算机视觉中的一个重要问题，也是许多成像和图形应用中的一个基本功能，例如对象去除，图像恢复，操纵，重定向，合成和基于图像的渲染。
   2. Image-to-Image Translation：**图像到图像翻译**是计算机视觉和机器学习中的一项任务，其目标是学习输入图像和输出图像之间的映射，以便输出图像可用于执行特定任务，例如样式传输，数据增强或图像恢复。
   3. Image Manipulation 图像操纵：图像处理是改变或变换现有图像以实现所需效果或修改其内容的过程。这可能涉及各种技术和工具，以根据特定要求增强、修改或创建图像。
   4. Image Harmonization 图像协调：图像协调的目的是修改合成区域相对于特定背景的颜色。

5. Data Augmentation 数据增强

   > 





