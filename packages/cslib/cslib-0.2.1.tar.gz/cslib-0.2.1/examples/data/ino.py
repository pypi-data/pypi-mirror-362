import click
from pathlib import Path
from cslib.datasets.fusion import INO

default_dataset_root_path = "/Volumes/Charles/data/vision/torchvision"

@click.command()
@click.option("--dataset-path", default=Path(default_dataset_root_path), type=Path, required=True)
def main(dataset_path: Path):
    dataset = INO(
        dataset_path, 
        download=True, # <- default
    )
    print(len(dataset)) # 1218

if __name__ == '__main__':
    main()