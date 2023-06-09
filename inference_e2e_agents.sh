python inference.py \
    --model_name_or_path "openai/gpt-3.5-turbo" \
    --model_name_or_path_agent "openai/gpt-3.5-turbo" \
    --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
    --task "e2e_instructod" \
    --dialog_history_limit_e2e 4 \
    --single_domain_only \
    --save_path "/home/willy/instructod/src/e2e/results/gpt-3.5-turbo_e2e_agents_370-end_output.csv"\
    --verbose True \
    --agent_max_iterations 5 \
    --start_idx 370 \
    --do_inference     
    
