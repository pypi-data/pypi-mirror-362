import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from PIL import ImageTk

class BasicUI(tk.Tk):
    def __init__(self,**kwargs):
        ''' Set data part into the app
        '''
        super().__init__()
        self.config(**kwargs)
        self.define()
        self.pack()

    def config(self,**kwargs):
        # Default Config
        self.title_label_text = "Undefined"
        self.background = "white"
        self.foreground = "black"
        self.width = 80
        self.height = 360
        self.title_height = 3
        self.title_label_font = ("Helvetica", 24)
        self.config_width = 20
        self.config_label_width = 8
        self.config_height = 1
        self.scale_factor = 6

        # Change Config
        for (k,v) in kwargs.items():
            setattr(self, k, v)

    def define(self):
        self.title_label = tk.Label(
            master=self,
            height=self.title_height,
            text=self.title_label_text,
            background=self.background,
            foreground=self.foreground
        )
        self.title_label.config(font=self.title_label_font)
        self.content_frame = tk.Frame(
            master=self,
            height=self.height - self.title_height,
            width=self.width,
            background=self.background
        )
        self.config_frame = tk.Frame(
            master=self.content_frame,
            width=self.config_width,
            background=self.background
        )
        self.show_frame = tk.Frame(
            master=self.content_frame,
            width=self.width - self.config_width,
            background=self.background
        )
    
    def pack(self):
        self.title_label.pack(fill='x',side='top')
        self.content_frame.pack(fill='both',expand=True,side='top')
        self.config_frame.pack(fill='y',side='left')
        self.show_frame.pack(fill='both',expand=True,side='left')
        

class ConfigBox(tk.Frame):
    def __init__(self,**kwargs):
        super().__init__(master=kwargs['master'])
        self.config(**kwargs)
        self.define()
        self.pack()
    
    def config(self,**kwargs):
        # Default Config
        self.label_width = 5
        self.width = 15
        self.height = 1
        self.text = 'Undefined'
        self.values = ['ex1','ex2','ex3']
        self.background = 'black'
        self.foreground = 'white'
        # Change Config
        for (k,v) in kwargs.items():
            setattr(self, k, v)
        self.label_width += 3 # Adjust to ConfigPath
        self.width += 2 # Adjust to ConfigPath

    def define(self):
        self.label = tk.Label(
            master = self,
            width = self.label_width,
            height = self.height,
            text = self.text,
            background=self.background,
            foreground=self.foreground
        )
        self.box = ttk.Combobox(
            master = self, 
            width = self.width - self.label_width,
            height = self.height,
            values = self.values,
            background=self.background,
            foreground=self.foreground
        )

    def pack(self,**kwargs):
        super().pack(**kwargs)
        self.label.pack(side='left')
        self.box.pack(side='left')
    
    def value(self):
        return self.values[self.box.current()]
    

class ConfigPath(tk.Frame):
    def __init__(self,**kwargs):
        super().__init__(master=kwargs['master'])
        self.config(**kwargs)
        self.define()
        self.pack()
    
    def config(self,**kwargs):
        # Default Config
        self.mode = 'Undefined'
        self.btn_width = 5
        self.width = 15
        self.height = 1
        self.text = 'Undefined'
        self.background = 'black'
        self.foreground = 'white'
        # Change Config
        for (k,v) in kwargs.items():
            setattr(self, k, v)

    def define(self):
        self.button = tk.Button(
            master = self,
            width = self.btn_width,
            height = self.height,
            text = self.text,
            background=self.background,
            foreground=self.foreground,
            command=lambda:self.open()
        )
        self.entry = tk.Entry(
            master = self, 
            width = self.width - self.btn_width,
            background=self.background,
            foreground=self.foreground
        )
        
    def pack(self,**kwargs):
        super().pack(**kwargs)
        self.button.pack(side='left')
        self.entry.pack(side='left')
    
    def value(self):
        return self.entry.get()
    
    def open(self):
        if self.mode == 'file':
            file_path = filedialog.askopenfilename()
        elif self.mode == 'dir':
            file_path = filedialog.askdirectory()
        else:
            raise ValueError('`mode` should be `dir` or `file`')
        
        self.entry.insert(0,file_path)


class PicBox(tk.Frame):
    def __init__(self,**kwargs):
        super().__init__(master=kwargs['master'])
        self.config(**kwargs)
        self.define()
        self.pack()
    
    def config(self,**kwargs):
        # Default Config
        self.mode = 'Undefined'
        self.label_height = 1
        self.width = 20
        self.height = 20
        self.size = 100
        self.text = 'Undefined'
        self.background = 'black'
        self.foreground = 'white'
        # Change Config
        for (k,v) in kwargs.items():
            setattr(self, k, v)

    def define(self):
        self.pic = tk.Label(
            master = self,
            # width = self.width,
            # height = self.height,
            background=self.background,
            foreground=self.foreground
        )
        self.label1 = tk.Label(
            master = self, 
            height=self.label_height,
            # width = self.width,
            background=self.background,
            foreground=self.foreground
        )
        self.label2 = tk.Label(
            master = self, 
            height=self.label_height,
            # width = self.width,
            background=self.background,
            foreground=self.foreground
        )
        
    def pack(self,**kwargs):
        super().pack(**kwargs)
        self.pic.pack(side='top')
        self.label1.pack(side='top')
        self.label2.pack(side='top')
    
    def resize(self, img):
        original_width, original_height = img.size
        max_dimension = max(original_width, original_height)
        scale_factor = self.size / max_dimension
        new_width = int(original_width * scale_factor)
        new_height = int(original_height * scale_factor)
        resized_img = img.resize((new_width, new_height))
        return ImageTk.PhotoImage(resized_img)
    
    def set(self, img, text1, text2):
        self.pic.config(image=img)
        self.label1.config(text=text1)
        self.label2.config(text=text2)
