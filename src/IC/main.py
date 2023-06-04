import os
import json
import openai
import argparse
from tqdm import tqdm
from datasets import load_dataset
from collections import OrderedDict

from utils import get_label_intent_dict, get_labels, get_prompts, get_intents, correcting_phrasing

openai.api_key= os.environ["OPENAI_API_KEY"]


def do_inference(test_data, label2intent, model, ALL_PROMPTS, save_path=None, start_from=0, save_steps=100, topn="top3", debug_mode=False):
    preds = {}
    total_tokens = 0
    if debug_mode:
        L = 10
    else:
        L = len(test_data)
    
    for i in tqdm(range(start_from, L)):
        cur_preds = {}
        text_input = test_data[i]
        prompt = ALL_PROMPTS[topn] + '"' + text_input["text"] + '"'

        cur_preds["text"] = text_input["text"]
        cur_preds["gold_label"] = text_input["label"]
        cur_preds["gold_intent"] = label2intent[str(text_input["label"])]
        cur_preds["prompt"] = prompt

        def completion(model, prompt):
            if model in ["gpt-3.5-turbo", "gpt-4"]:
                completion = openai.ChatCompletion.create(
                    model=model, 
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0
                )
                return completion["choices"][0]["message"]["content"], completion["usage"]["total_tokens"]
            else:
                completion = openai.Completion.create(
                    model=model,
                    prompt=prompt,
                    temperature=0
                    )
                return completion["choices"][0]["text"], 0
        
        retry_count = 0
        while True:
            if retry_count > 5:
                print("Retried too many times")
                break
            try:
                cur_preds["pred"], tokens = completion(model, prompt)
                total_tokens += tokens
                break
            except:
                retry_count += 1
                continue
        if retry_count > 5:
            break

        preds[i] = cur_preds
        if save_path and i % save_steps == 0:
            with open(save_path, "w") as f:
                json.dump(preds, f, indent=4)
        
    if save_path:
        with open(save_path, "w") as f:
            json.dump(preds, f, indent=4)

    print(f"Used in total {total_tokens} for the inference with {model}")

    return preds


def do_postprocessing(load_path, save_path, correction_path, dataset, args_topn, model):
    with open(load_path, "r") as f:
        results = json.load(f)
        
    full_results = results.copy()
    count = 0
    for index, result in results.items():
        topn = 1
        temp_results = {}
        pred = result["pred"].lower()
        pred = correcting_phrasing(pred, correction_path)
        pred = pred.replace(",", " ")
        pred = pred.replace(".", " ")
        pred = pred.replace(":", " ")
        pred = pred.replace(")", " ")
        if "clinc" in dataset:
            if "3" in args_topn:
                # splitted_preds = [(idx+1, pred.split(" ")[1]) for idx, pred in enumerate(pred.split("\n"))]
                # for topn in splitted_preds:
                #     temp_results["top" + str(topn[0])] = topn[1]
                pred = pred.replace("\n", " ")
                pred = pred.split(" ")
                if pred[-1] == "":
                    pred = pred[:-1]
                full_intent = ""
                for word in pred:
                    # if word not in ["", "1", "2", "3"]:
                    if not word.isdigit() and word != "":
                        full_intent += word + "_"
                    else:
                        temp_results["top"+str(topn)] = full_intent[:-1]
                        if full_intent != "":
                            topn += 1
                        full_intent = ""
                temp_results["top"+str(topn)] = full_intent[:-1]
                temp_results = {k:v for k, v in temp_results.items() if k in ["top1", "top2", "top3"]}

                L = len(temp_results)
                if L < 3:
                    print(f"""Predictions at index {index}: "{" ".join(pred)}" formatting isn't handled correctly\n""")
                    count += 1
                    for topn in ["top1", "top2", "top3"]:
                        if topn not in temp_results:
                            temp_results[topn] = "none"

            else:
                pred = pred.replace("\n", " ")
                if "3.5" in model:
                    if ":" in pred:
                        temp_results["top1"] = pred.split(": ")[1]
                    else:
                        temp_results["top1"] = pred
                elif "4" in model:
                    parsed_pred = pred.split(" ")
                    if parsed_pred[0].isdigit():
                        temp_results["top1"] = parsed_pred[1]
                    else:
                        temp_results["top1"] = parsed_pred[0]

        else:    
            pred = pred.replace("\n", " ")
            pred = correcting_phrasing(pred, correction_path)
            if "_" in pred:
                pred = pred.split(" ")
                for word in pred:
                    if "_" in word or word == "none":
                        temp_results["top"+str(topn)] = word
                        topn += 1
                if len(temp_results) != 3:
                    count += 1

            else:
                pred = pred.split(" ")
                if pred[-1] == "":
                    pred = pred[:-1]
                full_intent = ""
                for word in pred:
                    if word not in ["", "1", "2", "3"]:
                        full_intent += word + "_"
                    else:
                        temp_results["top"+str(topn)] = full_intent[:-1]
                        if full_intent != "":
                            topn += 1
                        full_intent = ""
                temp_results["top"+str(topn)] = full_intent[:-1]
                temp_results = {k:v for k, v in temp_results.items() if k in ["top1", "top2", "top3"]}

                L = len(temp_results)
                if L < 3:
                    count += 1
                    for topn in ["top1", "top2", "top3"]:
                        if topn not in temp_results:
                            temp_results[topn] = "none"

        full_results[index]["processed_pred"] = temp_results
    
    
    with open(save_path, "w") as f:
        json.dump(full_results, f, indent=4)
    
    return full_results


def do_evaluation(load_path, save_path):
    with open(load_path, "r") as f:
        preds = json.load(f)

    L = len(preds)
        
    results = {"top1":0, "top2":0, "top3":0, "others":0}
    for index, sample in preds.items():
        gold = sample["gold_intent"]
        processed_preds = sample["processed_pred"]
        found_correct = False
        for topn, intent in processed_preds.items():
            if intent == gold:
                found_correct = True
                results[topn] += 1
        if not found_correct:
            results["others"] += 1

    results["top1_acc"] = results["top1"]/L
    results["top2_acc"] = results["top2"]/L
    results["top3_acc"] = results["top3"]/L
    
            
    with open(save_path, "w") as f:
        json.dump(results, f, indent=4)    
        
    return results
            
                
            

        
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo", help="model to use")
    parser.add_argument("--save_steps", type=int, default=3, help="save the inference results every n steps because openai API might have server issues")
    parser.add_argument("--start_from", type=int, default=0, help="first index to start the evaluation")
    parser.add_argument("--topn", type=str, default="top3", choices=["top1", "top2", "top3"], help="do the inference to get eitehr top1, top2 or top3 intent predicted")
    parser.add_argument("--do_inference", action="store_true", help="use this argument to do inference")
    parser.add_argument("--do_postprocessing", action="store_true", help="use this argument to postprocess the output after having done inference")
    parser.add_argument("--do_evaluation", action="store_true", help="use this argument to run evaluation on postprocessed outputs")
    parser.add_argument("--corrections_path", type=str, default="/home/willy/instructod/src/IC/config/corrections.txt", help="correction files for the postprocessing")
    parser.add_argument("--prompt_path", type=str, default="/home/willy/instructod/src/IC/config/prompts.txt", help="txt file with prompt format")
    parser.add_argument("--label_path", type=str, default="/home/willy/instructod/src/IC/config/intents.txt", help="txt file with the intent labels")
    parser.add_argument("--dataset", type=str, default="banking77", help="dataset for intent classification")
    parser.add_argument("--split", type=str, default="test", help="split of the dataset")
    parser.add_argument("--save_path", type=str, default="/home/willy/instructod/src/IC/results/full_banking77_top3.json", help="path to save inference result")
    parser.add_argument("--load_path", type=str, default="/home/willy/instructod/src/IC/results/full_banking77_top3.json", help="path to load inference result for the postprocessing")
    parser.add_argument("--save_path_postprocess", type=str, default="/home/willy/instructod/src/IC/results/full_banking77_top3_processed.json", help="path to save json after postprocessing for top 3 intents")
    parser.add_argument("--save_path_eval", type=str, default="/home/willy/instructod/src/IC/results/full_banking77_top3_processed_eval.json", help="path to save json after evaluation of postprocessed results")
    parser.add_argument("--eval_file", type=str, default="/home/willy/instructod/src/IC/results/full_banking77_top3_processed.json", help="file to run evaluation from postprocessing")
    parser.add_argument("--debug_mode", action="store_true", help="debug mode")
    args = parser.parse_args()
  
    
    if args.do_inference:
        if "clinc" in args.dataset:
            dataset = load_dataset(args.dataset, "small", split=args.split)
            dataset = dataset.rename_column('intent', 'label')
        else:
            dataset = load_dataset(args.dataset, split=args.split)
        LABELS = get_labels(args.label_path)
        label2intent, intent2label = get_label_intent_dict(LABELS)
        INTENTS = get_intents(label2intent)
        ALL_PROMPTS = get_prompts(args.prompt_path, INTENTS)    

        preds = do_inference(dataset, 
                             label2intent, 
                             model=args.model,
                             save_path=args.save_path, 
                             ALL_PROMPTS=ALL_PROMPTS, 
                             start_from=args.start_from, 
                             save_steps=args.save_steps, 
                             topn=args.topn,
                             debug_mode=args.debug_mode)
        
    if args.do_postprocessing:
        preds = do_postprocessing(load_path=args.load_path, 
                                  save_path=args.save_path_postprocess, 
                                  correction_path=args.corrections_path,
                                  dataset=args.dataset,
                                  args_topn=args.topn,
                                  model=args.model)
    
    if args.do_evaluation:
        results = do_evaluation(load_path=args.eval_file,
                                save_path=args.save_path_eval)