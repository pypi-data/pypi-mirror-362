import sqlite3
from pathlib import Path
from cslib.metrics.fusion.utils import Database

default_metrics = [
    'ce','en','te','mi','nmi','q_ncie','psnr','cc','scc','scd',
    'ssim','ms_ssim','q_s','q','q_w','q_e','q_c','q_y','mb','mae',
    'mse','rmse','nrmse','ergas','d','ag','mg','ei','pfe','sd','sf',
    'q_abf','q_sf','eva','sam','asm','con','fmi','n_abf','pww',
    'q_cv','q_cb','vif'
]
default_algorithms = ['cpfusion','datfuse','fpde','fusiongan','gtf','ifevip','piafusion','stdfusion','tardal']

class OldDatabase():
    def __init__(self, path):
        self.conn = sqlite3.connect(Path(path))
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS fusion_metrics (
            algorithm TEXT,
            metric TEXT,
            id TEXT,
            value REAL,
            FOREIGN KEY (algorithm) REFERENCES algorithms (id),
            FOREIGN KEY (metric) REFERENCES metrics (id),
            PRIMARY KEY (algorithm, metric, id)
        );
        ''')

def migrate_database(odb, ndb):
    for metric,m_id in ndb.all_metrics.items():
        for algorithm, a_id in ndb.all_algorithms.items():
            odb.cursor.execute(
                "SELECT id, value FROM fusion_metrics WHERE algorithm=? AND metric=?",
                (algorithm, metric)
            )
            values = odb.cursor.fetchall()
            if values is None:
                continue
            for row in values:
                ndb.cursor.execute(
                    "INSERT INTO fusion_metrics (algorithm_id, metric_id, image_id, value) VALUES (?, ?, ?, ?)",
                    (a_id, m_id, row[0], row[1])
                )
            ndb.conn.commit()
            

if __name__ == '__main__':
    old_db_path = Path('/Volumes/Charles/data/vision/torchvision/tno/tno/fused/metrics0.db')  # 替换为旧数据库的路径
    new_db_path = Path('/Volumes/Charles/data/vision/torchvision/tno/tno/fused/metrics.db')    # 替换为新数据库的路径

    ndb = Database(
        db_dir=new_db_path.parent,
        db_name=new_db_path.name,
        metrics=default_metrics,
        algorithms=default_algorithms
    )
    odb = OldDatabase(old_db_path)
    migrate_database(odb, ndb)