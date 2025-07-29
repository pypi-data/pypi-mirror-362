import click
from pathlib import Path
from cslib.datasets.fusion import M3FD

default_dataset_root_path = "/Volumes/Charles/data/vision/torchvision"

@click.command()
@click.option("--dataset-path", default=Path(default_dataset_root_path), type=Path, required=True)
def main(dataset_path: Path):
    dataset = M3FD(
        dataset_path, 
        download=True, # <- default
    )
    print(len(dataset)) # 300

if __name__ == '__main__':
    main()