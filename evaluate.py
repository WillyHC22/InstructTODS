import os
import sys
import json
import string
import logging
import pandas as pd

from tqdm import tqdm
from langchain import PromptTemplate

from tqdm import tqdm
from transformers import (
    HfArgumentParser,
)

from src.config import CONFIG
from src.data import MWOZ_Dataset
from src.DST.dst import SLOTS_DESCRIPTIONS
from src.DST.evaluate_utils import remapping
from src.utils.args_helper import DataArguments, ModelArguments, PromptingArguments
from src.RG.rg_utils import compute_BLEU, add_delexicalize_response, compute_match_succes, process_baseline



logger = logging.getLogger(__name__)


def main():
    # See all possible arguments in src/transformers/training_args.py
    # or by passing the --help flag to this script.
    # We now keep distinct sets of args, for a cleaner separation of concerns.

    parser = HfArgumentParser((ModelArguments, DataArguments, PromptingArguments))
    if len(sys.argv) == 2 and sys.argv[1].endswith(".json"):
        # If we pass only one argument to the script and it's the path to a json file,
        # let's parse it to get our arguments.
        model_args, data_args, prompting_args = parser.parse_json_file(json_file=os.path.abspath(sys.argv[1]))
    else:
        model_args, data_args, prompting_args = parser.parse_args_into_dataclasses()

    # Setup logging
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        datefmt="%m/%d/%Y %H:%M:%S",
        handlers=[logging.StreamHandler(sys.stdout)],
    )

    log_level = prompting_args.get_process_log_level()
    logger.setLevel(log_level)

    # mwoz = MWOZ_Dataset(CONFIG, data_args)
    # dataset = mwoz.dataset
    if "baseline" in data_args.load_path:
        df_results = json.load(open(data_args.load_path, "r"))
    else:
        df_results = pd.read_csv(data_args.load_path)
        df_results = df_results.dropna(subset=['preds'])
    if prompting_args.task == "rg":
        print("======= Evaluating response generation =======")
        print("Delexicalizing the response generation...")
        if "baseline" in data_args.load_path:
            mwoz = MWOZ_Dataset(CONFIG, data_args)
            dataset = mwoz.dataset
            df_results = process_baseline(df_results, dataset)
        else:
            df_results = add_delexicalize_response(df_results)
        print("Computing BLEU...")
        bleu_single, bleu = compute_BLEU(df_results, n=0)
        bleu_4_single, bleu_4 = compute_BLEU(df_results, n=4)
        print("Computing match entity rate and success...")
        total_results = compute_match_succes(df_results)
        total_results["BLEU_single"] = bleu_single
        total_results["BLEU-4_single"] = bleu_4_single
        total_results["BLEU"] = bleu
        total_results["BLEU-4"] = bleu_4

    print("Saving results...")
    if data_args.save_path:
        with open(data_args.save_path, "w") as f:
            json.dump(total_results, f, indent=4)

    print(f"Results are:")
    for k, v in total_results.items():
        print(f"{k}: {v*100:.2f}")

    return total_results

        
if __name__ == "__main__":
    main()