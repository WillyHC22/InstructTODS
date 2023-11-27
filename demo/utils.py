from dataclasses import dataclass, field
from typing import Optional

@dataclass
class ModelArguments:
    model_name_or_path: Optional[str] = field(
        default="gpt-3.5-turbo-0301",
        metadata={"help": "The path of the HuggingFace model."}
    )
    temperature: Optional[int] = field(
        default=0,
        metadata={"help": "Temperature for the agent's generation"}
    )
    print_cost: Optional[bool] = field(
        default=False,
        metadata={"help": "Print the cost of using the agent for KB interaction at every turn"}
    )


@dataclass
class DataArguments:
    dataset_name: Optional[str] = field(
        default=None,
        metadata={"help": "Train dataset path"}
    )
    root_data_path: Optional[str] = field(
        default="./data", metadata={"help": "The path to the data directory."},
    )
    dialog_history_limit_bs: Optional[int] = field(
        default=3,
        metadata={"help": "Length of dialogue history to take for the proxy belief state"}
    )
    dialog_history_limit_rg: Optional[int] = field(
        default=7,
        metadata={"help": "Length of dialogue history to take for the response generation"}
    )
    log_path: Optional[str] = field(
        default="./demo/logs/",
        metadata={"help": "path for the log directory"}
    )
    load_path: Optional[str] = field(
        default="/data/",
        metadata={"help": "load path for the kb"}
    )
    config_path: Optional[str] = field(
        default="/config.json",
        metadata={"help": "load path"}
    )
    agent_max_iterations: Optional[int] = field(
        default=5,
        metadata={"help": "Max number of iterations for agents in e2e (higher=better but more expensive)"}
    )
    verbose: Optional[bool] = field(
        default=False,
        metadata={"help": "To output the intermediary steps"}
    )
    return_intermediate_steps: Optional[bool] = field(
        default=False,
        metadata={"help": "To log the intermediary steps (KB retrieval process)"}
    )
    
@dataclass
class TrainingArguments:
    pass