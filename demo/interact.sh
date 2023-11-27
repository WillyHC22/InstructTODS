#!/bin/bash

python main.py --config_path="/path/to/config,json" \
               --load_path="/path/to/db.json" \
               --log_path="/path/to/log/folder/" \
               --model_name_or_path="gpt-3.5-turbo-0301" \
               --dialog_history_limit_bs=2 \
               --dialog_history_limit_rg=7 \
               --agent_max_iterations=7