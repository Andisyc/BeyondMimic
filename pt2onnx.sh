#!/bin/bash

export CUDA_VISIBLE_DEVICES=3

unset DISPLAY

python scripts/rsl_rl/play.py \
    --headless \
    --video \
    --video_length 200 \
    --motion_file './motion/wave-single.npz' \
    --resume_path './rsl_rl/g1_flat/wave_single/model_16000.pt' \
    --livestream 0