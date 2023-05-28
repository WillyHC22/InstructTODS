import ast
import json
import pandas as pd

from config import CONFIG
from dst_utils import MWOZ_Dataset
from evaluate_utils import unpack_belief_states, compute_prf


def evaluate_dst(results_df, vocal=True, save_path=None):
    global_turns = 0    
    global_jga = 0
    results_single_domain = {"taxi":{"turns":0, "correct_turns_jga":0, "correct_slots":0, "total_slots":0, "slot_f1":0},
                            "restaurant":{"turns":0, "correct_turns_jga":0, "correct_slots":0, "total_slots":0, "slot_f1":0},
                            "hotel":{"turns":0, "correct_turns_jga":0, "correct_slots":0, "total_slots":0, "slot_f1":0},
                            "train":{"turns":0, "correct_turns_jga":0, "correct_slots":0, "total_slots":0, "slot_f1":0},
                            "attraction":{"turns":0, "correct_turns_jga":0, "correct_slots":0, "total_slots":0, "slot_f1":0},
                            "all":{"global_turns":0, "global_f1":0}}
    
    for idx, row in results_df.iterrows():
        unpacked_gold = unpack_belief_states(row["gold_bs"], "gold")
        unpacked_pred = unpack_belief_states(row["preds"], "pred")
        domains = row["domains"]
        if isinstance(domains, str):
            domains = ast.literal_eval(domains)

        if set(unpacked_gold)==set(unpacked_pred):
            global_jga += 1
            if len(domains) == 1:
                results_single_domain[domains[0]]["correct_turns_jga"] += 1

        gold_values = [gold.split("-")[1] for gold in unpacked_gold]
        pred_values = [pred.split("-")[1] for pred in unpacked_pred]
        F1, recall, precision = compute_prf(gold_values, pred_values)
        if len(domains) == 1:
            results_single_domain[domains[0]]["slot_f1"] += F1
            results_single_domain[domains[0]]["turns"] += 1
        # if len(domains) == 1:
        #     gold_values = [gold.split("-")[1] for gold in unpacked_gold]
        #     pred_values = [pred.split("-")[1] for pred in unpacked_pred]
        #     for gold_value in gold_values:
        #         if gold_value in pred_values:
        #             results_single_domain[domains[0]]["correct_slots"] += 1
        #         results_single_domain[domains[0]]["total_slots"] += 1
        #     results_single_domain[domains[0]]["turns"] += 1
        results_single_domain["all"]["global_f1"] += F1
        results_single_domain["all"]["global_turns"] += 1
        global_turns += 1

    total_single_domain_jga = 0
    total_single_domain_turns = 0
    for domain in results_single_domain:
        if domain == "all":
            continue
        domain_slot_f1 = results_single_domain[domain]["slot_f1"]
        domain_correct_slots = results_single_domain[domain]["correct_slots"]
        domain_total_slots = results_single_domain[domain]["total_slots"]
        domain_jga = results_single_domain[domain]["correct_turns_jga"]
        domain_turns = results_single_domain[domain]["turns"]
        total_single_domain_jga += domain_jga
        total_single_domain_turns += domain_turns
        results_single_domain[domain]["JGA"] = domain_jga/domain_turns
        # results_single_domain[domain]["SLOT-F1"] = domain_correct_slots/domain_total_slots
        results_single_domain[domain]["SLOT-F1"] = domain_slot_f1/domain_turns

        if vocal:
            print(f"""For {domain}, JGA: {results_single_domain[domain]["JGA"]} - SLOT-F1: {results_single_domain[domain]["SLOT-F1"]}""")
    jga_single_domain_average = total_single_domain_jga/total_single_domain_turns
    jga_average = global_jga/global_turns    
    slot_f1_average = results_single_domain["all"]["global_f1"] / results_single_domain["all"]["global_turns"]
    if vocal:
        print(f"""Average JGA in single domain samples only: {jga_single_domain_average}""")
        print(f"""Average JGA overall: {jga_average}""")
        print(f"""Average Slot F1 Overall: {slot_f1_average}""")

    results = results_single_domain
    results["JGA_single_domain_average"] = jga_single_domain_average
    results["JGA_average"] = jga_average

    if save_path:
        with open(save_path, "w") as f:
            json.dump(results, f, indent=4)

    return results



if __name__ == "__main__":

    #gpt4 single domain only
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_dialogHistoryLimit0_prompt3.csv"
    #gpt4 single domain only - all slot 
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"
    #gpt4 single domain only - all slot - slot description
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

    #gpt3.5 single domain only
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_dialogHistoryLimit0_prompt2.csv"
    #gpt3.5 multi domain only
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_dialogHistoryLimit0_prompt3_latestSave.csv"
    #gpt3.5 single domain only - with all slots (reported result)
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"
    #gpt3.5 sigle domain only - with all slots - with slot descriptions
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"
    #gpt3.5 multi domain - with all slots - dh3
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit2_prompt3.csv"
    #gpt3.5 multi domain - with all slots - dh5
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit4_prompt3.csv"
    #gpt3.5 multi domain - with all slots - dhall
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit20_prompt3_latestSave.csv"
    #gpt3.5 multi domain - with all slots - with slot desc
    results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_debugFalse_singleDomainOnlyFalse_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

    recorrect = False
    #gpt3.5 single domain only - with all slots - recorrect
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_recorrect_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"
    #gpt3.5 single domain only - with all slots - recorrect - prompt1
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"
    #gpt3.5 single domain only - with all slots - with slot description - recorrect (from no slot description originally) - prompt 2
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_recorrect_singleDomainOnlyTrue_withSlotDescriptionTrue_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

    #gpt3.5 multi domain - with all slots
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-3.5-turbo_0-end_singleDomainOnlyFalse_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

    #gpt4 single domain - with all slots - recorrect
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_recorrectSlotDescFalse_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"
    #gpt4 single domain - with all slots - with slot description - recorrect
    # results_df_path = "/home/willy/instructod/src/DST/results_single/gpt-4_0-end_recorrectSlotDescTrue_debugFalse_singleDomainOnlyTrue_withSlotDescriptionFalse_withSlotDifferentiationFalse_withAllSlotsTrue_dialogHistoryLimit0_prompt3.csv"

    save_path = "/home/willy/instructod/src/DST/processed_results/" + results_df_path.split("/")[-1][:-4] + "_results.json"
    
    #Get correct format of dataset here to fetch golds
    mwoz_path = "/home/willy/instructod/MultiWOZ_2.1/"
    dialog_history_limit = 0
    with_slot_description = False
    single_domain_only = False
    with_req_inf_differentiation = False
    with_all_slots = True
    mwoz = MWOZ_Dataset(config=CONFIG, 
                        mwoz_path=mwoz_path,
                        dialog_history_limit=dialog_history_limit,
                        with_slot_description=with_slot_description,
                        with_req_inf_differentiation=with_req_inf_differentiation,
                        single_domain_only=single_domain_only,
                        with_all_slots=with_all_slots)
    dataset = mwoz.dataset
    
    results_df = pd.read_csv(results_df_path)
    if recorrect:
        results_df = results_df.rename(columns={"preds":"preds_bs", "correct_preds":"preds"})
    results_df = results_df[["preds", "id"]]
    merged_results = pd.merge(dataset, results_df, on=["id"])
    
    evaluate_dst(results_df=merged_results,
                 vocal=True,
                 save_path=save_path)

