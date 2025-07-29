#!/bin/bash

PYTHON_SCRIPT="scripts/sr_run_demo.py"

python $PYTHON_SCRIPT \
    --dataset "SRBase" \
    --root_dir_base "" \
    --root_dir_path "Set5" \
    --upscale_factor "3"\
    --des_dir "" \
    --des_suffix ""\
    --algorithm_name "SRCNN" \
    --algorithm_config "SRCNN3" \
    --pre_trained "" \
    #--img_id "baby"  # 注意：这里假设img_id是一个字符串或者一个以空格分隔的字符串序列 # baby
