import os
import ast
import json
import copy
import string
import regex as re
import pandas as pd
from src.DST.dst import GENERAL_TYPO, SLOTS_REMAPPING, SLOTS_REVERSE_REMAPPING


# SLOTS_REMAPPING = {
#         # slots
#         "address":"addr",
#         "postcode":"post",
#         "leaveat":"leave",
#         "arriveby":"arrive",
#         "pricerange":"price",
#         "price":"fee",
#         "reference":"ref",
#         "departure":"depart",
#         "destination":"dest",
#         # values
#         "not mentioned": "null",
#         "unknown":"?", "inform":"?", "unk":"?", "needed":"?", "available":"?", "requested":"?", "request":"?", "n/a":"?",
# }

def fix_typos(pred):

    # pred = pred.replace("catherine 's", "catherine's")
    # pred = pred.replace("john 's", 'john"s')
    # pred = pred.replace("rosa 's", 'rosa"s')
    # pred = pred.replace("mary 's", 'mary"s')
    # pred = pred.replace("christ 's", "christ's")
    # pred = pred.replace("alpha - milton", "alpha-milton")
    # pred = pred.replace("michaelhouse cafe", "mic")
    # pred = pred.replace("the ", "")
    # pred = pred.replace(" nights", "")  
    # pred = pred.replace(" person", "")
    # pred = pred.replace(" night", "")   
    # pred = pred.replace(" days", "")    
    # pred = pred.replace("after ", "")  
    for k, v in SLOTS_REMAPPING.items():
        pred = pred.lower()
        pred = pred.replace(k, v)
        pred = pred.replace('"', "'")

    return pred


def remapping(t):
    t = t.lower()
    if t in SLOTS_REMAPPING:
        t = SLOTS_REMAPPING[t]
    return t


def nested_fix(d, fix):
    if not d or isinstance(d, bool):
        return ""
    elif isinstance(d, dict):  # if dict, apply to each key
        return {k.lower(): nested_fix(v, fix) for k, v in d.items()}
    elif isinstance(d, list):  # if list, apply to each element
        return [nested_fix(elem, fix) for elem in d]
    else:
        return fix(str(d))

def unpack_belief_states(belief_state, mode):

    # def nested_fix(d, fix):
    #     if not d or isinstance(d, bool):
    #         return ""
    #     elif isinstance(d, dict):  # if dict, apply to each key
    #         return {k: nested_fix(v, fix) for k, v in d.items()}
    #     elif isinstance(d, list):  # if list, apply to each element
    #         return [nested_fix(elem, fix) for elem in d]
    #     else:
    #         return fix(str(d))

    unpacked_belief_states = []
    if not belief_state: 
        return ["none-none"] 

    if mode == "gold":
        if isinstance(belief_state, str): #gold should be json by default, if misformatted into str for some reason this will take care of it
            rx = re.compile(r'"[^"]*"(*SKIP)(*FAIL)|\'')
            belief_state = json.loads(rx.sub('"', belief_state.lower()))
        if not belief_state:
            return ["none-none"]
        belief_state = nested_fix(belief_state, fix_typos)
        for domain_act in belief_state:
            slot_values = belief_state[domain_act]
            for slot_value in slot_values:
                slot, value = fix_typos(slot_value[0].lower()), fix_typos(slot_value[1].lower())
                unpacked_belief_states.append(f"{slot}-{value}")

    elif mode == "pred":
        if not isinstance(belief_state, dict):
            try:
                rx = re.compile(r'"[^"]*"(*SKIP)(*FAIL)|\'')
                belief_state = json.loads(rx.sub('"', belief_state.lower().replace("none", "null")))
            except:
                # print(f"No belief state: {fix_typos(belief_state.lower())}")
                return ["none-none"]
        else:
            if not belief_state:
                return ["none-none"]

        flag = False
        belief_state = nested_fix(belief_state, fix_typos)
        if not belief_state: 
            return ["none-none"] 
        for slot, value in belief_state.items():

            if isinstance(value, dict):
                #form like {"requested slots": {"leaveat":"07:15"}}
                flag = True
                unpacked_belief_states += unpack_belief_states(value, "pred")
            
            elif isinstance(value, list):
                #form like {"requested slots": [["leaveat", "07:15"], ["arriveby", "10:00"]]}
                flag = True
                unpacked_belief_states.append("none-none")

            elif not value:
                #empty prediction
                continue

            else:
                #form like {"leaveat":"07:15"}
                fixed_value = remapping(str(value).lower())
                if fixed_value == "null":
                    fixed_slot, fixed_value = "none", "none"
                else:
                    fixed_slot = remapping(slot.lower())

                slot_value = f"{fixed_slot}-{fixed_value}"
                if slot_value != "none-none":
                    flag = True
                unpacked_belief_states.append(slot_value)

        if flag:
            unpacked_belief_states = list(filter(lambda a: a != "none-none", unpacked_belief_states))
        if not unpacked_belief_states:
            unpacked_belief_states = ["none-none"]

    return unpacked_belief_states


def compute_prf(gold, pred):
    TP, FP, FN = 0, 0, 0
    if len(gold)!= 0:
        for g in gold:
            if g in pred:
                TP += 1
            else:
                FN += 1
        for p in pred:
            if p not in gold:
                FP += 1
        precision = TP / float(TP+FP) if (TP+FP)!=0 else 0
        recall = TP / float(TP+FN) if (TP+FN)!=0 else 0
        F1 = 2 * precision * recall / float(precision + recall) if (precision+recall)!=0 else 0
    else:
        if len(pred)==0:
            precision, recall, F1  = 1, 1, 1
        else:
            precision, recall, F1  = 0, 0, 0
    return F1, recall, precision


def add_running_accumulated_bs_column(df, mode = 'preds', new_column_suffix=''):

    running_bs_list = []
    new_turn_domains = []
    turn_domains = df['turn_domain']
    dialogue_ids = df['dialogue_id']
    column_name = 'preds' if mode == 'preds' else 'gold_turn_bs'
    if 'gold' in mode:
        mode = 'gold'
    items = df[column_name]
    for i, item in enumerate(items):
        
        # bug correction, take next turn domain when it's not available
        turn_domain = turn_domains[i] if turn_domains[i] != '' else turn_domains[i+1]

        if i == 0:
            running_bs = {}
            running_bs[turn_domain] = {}
        elif dialogue_ids[i] == dialogue_ids[i-1]:
            running_bs = copy.deepcopy(running_bs_list[i-1])
        else:
            running_bs = {}
            running_bs[turn_domain] = {}
            
        if mode == 'preds':
            unpacked_item = unpack_belief_states(item, 'pred')
            if unpacked_item != ['none-none']:
                try:
                    item_dict = ast.literal_eval(item) 
                except:
                    print("ERROR")
                    item_dict = {}
                if turn_domain not in list(running_bs.keys()):
                    running_bs[turn_domain] = {}
                for item_slot in item_dict.keys():
                    running_bs[turn_domain][item_slot] = item_dict[item_slot]
        elif mode == 'gold':
            unpacked_item = unpack_belief_states(item, 'gold')
            if unpacked_item != ['none-none']:
                item_dict = ast.literal_eval(item) if type(item) != type({}) else item
                item_dict = {items[0]:items[1] for items in list(item_dict.values())[0]}
                if turn_domain not in list(running_bs.keys()):
                    running_bs[turn_domain] = {}
                for item_slot in item_dict.keys():
                    running_bs[turn_domain][item_slot] = item_dict[item_slot]

        running_bs_list.append(running_bs)
        new_turn_domains.append(turn_domain)

    df[mode+'_bs'+new_column_suffix] = running_bs_list
    df['turn_domain'] = new_turn_domains

def drop_empty_keys(dictionary):
    if isinstance(dictionary, dict):
        return {key: drop_empty_keys(value) for key, value in dictionary.items() if value}
    else:
        return dictionary

def change_keys(dictionary, key_mapping):
    if isinstance(dictionary, dict):
        new_dict = {}
        for key, value in dictionary.items():
            if key == "type" or key == "car" or value == "?":
                continue           
            new_key = key_mapping(key)
            new_dict[new_key] = change_keys(value, key_mapping)
        return new_dict
    else:
        return dictionary


def full_fix(d):
    d = nested_fix(d, fix_typos)
    d = drop_empty_keys(d)
    d = change_keys(d, remapping)
    return d



#utils to merge dataframe results
def retrieve_golds(MWOZ_dataset, start_sample_idx, last_sample_idx, results_df):
    dataset = MWOZ_dataset.dataset
    df = results_df.copy(deep=True)
    if last_sample_idx != 1053:
        df["golds"] = list(dataset["golds"][start_sample_idx:last_sample_idx+1])
        df["prompts"] = list(dataset["prompts"][start_sample_idx:last_sample_idx+1])
        df["domains"] = list(dataset["domains"][start_sample_idx:last_sample_idx+1])
        df["dialogue_ids"] = list(dataset["ids"][start_sample_idx:last_sample_idx+1])
        df["model_used"] = ["gpt-4" for _ in range(last_sample_idx-start_sample_idx+1)]
    else:
        df["golds"] = list(dataset["golds"][start_sample_idx:])
        df["prompts"] = list(dataset["prompts"][start_sample_idx:])
        df["domains"] = list(dataset["domains"][start_sample_idx:])
        df["dialogue_ids"] = list(dataset["ids"][start_sample_idx:])
        df["model_used"] = ["gpt-4" for _ in range(last_sample_idx-start_sample_idx)]
    return df


def compute_dst_prf(df_result):
    L = len(df_result)
    bf_match = 0
    correct_slots = 0
    total_slots = 0
    total_F1 = 0
    results_per_domain = {"taxi":{"total_bf_match":0,
                                  "total_f1":0,
                                  "total_samples":0},
                          "attraction":{"total_bf_match":0,
                                        "total_f1":0,
                                        "total_samples":0},
                          "hotel":{"total_bf_match":0,
                                   "total_f1":0,
                                   "total_samples":0},
                          "restaurant":{"total_bf_match":0,
                                        "total_f1":0,
                                        "total_samples":0},
                          "train":{"total_bf_match":0,
                                   "total_f1":0,
                                   "total_samples":0},
                          "":{"total_bf_match":0,
                              "total_f1":0,
                              "total_samples":0}}
    for idx in range(L):
        turn_domain = df_result["turn_domain"][idx]

        pred_bs = df_result["preds_bs"][idx]
        gold_bs = df_result["gold_bs_new"][idx]
 
        corrected_pred_bs = full_fix(pred_bs)
        corrected_gold_bs = full_fix(gold_bs)

        # slot-f1
        # turn_correct = 0
        turn_TP = 0
        turn_FN = 0
        turn_FP = 0
        # turn_total = 0
        for k, v in corrected_gold_bs.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    # turn_total += 1
                    try:
                        #if correct in pred
                        if corrected_pred_bs[k][k1] == v1:
                            # turn_correct += 1
                            turn_TP += 1
                        else:
                            turn_FN += 1
                    except:
                        turn_FN += 1

        for k, v in corrected_pred_bs.items():
            if isinstance(v, dict):
                for k1, v1 in v.items():
                    # turn_total += 1
                    try:
                        #if correct in pred
                        if corrected_gold_bs[k][k1] != v1:
                            # turn_correct += 1
                            turn_FP += 1
                    except:
                        turn_FP += 1

        # total_slots += turn_total
        # correct_slots += turn_correct
        turn_precision = turn_TP / float(turn_TP+turn_FP) if (turn_TP+turn_FP)!=0 else 0
        turn_recall = turn_TP / float(turn_TP+turn_FN) if (turn_TP+turn_FN)!=0 else 0
        turn_F1 = 2 * turn_precision * turn_recall / float(turn_precision + turn_recall) if (turn_precision+turn_recall)!=0 else 0

        total_F1 += turn_F1

        results_per_domain[turn_domain]["total_f1"] += turn_F1
        results_per_domain[turn_domain]["total_samples"] += 1

        if corrected_pred_bs == corrected_gold_bs:
            bf_match += 1
            results_per_domain[turn_domain]["total_bf_match"] += 1
        else:
            if turn_domain == "nothing":
                print(gold_bs)
                print(pred_bs)
                print("gold", corrected_gold_bs)
                print("pred", corrected_pred_bs)
                print("---------")

    print(f"Total JGA: {(bf_match/L)*100:.2f}")
    print(f"Total F1: {(total_F1/L)*100:.2f}")
    print("----")

    for domain in ["attraction", "hotel", "restaurant", "taxi", "train"]:
        print(f"Domain: {domain}")
        domain_f1 = results_per_domain[domain]['total_f1']/results_per_domain[domain]['total_samples']
        domain_jga = results_per_domain[domain]['total_bf_match']/results_per_domain[domain]['total_samples']
        print(f"JGA: {domain_jga*100:.2f}")
        print(f"F1: {domain_f1*100:.2f}")     
        results_per_domain[domain]["F1"] = domain_f1
        results_per_domain[domain]["JGA"] = domain_jga
    
    results_per_domain["JGA"] = bf_match/L
    results_per_domain["F1"] = total_F1/L

    return results_per_domain



def merge_results(MWOZ_dataset, result_folder="src/DST/results/"):
    total_sample = 0
    merged_df = pd.DataFrame({})
    sorted_files = sorted(os.listdir(result_folder))
    for file in sorted_files:
        idxs = file.split("_")[1].split("-")
        start_idx, last_idx = int(idxs[0]), int(idxs[1])
        print(f"Processing samples between {start_idx} and {last_idx}")
        result_path = os.path.join(result_folder, file)
        results_df = pd.read_csv(result_path)
        total_sample += len(results_df)
        new_df = retrieve_golds(MWOZ_dataset, start_idx, last_idx, results_df)
        merged_df = merged_df.append(new_df, ignore_index=False)
    merged_df = merged_df.drop_duplicates(subset=["prompts", "dialogue_ids"], keep="first")
    return merged_df
