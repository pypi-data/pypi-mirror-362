import click
import pandas as pd
from cslib.utils.config import Options
from cslib.metrics.fusion.utils import Database
import pandas as pd
import numpy as np

# Paths - llvip
default_db_dir = "/Volumes/Charles/data/vision/torchvision/llvip/fused"
default_db_name = "metrics.db"

# Paths - tno
# default_db_dir = "/Volumes/Charles/data/vision/torchvision/tno/tno/fused"
# default_db_name = "metrics.db"

# Fusion Images
# 1. Calculare all images in each fused_dir
defaulf_img_id = ()
# 2. Calculare for specified images
# defaulf_img_id = ('190001','190002','190003')
# defaulf_img_id = ('39',)

# Fusion Algorithms
# 1. `fused_dir` is into one algorithm
# default_algorithms = () 
# 2. `fused_dir` is the parent dir of all algorithms
default_algorithms = ('cpfusion','datfuse','fpde','fusiongan','gtf','ifevip','piafusion','stdfusion','tardal')
# default_algorithms = ('cpfusion',)

# Metrics
# default_metrics = [
#     'ce','en','te','mi','nmi','q_ncie','psnr','cc','scc','scd',
#     'ssim','ms_ssim','q_s','q','q_w','q_e','q_c','q_y','mb','mae',
#     'mse','rmse','nrmse','ergas','d','ag','mg','ei','pfe','sd','sf',
#     'q_abf','q_sf','eva','sam','asm','con','fmi','n_abf','pww',
#     'q_cv','vif' # q_cb
# ]
big_metrics = [
    'ag','ei','en','q_abf','q_cb','sf','vif'
]
small_metrics = [
    'q_cv',
]
default_metrics = big_metrics + small_metrics
# 1. All Metrics
# default_metrics = [
#     'ce','en','te','mi','nmi','q_ncie','psnr','cc','scc','scd',
#     'ssim','ms_ssim','q_s','q','q_w','q_e','q_c','q_y','mb','mae',
#     'mse','rmse','nrmse','ergas','d','ag','mg','ei','pfe','sd','sf',
#     'q_abf','q_sf','eva','sam','asm','con','fmi','n_abf','pww',
#     'q_cv','q_cb','vif'
# ]
# 2. VIFB
# default_metrics = [
#     'ce','en','mi','psnr','ssim','rmse','ag','ei','sf',
#     'q_abf','sd','q_cb','q_cv'
# ]
# 3. MEFB
# default_metrics = [
#     'ce','en','fmi','nmi','psnr','q_ncie','te','ag','ei',
#     'q_abf','sd','sf','q_c','q_w','q_y','q_cb','q_cv','vif'
# ]

def load_data(opts):
    database = Database(
        db_dir = opts.db_dir, 
        db_name = opts.db_name,
        metrics = opts.metrics,
        algorithms = opts.algorithms,
        mode = 'analyze' # analyze 就是检查 metrics 和 algorithms 已经存在
    )

    data = database.select_values(
        algorithm=opts.algorithms if opts.algorithms else None,
        metrics=opts.metrics if opts.metrics else None,
        img_id=None,  # 如果需要指定 img_id，可以在这里传入
        return_value=True,
        return_algorithm_id=True,
        return_metric_id=True,
        return_img_id=True,
        mode='name'
    )
    # for row in results:
    #     print(row)
    columns = np.array(['alg', 'metrics', 'img_id', 'value'])
    return pd.DataFrame(data, columns=columns)

def select_subgraphs(df, name, n):
    # 指标最大最小值信息
    #   metrics        min          max
    # 0      ag   0.528617    44.286331
    # 1      ei   5.397320   408.415039
    # 2      en   3.500764     7.937342
    # 3   q_abf   0.040066     0.699868
    metrics_min_max = df.groupby('metrics')['value'].agg(['min', 'max']).reset_index()

    # 添加指标的归一化值(1最好，0 最差)
    #            alg metrics img_id        value        min          max  normalized_value
    # 1408  cpfusion   q_abf     98     0.391185   0.040066     0.699868         0.532158
    # 1409  cpfusion   q_abf     99     0.404944   0.040066     0.699868         0.553011
    # 1410  cpfusion    q_cv      1  1071.362427  13.119925  6843.850098         0.845076
    # 1411  cpfusion    q_cv     10   107.746536  13.119925  6843.850098         0.986147
    df = df.merge(metrics_min_max, on='metrics', suffixes=('', '_agg'))
    df['normalized_value'] = (df['value'] - df['min']) / (df['max'] - df['min'])
    df.loc[df['metrics'].isin(small_metrics), 'normalized_value'] = 1 - df['normalized_value']

    # 按照分数优先量进行排名
    # alg img_id  cpfusion   datfuse      fpde  fusiongan       gtf    ifevip  piafusion  stdfusion    tardal     score
    # 145     23  4.454285  2.547948  3.864253   2.512349  3.543375  3.519881   4.607873   4.088864  3.371820  0.947239
    # 157     25  4.425548  3.035204  3.420054   2.682142  4.030317  3.861024   4.055783   3.517504  3.513206  0.911144
    # 178     45  4.288109  3.203009  3.144600   3.002779  3.492554  3.907723   3.980107   3.486220  2.988195  0.887460
    # 134     22  4.397359  3.461283  3.030236   2.602168  3.597397  3.799316   4.322128   4.076905  3.488439  0.850125
    image_scores = df.groupby(['img_id','alg'])['normalized_value'].sum().reset_index()
    image_scores.rename(columns={'normalized_value': 'score'}, inplace=True)
    image_scores = image_scores.pivot(index='img_id', columns='alg', values='score').reset_index()
    other_alg = [alg for alg in default_algorithms if alg != name]
    image_scores['score'] = image_scores[name] - image_scores[other_alg].mean(axis=1)
    image_scores = image_scores.sort_values(by='score', ascending=False)

    return image_scores.head(n)['img_id'].tolist()

@click.command()
@click.option('--n', default=200, help='Select specific images by metrics.')
@click.option('--optimize_alg', default='cpfusion')
@click.option('--metrics', default=default_metrics, multiple=True)
@click.option('--algorithms', default=default_algorithms, multiple=True, help='analyze metrics for multiple fusion algorithms')
@click.option('--db_dir', default=default_db_dir, help='Path to save database file.')
@click.option('--db_name', default=default_db_name, help='Name of database file.')
def main(**kwargs):
    opts = Options('Select Images',kwargs).parse({},present=True)
    df = load_data(opts)
    top_img_id = select_subgraphs(df, opts.optimize_alg, opts.n)
    print(top_img_id)
    

if __name__ == '__main__':
    main()