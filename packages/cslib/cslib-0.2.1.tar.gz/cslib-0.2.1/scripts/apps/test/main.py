from ui import UI

from cslib.utils import to_image
from cslib.projects import classify 

import sys
from pathlib import Path
sys.path.append(Path(__file__,'../../../scripts').resolve().__str__())
import config # 这里用不了了

import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader

class App(UI):
    def __init__(self):
        super().__init__()

    def load(self):
        model_name = self.model_box.value()
        pth_path = self.pth_path_btn.value()
        dataset_name = self.dataset_box.value()
        dataset_path = self.dataset_path_btn.value()

        # model_name = 'LeNet'
        # pth_path = r'/Users/kimshan/resources/DataSets/Model/LeNet/MNIST/9430/model.pth'
        # dataset_name = 'MNIST'
        # dataset_path = r'/Users/kimshan/resources/DataSets/torchvision'

        config.opts[model_name] = {
            'pre_trained': pth_path
        }
        opts = config.opts[model_name]
        self.alg = getattr(classify,model_name)
        self.opts = self.alg.TestOptions().parse(opts,present=False)
        self.model = self.alg.load_model(self.opts)

        transform = transforms.Compose([
            transforms.Resize((28, 28)),
            transforms.ToTensor(),
            transforms.Normalize((0.5,), (0.5,))
        ])

        dataset = getattr(datasets,dataset_name)(root=dataset_path, train=False, download=True, transform=transform)
        self.dataLoader = DataLoader(dataset=dataset, batch_size=4, shuffle=False)
        self.dataLoader_iter = iter(self.dataLoader)

        self.opts.presentParameters()
        self.model.eval()

    def inference(self):
        def _get_image(tensor):
            img = to_image(tensor)
            return self.pics[0].resize(img)

        with torch.no_grad():
            images,labels = next(self.dataLoader_iter)
            self.images = [_get_image(i) for i in images]
            _, predict = torch.max(self.model(images).data, 1)
            for pic,i,l,p in zip(self.pics,self.images,labels,predict):
                pic.set(i,f'Label: {l}',f'Predict: {p}')

if __name__ == "__main__":
    app = App()
    app.mainloop()
