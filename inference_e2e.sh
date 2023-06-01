python inference.py \
    --model_name_or_path "openai/gpt-3.5-turbo" \
    --task "e2e" \
    --save_path "/home/willy/instructod/src/e2e/results/gpt-3.5-turbo_e2e_5236_end_output.csv" \
    --dialog_history_limit_rg -1 \
    --db_format_type "2" \
    --start_idx 5236