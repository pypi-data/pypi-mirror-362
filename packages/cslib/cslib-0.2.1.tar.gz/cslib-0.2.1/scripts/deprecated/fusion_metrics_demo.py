from torch.utils.data import DataLoader
from pathlib import Path
import sqlite3
import click

import cslib.metrics.fusion as metrics
from cslib.datasets import fusion as fusion_data
from cslib.utils import get_device

'''
测试融合算法的指标
1. 选择指定的融合方案
2. 选择指定的融合指标
3. 选择指定的融合图片
4. 结果输出到数据库中
5. 可以避免重复计算，可以进行结果更新(二选一)
6. 注意需要提前组织好融合图片的存储结构
'''
@click.command()
@click.option('--dataset','-n',default='MetricsToy', help='Name of images dataset.')
@click.option('--root_dir','-r',default="Path to datset", help='Root directory containing the dataset.')
@click.option('--db_name','-n',default='metrics.db', help='Name of database file.')
@click.option('--algorithm','-a',default=(),multiple=True, help='Fusion algorithm.')
@click.option('--img_id','-i',default=(),multiple=True, help='Image IDs to compute metrics for.')
@click.option('--metric_group','-m',default='VIFB', help='Methods Group to compute metrics for.')
@click.option('--device','-d',default='auto', help='Device to compute metrics on.')
@click.option('--jump','-u',default=False, help='Jump Metrics that calculated before.')
def main(dataset, root_dir, db_name, metric_group, algorithm, img_id, device, jump):
    # Modify Params
    assert hasattr(fusion_data, dataset)
    [img_id, algorithm] = [None if len(item)==0 else item for item in [img_id, algorithm]]
    device = get_device(device)
    
    # Connect to Database
    conn = sqlite3.connect(Path(root_dir,'fused',db_name))
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS fusion_metrics (
        method TEXT,
        id TEXT,
        name TEXT,
        value REAL,
        PRIMARY KEY (method, id, name)
    );
    ''')

    # Load Dataset and Dataloader
    dataset = getattr(fusion_data,dataset)(root_dir=root_dir,method=algorithm,img_id=img_id)
    dataloader = DataLoader(dataset, batch_size=1, shuffle=False)

    # Load metrics
    group = {
        'ALL': ['ce','en','te','mi','nmi','q_ncie','psnr','cc','scc','scd','ssim','ms_ssim','q_s','q','q_w','q_e','q_c','q_y','mb','mae','mse','rmse','nmse','ergas','d','ag','mg','ei','pfe','sd','sf','q_abf','q_sf','eva','sam','asm','con','fmi','n_abf','pww','q_cv','q_cb','vif'], #'q_p'
        'VIFB': ['ce','en','mi','psnr','ssim','rmse','ag','ei','sf','q_abf','sd','q_cb','q_cv'],
        'MEFB': ['ce','en','fmi','nmi','psnr','q_ncie','te','ag','ei','q_abf','sd','sf','q_c','q_w','q_y','q_cb','q_cv','vif'], #'q_p'
        'ce': ['ce'],
        'en': ['en'],
        'te': ['te'],
        'mi': ['mi'],
        'nmi': ['nmi'],
        'q_ncie': ['q_ncie'],
        'psnr': ['psnr'],
        'cc': ['cc'],
        'scc': ['scc'],
        'scd': ['scd'],
        'ssim': ['ssim'],
        'ms_ssim': ['ms_ssim'],
        'q_s': ['q_s'],
        'q': ['q'],
        'q_w': ['q_w'],
        'q_e': ['q_e'],
        'q_c': ['q_c'],
        'q_y': ['q_y'],
        'mb': ['mb'],
        'mae': ['mae'],
        'mse': ['mse'],
        'rmse': ['rmse'],
        'nmse': ['nmse'],
        'ergas': ['ergas'],
        'd': ['d'],
        'ag': ['ag'],
        'mg': ['mg'],
        'ei': ['ei'],
        'pfe': ['pfe'],
        'sd': ['sd'],
        'sf': ['sf'],
        'q_abf': ['q_abf'],
        'q_sf': ['q_sf'],
        'eva': ['eva'],
        'sam': ['sam'],
        'asm': ['asm'],
        'con': ['con'],
        'fmi': ['fmi'],
        'n_abf': ['n_abf'],
        'pww': ['pww'],
        'q_cv': ['q_cv'],
        'q_cb': ['q_cb'],
        'vif': ['vif'],
        'q_p': ['q_p'],
    }
    assert metric_group in group
    
    # Calculate
    for batch in dataloader:
        for (k,v) in metrics.info_summary_dict.items():
            # Skip Unneeded Metrics
            if k not in group[metric_group]: continue

            # Check if the metric has already been calculated
            cursor.execute('''
            SELECT value FROM fusion_metrics WHERE method=? AND id=? AND name=?;
            ''', (batch['method'][0], batch['id'][0], k))
            result = cursor.fetchone()

            if result and jump:
                value = result[0]
                print(f"{k} - {batch['method'][0]} - {batch['id'][0]}: {value} (skipped)")
                continue  # Skip calculation if the metric already exists and jump is True

            # Calculate
            value = v['metric'](batch['ir'].to(device),batch['vis'].to(device),batch['fused'].to(device))
            print(f"{k} - {batch['method'][0]} - {batch['id'][0]}: {value}")
            
            # Insert or Update the database
            cursor.execute('''
            INSERT OR REPLACE INTO fusion_metrics (method, id, name, value)
            VALUES (?, ?, ?, ?);
            ''', (batch['method'][0], batch['id'][0], k, value.item()))

        conn.commit()
    conn.close()

if __name__ == '__main__':
    main()