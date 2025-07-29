#!/bin/bash

PYTHON_SCRIPT="scripts/fusion_metrics_demo.py"

python $PYTHON_SCRIPT \
    --dataset "MetricsToy" \
    --root_dir "/Volumes/Charles/data/vision/torchvision/tno/tno" \
    --db_name "metrics.db" \
    --algorithm "cpfusion" \
    --metric_group "ALL" \
    --device "cpu" \
    --jump True
    #--img_id ""  # 注意：这里假设img_id是一个字符串或者一个以空格分隔的字符串序列

#--root_dir "/root/autodl-tmp/torchvision/tno/tno" \