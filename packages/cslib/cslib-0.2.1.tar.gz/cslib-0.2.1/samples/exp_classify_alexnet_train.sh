#!/bin/bash

PYTHON_SCRIPT="scripts/general_train.py"

python $PYTHON_SCRIPT \
    --name "AlexNet" \
    --param *ResPath "@ModelBasePath/AlexNet/MNIST/" str\
    --param *ResBasePath "@ResPath/temp" str \
    --param lr 0.01 float \
    --param epochs 5 int \
    --param repeat 6 int \
    --param factor 0.5 float \
    --param seed 42 int \
    --param val 0.2 float \
    --param batch 128 int \
    --param num_classes 10 int # 因为是 MNIST