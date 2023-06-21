####GPT3.5

##FULL DH

# full dh - domain slots - no description
# python inference.py \
#     --model_name_or_path "openai/gpt-3.5-turbo" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-3.5-turbo_dh-1_domainSlots_descriptionNo.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst -1 \
#     --with_slot_domain_diff False \
#     --with_all_slots False \
#     --with_slot_description False \

#full dh - all slots - no description
# python inference.py \
#     --model_name_or_path "openai/gpt-3.5-turbo" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-3.5-turbo_dh-1_allSlots_descriptionNo.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst -1 \
#     --with_slot_domain_diff False \
#     --with_all_slots True \
#     --with_slot_description False \

#full dh - domain slots - with description
# python inference.py \
#     --model_name_or_path "openai/gpt-3.5-turbo" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-3.5-turbo_dh-1_domainSlots_descriptionYes.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst -1 \
#     --with_slot_domain_diff False \
#     --with_all_slots False \
#     --with_slot_description True \


##DH 1

# DH 1 - domain slots - no description
    # python inference.py \
    #     --model_name_or_path "openai/gpt-3.5-turbo" \
    #     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
    #     --task "dst" \
    #     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-3.5-turbo_dh0_domainSlots_descriptionNo_updated.csv"\
    #     --start_idx 0 \
    #     --single_domain_only \
    #     --dialog_history_limit_dst 0 \
    #     --with_slot_domain_diff False \
    #     --with_all_slots False \
    #     --with_slot_description False \
    
#DH 1 - all slots - no description
# python inference.py \
#     --model_name_or_path "openai/gpt-3.5-turbo" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-3.5-turbo_dh0_allSlots_descriptionNo.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst -1 \
#     --with_slot_domain_diff False \
#     --with_all_slots True \
#     --with_slot_description False \
    
#DH 1 - domain slots - with description
# python inference.py \
#     --model_name_or_path "openai/gpt-3.5-turbo" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-3.5-turbo_dh0_domainSlots_descriptionYes.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst -1 \
#     --with_slot_domain_diff False \
#     --with_all_slots False \
#     --with_slot_description True \






####GPT4

##FULL DH

# full dh - domain slots - no description
# python inference.py \
#     --model_name_or_path "openai/gpt-4" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-4_dh-1_domainSlots_descriptionNo.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst -1 \
#     --with_slot_domain_diff False \
#     --with_all_slots False \
#     --with_slot_description False \

#full dh - all slots - no description
# python inference.py \
#     --model_name_or_path "openai/gpt-4" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-4_dh-1_allSlots_descriptionNo.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst -1 \
#     --with_slot_domain_diff False \
#     --with_all_slots True \
#     --with_slot_description False \

#full dh - domain slots - with description
# python inference.py \
#     --model_name_or_path "openai/gpt-4" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-4_dh-1_domainSlots_descriptionYes.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst -1 \
#     --with_slot_domain_diff False \
#     --with_all_slots False \
#     --with_slot_description True \


##DH 1

#DH 1 - domain slots - no description
python inference.py \
    --model_name_or_path "openai/gpt-4" \
    --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
    --task "dst" \
    --save_path "/home/willy/instructod/src/DST/correct_results/gpt-4_dh0_domainSlots_descriptionNo.csv"\
    --start_idx 0 \
    --single_domain_only \
    --dialog_history_limit_dst 0 \
    --with_slot_domain_diff False \
    --with_all_slots False \
    --with_slot_description False \
    
#DH 1 - all slots - no description
# python inference.py \
#     --model_name_or_path "openai/gpt-4" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-4_dh0_allSlots_descriptionNo.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst 0 \
#     --with_slot_domain_diff False \
#     --with_all_slots True \
#     --with_slot_description False \
    
#DH 1 - domain slots - with description
# python inference.py \
#     --model_name_or_path "openai/gpt-4" \
#     --mwoz_path "/home/willy/instructod/MultiWOZ_2.1" \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/correct_results/gpt-4_dh0_domainSlots_descriptionYes.csv"\
#     --start_idx 0 \
#     --single_domain_only \
#     --dialog_history_limit_dst 0 \
#     --with_slot_domain_diff False \
#     --with_all_slots False \
#     --with_slot_description True \
