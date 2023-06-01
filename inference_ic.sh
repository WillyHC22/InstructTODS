# CUDA_VISIBLE_DEVICES=1 python src/IC/baseline.py \
#                        --model "facebook/bart-large-mnli" \
#                        --save_file "bart-large-mnli.json" \
#                        --save_dir "/home/willy/instructod/src/IC/results/baselines/" \
#                        --do_inference

# python src/IC/baseline.py \
#     --model "facebook/bart-large-mnli" \
#     --eval_file "bart-large-mnli.json" \
#     --save_dir "/home/willy/instructod/src/IC/results/baselines/" \
#     --do_evaluation \
#     --as_topn 3

# python src/IC/main.py \
#     --model "gpt-3.5-turbo" \
#     --save_path "/home/willy/instructod/src/IC/results/full_banking77_top1_gpt3.5.json" \
#     --load_path "/home/willy/instructod/src/IC/results/full_banking77_top1_gpt3.5.json" \
#     --save_path_postprocess "/home/willy/instructod/src/IC/results/full_banking77_top1_gpt3.5_processed.json" \
#     --save_path_eval "/home/willy/instructod/src/IC/results/full_banking77_top1_gpt3.5_processed_eval.json" \
#     --eval_file "/home/willy/instructod/src/IC/results/full_banking77_top1_gpt3.5_processed.json" \
#     --do_inference \
#     --do_postprocessing \
#     --do_evaluation


python src/IC/main.py \
    --model "gpt-3.5-turbo" \
    --save_path "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4.json" \
    --load_path "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4.json" \
    --save_path_postprocess "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4_processed.json" \
    --save_path_eval "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4_processed_eval.json" \
    --eval_file "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4_processed.json" \
    --do_postprocessing \
    --do_evaluation