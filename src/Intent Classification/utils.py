import os
import json
import openai
from datasets import load_dataset
from collections import OrderedDict

def get_label_intent_dict(labels_str:str):
    intent_labels = labels_str.replace("\t", "")
    intent_labels = labels_str.split("\n")

    label2intent = {}
    intent2label = {}
    for intent in intent_labels:
        temp_split = intent.split()
        label = temp_split[0]
        intent = temp_split[1]
        label2intent[label] = intent
        intent2label[intent] = label
        
    return label2intent, intent2label

def get_labels(labels_path):
    with open(labels_path, "r") as f:
        LABELS = f.read()
    return LABELS


def get_intents(label2intent):
    INTENTS = ""
    for label in label2intent:
        INTENTS += label + " " + label2intent[label] + "\n"
    return INTENTS


def get_prompts(prompts_path, intents):
    PROMPT = {}
    with open(prompts_path, "r") as f:
        prompts = f.readlines()
        
    for idx, prompt in enumerate(prompts):
        PROMPT["top"+str(idx+1)] = prompt.replace("{INTENTS}", intents).replace("\\n", "\n")
        
    return PROMPT

def check_correct_format(intent2label, preds):
    for pred in preds:
        if pred not in intent2label:
            print(False)
            
            
def correcting_phrasing(pred, correction_path="config/corrections.txt"):
    with open(correction_path, "r") as f:
        lines = f.readlines()
    corrections = [correction.replace("\n", "").split(",") for correction in lines]
    for pairs in corrections:
        pred = pred.replace(pairs[0], pairs[1])
    return pred