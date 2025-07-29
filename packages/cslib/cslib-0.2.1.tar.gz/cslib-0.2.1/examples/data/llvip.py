import click
from pathlib import Path
from cslib.datasets.fusion import LLVIP

default_dataset_root_path = "/Volumes/Charles/data/vision/torchvision"

@click.command()
@click.option("--dataset-path", default=Path(default_dataset_root_path), type=Path, required=True)
def main(dataset_path: Path):
    dataset = LLVIP(
        dataset_path, 
        download=True, # <- default
        train=False, # <- Test Set (default)
    )
    print(len(dataset)) # 3463

if __name__ == '__main__':
    main()