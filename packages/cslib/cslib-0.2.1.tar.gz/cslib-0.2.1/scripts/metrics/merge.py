import click

from cslib.utils import get_device
from cslib.utils.config import Options
from cslib.metrics.fusion.utils import Database

'''
update content in database2 to database1
'''

default_db_dir1 = "/Volumes/Charles/data/vision/torchvision/llvip/fused"
default_db_name1 = "metrics_all.db"
default_db_dir2 = "/Volumes/Charles/data/vision/torchvision/llvip/fused"
default_db_name2 = "metrics_asm.db"

@click.command()
@click.option('--suffix', default="jpg")
@click.option('--db_dir1', default=default_db_dir1, help='Path to save database file.')
@click.option('--db_name1', default=default_db_name1, help='Name of database file.')
@click.option('--db_dir2', default=default_db_dir2, help='Path to save database file.')
@click.option('--db_name2', default=default_db_name2, help='Name of database file.')
@click.option('--device', default='auto', help='auto | cuda | mps | cpu')
# @click.option('--jump', default=True, help='Jump Metrics that calculated before.')
def main(**kwargs):
    kwargs['device'] = get_device(kwargs['device'])
    opts = Options('Compute Metrics',kwargs)
    db = Database(
        db_dir = opts.db_dir1, 
        db_name = opts.db_name1,
    )
    db_addition = Database(
        db_dir = opts.db_dir2, 
        db_name = opts.db_name2,
    )
    db.merge(db_addition)

if __name__ == '__main__':
    main()
