CUDA_VISIBLE_DEVICES=6 python pptod_ic.py\
    --data_prefix ../../../../data/banking77/\
    --model_name t5-base\
    --format_mode bs\
    --pretrained_path ../../../ckpt/base/\
    --number_of_gpu 1\
    --batch_size_per_gpu 64\
    --save_path ../../../inference_result/base