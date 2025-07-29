#!/bin/bash

PYTHON_SCRIPT="scripts/general_inference.py"

python $PYTHON_SCRIPT \
    --name "LeNet" \
    --field "classical" \
    --param *ResPath "@ModelBasePath/LeNet/MNIST/" str \
    --param *pre_trained "@ResPath/temp/model.pth" str \
    --param batch_size 8 int \
    --param use_relu 0 bool \
    --param use_max_pool 0 bool \