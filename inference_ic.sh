# Banking77

#BASELINES

# CUDA_VISIBLE_DEVICES=1 python src/IC/baseline.py \
#                        --model "facebook/bart-large-mnli" \
#                        --save_file "bart-large-mnli.json" \
#                        --save_dir "/home/willy/instructod/src/IC/results/baselines/" \
#                        --do_inference

# CUDA_VISIBLE_DEVICES=5 python src/IC/baseline.py \
#     --model "facebook/bart-large-mnli" \
#     --eval_file "bart-large-mnli-intent-correct.json" \
#     --save_dir "/home/willy/instructod/src/IC/results/baselines/" \
#     --save_file "bart-large-mnli-intent-correct.json" \
#     --do_evaluation \
#     --as_topn 1

#MAIN

# python src/IC/main.py \
#     --model "text-curie-001" \
#     --save_path "/home/willy/instructod/src/IC/results/full_banking77_top1_curie001.json" \
#     --load_path "/home/willy/instructod/src/IC/results/full_banking77_top1_curie001.json" \
#     --save_path_postprocess "/home/willy/instructod/src/IC/results/full_banking77_top1_curie001_processed.json" \
#     --save_path_eval "/home/willy/instructod/src/IC/results/full_banking77_top1_curie001_processed_eval.json" \
#     --eval_file "/home/willy/instructod/src/IC/results/full_banking77_top1_curie001_processed.json" \
#     --do_inference \
#     --do_postprocessing \
#     --do_evaluation

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


# python src/IC/main.py \
#     --model "gpt-3.5-turbo" \
#     --save_path "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4.json" \
#     --load_path "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4.json" \
#     --save_path_postprocess "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4_processed.json" \
#     --save_path_eval "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4_processed_eval.json" \
#     --eval_file "/home/willy/instructod/src/IC/results/full_banking77_top3_gpt4_processed.json" \
#     --do_postprocessing \
#     --do_evaluation





#CLINC150

#BASELINES

# CUDA_VISIBLE_DEVICES=5 python src/IC/baseline.py \
#                        --model "facebook/bart-large-mnli" \
#                        --dataset "clinc_oos" \
#                        --save_file "bart-large-mnli_clinc150.json" \
#                        --save_dir "/home/willy/instructod/src/IC/results/baselines" \
#                        --label_path "/home/willy/instructod/src/IC/config/intents_clinc.txt" \
#                        --eval_file "bart-large-mnli_clinc150.json" \
#                        --do_evaluation \
#                        --do_inference

# CUDA_VISIBLE_DEVICES=5 python src/IC/baseline.py \
#     --model "facebook/bart-large-mnli" \
#     --eval_file "bart-large-mnli-intent-correct.json" \
#     --save_dir "/home/willy/instructod/src/IC/results/baselines/" \
#     --save_file "bart-large-mnli-intent-correct.json" \
#     --do_evaluation \
#     --as_topn 1




#MAIN

#Top3 

# python src/IC/main.py \
#     --model "gpt-3.5-turbo" \
#     --save_path "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5.json" \
#     --load_path "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5.json" \
#     --save_path_postprocess "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5_processed.json" \
#     --save_path_eval "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5_processed_eval.json" \
#     --eval_file "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5_processed.json" \
#     --label_path "/home/willy/instructod/src/IC/config/intents_clinc.txt"\
#     --dataset "clinc_oos"\
#     --corrections_path "/home/willy/instructod/src/IC/config/corrections_clinc.txt" \
#     --do_postprocessing \
#     --do_evaluation \
#     --do_inference 

#Top1

python src/IC/main.py \
    --model "gpt-4" \
    --save_path "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5.json" \
    --load_path "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5.json" \
    --save_path_postprocess "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5_processed.json" \
    --save_path_eval "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5_processed_eval.json" \
    --eval_file "/home/willy/instructod/src/IC/results/clinc150/full_clinc150_top3_gpt3.5_processed.json" \
    --label_path "/home/willy/instructod/src/IC/config/intents_clinc.txt"\
    --dataset "clinc_oos"\
    --corrections_path "/home/willy/instructod/src/IC/config/corrections_clinc.txt" \
    --do_postprocessing \
    --do_evaluation \
    --topn "top3" \
    # --do_inference

