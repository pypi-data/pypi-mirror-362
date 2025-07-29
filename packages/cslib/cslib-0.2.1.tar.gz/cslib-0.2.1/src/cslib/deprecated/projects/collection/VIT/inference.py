from .config import TestOptions

def inference(opts={}):
    opts = TestOptions().parse(opts)
