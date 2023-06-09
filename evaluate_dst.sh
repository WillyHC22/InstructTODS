#GPT-4

#Recorrect - w/o slot desc
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-4_0-end_recorrectSlotDescTrue_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_recorrectSlotDescTrue_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

#Recorrect - w/ slot desc
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-4_0-end_recorrectSlotDescFalse_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_recorrectSlotDescFalse_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

#w/ slot desc
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-4_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

#w/ all slots
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-4_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

#w/ domain slots
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-4_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_dialogHistoryLimit0_prompt3.csv"



#ChatGPT


#Recorrect - w/o slot desc
python evaluate.py \
    --task "dst" \
    --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_recorrect_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3_eval.json" \
    --load_path "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_recorrect_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

#Recorrect - w/ slot desc
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_recorrect_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_recorrect_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

#w/ slot desc
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

# w/ all slots
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

#w/ domain slots
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_dialogHistoryLimit0_prompt3.csv"




#ChatGPT

#DH1
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-4_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

#DH3
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit2_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit2_prompt3.csv"

#DH5
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit4_prompt3_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit4_prompt3.csv"

#DH20
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit20_prompt3_latestSave_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit20_prompt3_latestSave.csv"



#Test
# python evaluate.py \
#     --task "dst" \
#     --save_path "/home/willy/instructod/src/DST/final_results/gpt-3.5-turbo_0-end_recorrect_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt4_latestSave_eval.json" \
#     --load_path "/home/willy/instructod/src/DST/results_single_old/gpt-3.5-turbo_0-end_recorrect_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt4_latestSave.csv"