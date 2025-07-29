from cslib.utils.gui import *

class UI(BasicUI):
    def __init__(self):
        super().__init__(
            title_label_text = 'Image Classification Demo',
            background = 'white',
            foreground = 'black'
        )
        self.title("Clib Pro")
    
    def config(self,**kwargs):
        super().config(**kwargs)
        self.configer_config = {
            'width': self.config_width,
            'label_width': self.config_label_width,
            'btn_width': self.config_label_width,
            'height': self.config_height,
            'background': self.background,
            'foreground': self.foreground,
        }
        
    def define(self):
        super().define()
        self.model_box = ConfigBox(
            master=self.config_frame,
            text='Model',
            values=['LeNet','AlexNet'],
            **self.configer_config
        )
        self.pth_path_btn = ConfigPath(
            master=self.config_frame,
            mode='file',
            text='Pre-Trained',
            **self.configer_config
        )
        self.dataset_box = ConfigBox(
            master=self.config_frame,
            text='Dataset',
            values=['MNIST'],
            **self.configer_config
        )
        self.dataset_path_btn = ConfigPath(
            master=self.config_frame,
            mode='dir',
            text='Dataset Path',
            **self.configer_config
        )
        self.load_btn = tk.Button(
            master=self.config_frame,
            text='load',
            background=self.background,
            foreground=self.foreground,
            command=lambda:self.load()
        )
        self.infer_btn = tk.Button(
            master=self.config_frame,
            text='infer',
            background=self.background,
            foreground=self.foreground,
            command=lambda:self.inference()
        )
        self.pics = [PicBox(master=self.show_frame,**self.configer_config) for _ in range(4)]
    
    def inference(self):
        pass

    def load(self):
        pass

    def pack(self):
        super().pack()
        self.model_box.pack()
        self.pth_path_btn.pack()
        self.dataset_box.pack()
        self.dataset_path_btn.pack()
        for i in self.pics:
            i.pack(side='left')
        self.load_btn.pack()
        self.infer_btn.pack()
