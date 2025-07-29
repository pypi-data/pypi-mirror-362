import click

from cslib.utils.config import Options
from cslib.metrics.fusion.utils import Database

'''
split db into dbs by metrics
'''

# default_db_src_dir = "/Volumes/Charles/data/vision/torchvision/llvip/fused"
# default_db_src_name = "metrics.db"
# default_db_res_dir = "/Volumes/Charles/data/vision/torchvision/llvip/fused/assets/by_metrics"

default_db_src_dir = "/Volumes/Charles/data/vision/torchvision/tno/tno/fused"
default_db_src_name = "metrics.db"
default_db_res_dir = "/Volumes/Charles/data/vision/torchvision/tno/tno/fused/assets/by_metrics"

@click.command()
@click.option('--suffix', default="jpg")
@click.option('--db_dir', default=default_db_src_dir, help='Path to save database file.')
@click.option('--db_name', default=default_db_src_name, help='Name of database file.')
@click.option('--db_dir_res', default=default_db_res_dir, help='Path to save database file.')
def main(**kwargs):
    opts = Options('Compute Metrics',kwargs)
    Database(
        db_dir = opts.db_dir, 
        db_name = opts.db_name,
    ).split_by_metric(opts.db_dir_res)

if __name__ == '__main__':
    main()
