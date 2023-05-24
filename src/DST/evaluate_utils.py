import os
import json
import regex as re
import pandas as pd


SLOTS_REMAPPING = {
        # slots
        "address":"addr",
        "postcode":"post",
        "leaveat":"leave",
        "arriveby":"arrive",
        "pricerange":"price",
        "price":"fee",
        "reference":"ref",
        "departure":"depart",
        "destination":"dest",
        # values
        "not mentioned": "null",
        "unknown":"?", "inform":"?", "unk":"?", "needed":"?", "available":"?", "requested":"?", "request":"?", "n/a":"?",
}

def fix_typos(pred):

    pred = pred.replace("catherine 's", "catherine's")
    pred = pred.replace("john 's", 'john"s')
    pred = pred.replace("rosa 's", 'rosa"s')
    pred = pred.replace("mary 's", 'mary"s')
    pred = pred.replace("christ 's", "christ's")
    pred = pred.replace("alpha - milton", "alpha-milton")
    pred = pred.replace("michaelhouse cafe", "mic")
    pred = pred.replace("the ", "")
    pred = pred.replace(" nights", "")  
    pred = pred.replace(" person", "")
    pred = pred.replace(" night", "")   
    pred = pred.replace(" days", "")    
    pred = pred.replace("after ", "")  

    return pred


def remapping(pred):
    pred = pred.lower()
    if pred in SLOTS_REMAPPING:
        pred = SLOTS_REMAPPING[pred]
    return pred


def unpack_belief_states(belief_state, mode):

    def nested_fix(d, fix):
        if not d or isinstance(d, bool):
            return ""
        elif isinstance(d, dict):  # if dict, apply to each key
            return {k: nested_fix(v, fix) for k, v in d.items()}
        elif isinstance(d, list):  # if list, apply to each element
            return [nested_fix(elem, fix) for elem in d]
        else:
            return fix(str(d))

    unpacked_belief_states = []
    if not belief_state: 
        return ["none-none"] 

    if mode == "gold":
        if isinstance(belief_state, str): #gold should be json by default, if misformatted into str for some reason this will take care of it
            rx = re.compile(r'"[^"]*"(*SKIP)(*FAIL)|\'')
            belief_state = json.loads(rx.sub('"', belief_state.lower()))

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
                print(f"No belief state: {fix_typos(belief_state.lower())}")
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
