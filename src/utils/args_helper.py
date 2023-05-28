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
    preprocessing_num_workers: Optional[int] = field(
        default=16,
        metadata={"help": "The number of processes to use for the preprocessing."},
    )
    cache_dir: Optional[str] = field(
        default="cache",
        metadata={"help": "Name of cache directory."},
    )
    prompt_template_id: Optional[int] = field(
        default=0,
        metadata={"help": "Prompt template ID."}
    )
    max_seq_length: Optional[int] = field(
        default=64,
        metadata={
            "help": (
                "The maximum total input sequence length after tokenization. Sequences longer "
                "than this will be truncated, sequences shorter will be padded."
            )
        },
    )
    shard_id: Optional[int] = field(
        default=None,
        metadata={"help": "Shard ID, each shard contains 1000 data. ID starts from 0."}
    )
    num_rows_in_shard: Optional[int] = field(
        default=1000,
        metadata={"help": "Number of data rows per shard. Only used if shard_id is not None."}
    )

@dataclass
class TrainingArguments(TrainingArguments):
    """
    Arguments pertraining to the training pipeline.
    """
    output_dir: Optional[str] = field(
        default="./save",
        metadata={"help": "Output directory"},
    )
    load_best_model_at_end: Optional[bool] = field(
        default=True,
        metadata={"help": "Whether to load the best model at the end or not."}
    )
    evaluation_strategy: Optional[str] = field(
        default="epoch",
        metadata={"help": "Evaluation strategy."}
    )
    save_strategy: Optional[str] = field(
        default="epoch",
        metadata={"help": "Save strategy."}
    )
    evaluation_strategy: Optional[str] = field(
        default="epoch",
        metadata={"help": "Evaluation strategy."}
    )
    logging_strategy: Optional[str] = field(
        default="epoch",
        metadata={"help": "Logging strategy."}
    )
    save_steps: Optional[int] = field(
        default=1,
        metadata={"help": "Save steps."}
    )
    eval_steps: Optional[int] = field(
        default=1,
        metadata={"help": "Evaluation steps."}
    )
    logging_steps: Optional[int] = field(
        default=1,
        metadata={"help": "Logging steps."}
    )
    save_total_limit: Optional[int] = field(
        default=1,
        metadata={"help": "Save total limit."}
    )
    report_to: Optional[str] = field(
        default="tensorboard",
        metadata={"help": "Report to."}
    )
    full_determinism: Optional[bool] = field(
        default=True,
        metadata={"help": "Full determinism."}
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
    max_requests_per_minute: Optional[int] = field(
        default=20,
        metadata={"help": "Max number of requests for OpenAI API."}
    )
    openai_api_key_name: Optional[str] = field(
        default="OPENAI_API_KEY",
        metadata={"help": "OpenAI API key name."}
    )