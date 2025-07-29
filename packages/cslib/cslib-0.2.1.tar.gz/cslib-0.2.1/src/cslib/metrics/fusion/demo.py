from pathlib import Path
from cslib.utils import to_tensor,path_to_gray

__all__ = [
    'ir', 'vis', 'fused', 'cddfuse', 'densefuse', 'adf'
]

def load_demo_image():
    path = Path(__file__).resolve().parent / 'resources'
    filenames = ['ir', 'vis', 'CDDFuse', 'CDDFuse', 'DenseFuse', 'ADF']
    return [to_tensor(path_to_gray(path / f'{f}.png')).unsqueeze(0) for f in filenames]

(ir, vis, fused, cddfuse, densefuse, adf) = load_demo_image()
