import re
import ast
import nltk
import string
import pandas as pd
from tqdm import tqdm
from word2number import w2n
from nltk.translate.bleu_score import sentence_bleu


def compute_BLEU(df_results, n=4):
    translator = str.maketrans("", "", string.punctuation)
    bleu_scores = []
    bleu_scores_single = []
    dialogue_ids = df_results['dialogue_id'].tolist()
    golds = df_results['gold_response'].tolist()
    preds = df_results['preds'].tolist()
    for i in tqdm(range(len(df_results))):
        dialogue_id = dialogue_ids[i]
        gold = golds[i].replace("SYSTEM: ", "").replace("\n", "").lower().translate(translator)
        try:
            pred = preds[i].lower().translate(translator)
        except:
            print(pred)
        if n == 4:
            bleu_score = sentence_bleu([nltk.word_tokenize(gold)], nltk.word_tokenize(pred), weights=(0, 0, 0, 1))
        else:
            bleu_score = sentence_bleu([nltk.word_tokenize(gold)], nltk.word_tokenize(pred), weights=(0.25, 0.25, 0.25, 0.25))
        bleu_scores.append(bleu_score)
        if "MUL" not in dialogue_id:
            bleu_scores_single.append(bleu_score)
    
    bleu = sum(bleu_scores) / len(bleu_scores)
    bleu_single = sum(bleu_scores_single) / len(bleu_scores_single)
    return bleu_single, bleu


def add_delexicalize_response(df_results):
    delex_preds = []

    for idx, row in df_results.iterrows():  
        if isinstance(row["gold_act"], str):
            gold_act = ast.literal_eval(row["gold_act"])
        else:
            gold_act = row["gold_act"]
        pred = row["preds"].lower()
        delex_pred = pred
        for k, v in gold_act.items():
            if "inform" in k.lower() or "recommend" in k.lower():
                for slot_values in v:
                    placeholder = "[" + slot_values[0].lower() + "_value]"
                    delex_pred = delex_pred.replace(slot_values[1].lower(), placeholder)
                    if slot_values[1].lower() != "two 2":
                        try:
                            converted_nb = w2n.word_to_num(slot_values[1].lower())
                            delex_pred = delex_pred.replace(str(converted_nb), placeholder)
                        except:
                            pass

            else:
                continue
        delex_preds.append(delex_pred)
        
    df_results["delexicalized_preds"] = delex_preds
    return df_results

def compute_match_succes(df_results):
    total_result = {}
    cur_request_slots = {}
    cur_inform_slots = {}
    prev_dialogue_id = df_results["dialogue_id"][0]
    for idx, row in df_results.iterrows():
        cur_dialogue_id = row["dialogue_id"]
        if cur_dialogue_id not in total_result:
            total_result[cur_dialogue_id] = {}

        if cur_dialogue_id != prev_dialogue_id:
            ##compute everything and reset variables, we are switching samples
            success = True
            for k, v in cur_request_slots.items():
                if cur_request_slots:
                    if v[1] == 0:
                        success = False
            if success:
                total_result[prev_dialogue_id]["success"] = 1
            else:
                total_result[prev_dialogue_id]["success"] = 0
            
            if cur_inform_slots:
                inform_score = 0
                for k, v in cur_inform_slots.items():
                    inform_score += v[1]/v[0]
                total_result[prev_dialogue_id]["inform"] = inform_score/len(cur_inform_slots)
            else:
                total_result[prev_dialogue_id]["inform"] = 1
                    
            cur_request_slots = {}
            cur_inform_slots = {}
        
        delex_pred = row["delexicalized_preds"]

        #success
        if isinstance(row["gold_turn_bs"], str):
            gold_turn_bs = ast.literal_eval(row["gold_turn_bs"])
        else:
            gold_turn_bs = row["gold_turn_bs"]
        for k, v in gold_turn_bs.items():
            if "request" in k.lower():
                for slot_values in v:
                    request_slot = slot_values[0].lower() + "_value"
                    if request_slot in cur_request_slots:
                        cur_request_slots[request_slot][0] += 1
                    else:
                        cur_request_slots[request_slot] = [1, 0]
        
        #match
        if isinstance(row["gold_act"], str):
            gold_act = ast.literal_eval(row["gold_act"])
        else:
            gold_act = row["gold_act"]
        for k, v in gold_act.items():
            if "inform" in k.lower():
                for slot_values in v:
                    inform_slot = slot_values[0].lower() + "_value"
                    if inform_slot in cur_inform_slots:
                        cur_inform_slots[inform_slot][0] += 1
                    else:
                        cur_inform_slots[inform_slot] = [1, 0]

                    if inform_slot in delex_pred:
                        cur_inform_slots[inform_slot][1] += 1

        
        for slot in cur_request_slots:
            if slot in delex_pred:
                cur_request_slots[slot][1] += 1

        prev_dialogue_id = cur_dialogue_id

    total_multi = 0
    total_single = 0
    correct_multi_success = 0
    correct_single_success = 0
    correct_multi_match = 0
    correct_single_match = 0
    results = {}
    L = len(total_result)
    for k, v in total_result.items():
        if not v:
            continue
        if "MUL" in k:
            total_multi += 1
            correct_multi_success += v["success"]
            correct_multi_match += v["inform"]
        else:
            total_single += 1
            correct_single_success += v["success"]
            correct_single_match += v["inform"]
    results["success_total"] = (correct_single_success+correct_multi_success) / L
    results["success_single"] = correct_single_success / total_single
    results["success_multi"] = correct_multi_success / total_multi
    results["match_total"] = (correct_single_match+correct_multi_match) / L
    results["match_single"] = correct_single_match / total_single
    results["match_multi"] = correct_multi_match / total_multi

    return results

def process_baseline(df_results, dataset):

    preds = []
    dial_ids = []
    turns = []

    for result in df_results:
        pred = result["resp_gen"]
        dial_id = result["dial_id"]
        turn = result["turn_num"]

        matches = re.findall(r'\[(.*?)\]', pred)
        for match in matches:
            reversed_match = match.split("_")[1] + "_" + match.split("_")[0]
            pred = pred.replace(match, reversed_match)

        turns.append(int(turn))
        preds.append(pred)
        dial_ids.append(dial_id.upper() + ".json")

    df = pd.DataFrame({"dialogue_id":dial_ids,
                        "turn":turns,
                        "delexicalized_preds":preds,
                        "preds":preds})

    merged_df = pd.merge(df, dataset, on=["dialogue_id", "turn"])
    return merged_df