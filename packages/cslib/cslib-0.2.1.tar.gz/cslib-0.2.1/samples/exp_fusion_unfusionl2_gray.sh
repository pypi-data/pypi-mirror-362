#!/bin/bash

PYTHON_SCRIPT="scripts/fusion_run_demo.py"

python $PYTHON_SCRIPT \
    --dataset "FusionToy" \
    --root_dir_base "" \
    --root_dir_path "Toy" \
    --des_dir "" \
    --des_suffix ""\
    --algorithm_name "UNFusion" \
    --algorithm_config "UNFusion_l2_mean" \
    --pre_trained "" \
    #--img_id ""  # 注意：这里假设img_id是一个字符串或者一个以空格分隔的字符串序列
