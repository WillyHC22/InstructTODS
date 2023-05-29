from dataclasses import dataclass, field
from typing import Optional
from transformers import TrainingArguments


@dataclass
class ModelArguments:
    """
    Arguments pertaining to which model/config/tokenizer we are going to utilize.
    """
    model_name_or_path: Optional[str] = field(
        default=None,
        metadata={"help": "The path of the HuggingFace model."}
    )
    use_int8: Optional[bool] = field(
        default=False,
        metadata={"help": "Whether to use int8 model or not."}
    )
    use_deepspeed: Optional[bool] = field(
        default=False,
        metadata={"help": "Whether to use deepspeed model or not."}
    )
    

@dataclass
class DataArguments:
    """
    Arguments pertaining to the data loading and preprocessing pipeline.
    """
    dataset_name: Optional[str] = field(
        default=None,
        metadata={"help": "Train dataset path"}
    )
    dataset_names: Optional[str] = field(
        default=None,
        metadata={"help": "Train dataset paths"}
    )
    root_data_path: Optional[str] = field(
        default="./data", metadata={"help": "The path to the data directory."},
    )
    mwoz_path: Optional[str] = field(
        default="/home/willy/instructod/MultiWOZ_2.1/",
        metadata={"help": "MWOZ path"}
    )
    dialog_history_limit_dst: Optional[int] = field(
        default=0,
        metadata={"help": "Lenght of dialogue history for dst"}
    )
    dialog_history_limit_dst_recorrect: Optional[int] = field(
        default=0,
        metadata={"help": "Lenght of dialogue history for dst update"}
    )
    dialog_history_limit_rg: Optional[int] = field(
        default=20,
        metadata={"help": "Lenght of dialogue history for response generation"}
    )
    dialog_history_limit_e2e: Optional[int] = field(
        default=20,
        metadata={"help": "Lenght of dialogue history for e2e"}
    )
    single_domain_only: Optional[bool] = field(
        default=False,
        metadata={"help": "Whether to keep only the single domain sample or not"}
    )
    with_slot_description: Optional[bool] = field(
        default=False,
        metadata={"help": "Whether to use slot description or not for DST"}
    )
    with_req_inf_differentiation: Optional[bool] = field(
        default=False,
        metadata={"help": "Whether to differentiate between require and inform slot for DST"}
    )
    with_all_slots: Optional[bool] = field(
        default=True,
        metadata={"help": "Whether to use all slots or not"}
    )
    debug_mode: Optional[bool] = field(
        default=False,
        metadata={"help": "debug mode to only try 20 samples"}
    )
    start_idx: Optional[int] = field(
        default=0,
        metadata={"help": "Starting index to restart the prediction if needed"}
    )
    save_path: Optional[str] = field(
        default="results/",
        metadata={"help": "save path"}
    )
    save_every: Optional[int] = field(
        default=5,
        metadata={"help": "every step to save in case api fail"}
    )
    db_format_type: Optional[str] = field(
        default="1",
        metadata={"help": "1 is more precise, 2 is more concise for db integration"},
    )

@dataclass
class PromptingArguments(TrainingArguments):
    """
    Arguments pertraining to the prompting pipeline.
    """
    output_dir: Optional[str] = field(
        default="./out",
        metadata={"help": "Output directory"},
    )
    task: Optional[str] = field(
        default="dst",
        metadata={"help": "Task to perform"}
    )
    max_requests_per_minute: Optional[int] = field(
        default=20,
        metadata={"help": "Max number of requests for OpenAI API."}
    )
    openai_api_key_name: Optional[str] = field(
        default="OPENAI_API_KEY",
        metadata={"help": "OpenAI API key name."}
    )