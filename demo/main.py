import os
import json
import openai
import random
import datetime
import transformers
import pandas as pd

from pathlib import Path
from pprint import pprint
from collections import defaultdict

from langchain import PromptTemplate
from langchain.agents import create_pandas_dataframe_agent
from langchain.llms.openai import OpenAI
from langchain.callbacks import get_openai_callback
from langchain.agents import AgentType

from utils import ModelArguments, DataArguments, TrainingArguments

class AgentConfig():
    def __init__(self,
                 config,
                 model_args,
                 data_args):
        self.config = config
        self.model_args = model_args
        self.data_args = data_args
        
        self.task_objective = config["task_objective"]
        self.kb_df = self._load_knowledge_base()
        self._load_prompt_config()
        self.attributes = list(self.kb_df.columns)
        
    
    def _load_prompt_config(self):
        
        self.prompt_bs_template = PromptTemplate(template=self.config["proxy_bs"]["template"],
                                                 input_variables=self.config["proxy_bs"]["input_variables"])
        self.bs_instruction = self.config["proxy_bs"]["instruction"]
        self.bs_example = self.config["proxy_bs"]["example"]

        self.prompt_rg_template = PromptTemplate(template=self.config["response_generation"]["template"],
                                                 input_variables=self.config["response_generation"]["input_variables"])
        self.rg_instruction = self.config["response_generation"]["instruction"]
        self.rg_example = self.config["response_generation"]["example"]
        
        self.prompt_chitchat_template = PromptTemplate(template=self.config["chitchat"]["template"],
                                                       input_variables=self.config["chitchat"]["input_variables"])
        self.chitchat_instruction = self.config["chitchat"]["instruction"]
        
        self.prompt_classification_template = PromptTemplate(template=self.config["classification"]["template"],
                                                             input_variables=self.config["classification"]["input_variables"])
        self.classification_instruction = self.config["classification"]["instruction"]
        self.classification_example = self.config["classification"]["example"]
        
        self.welcome_sentence = f"Hi! I am a TOD with chitchat capability. My current task is {self.task_objective}. What can I help you with?"
        
        
    def _load_knowledge_base(self):
        
        kb_ext = os.path.splitext(self.data_args.load_path)[-1]
        kb_path = self.data_args.load_path
        if kb_ext == ".json":
            kb_df = pd.read_json(kb_path)
        elif kb_ext == ".csv":
            kb_df = pd.read_csv(kb_path)
        elif kb_ext == ".xlsx":
            kb_df = pd.read_excel(kb_path) 
        else:
            raise ValueError(f"Knowledge base should be either json, csv or xslx. Current kb_path: {kb_path}")
        
        return kb_df
    

    def _completion(self, prompt):
        
        if "gpt-3.5-turbo" in self.model_args.model_name_or_path or "gpt-4" in self.model_args.model_name_or_path:
            try:
                completion = openai.ChatCompletion.create(
                        model=self.model_args.model_name_or_path.replace("openai/", ""),
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0
                    )
            except: #Try twice, API sometimes fails due to server issues
                completion = openai.ChatCompletion.create(
                    model=self.model_args.model_name_or_path.replace("openai/", ""),
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
            response = completion.choices[0].message.content.strip()

        else:
            raise ValueError("model_name_or_path should be gpt-3.5-turbo or gpt-4 for this setting")
        
        return response  
    
    
    def flush_logs(self):
        
        self.conversation_logs = defaultdict(list)
        
        
    def _create_session_logs(self):
        
        self.conversation_logs[self.session_id] = {0:{"utterance":self.welcome_sentence,
                                                      "speaker":"SYSTEM",
                                                      "mode":"",
                                                      "belief_state":"",
                                                      "database_query":""}}
         
    def _update_logs(self, utterance, speaker, mode="", bs="", kb=""):
        
        self.conversation_logs[self.session_id][self.turn] = {"utterance":utterance,
                                                              "speaker":speaker,
                                                              "mode":mode,
                                                              "belief_state":bs,
                                                              "database_query":kb}
        self.turn += 1
    
    def _save_logs(self):
        log_file = datetime.datetime.now().strftime("log__%d-%m-%Y__%H-%M-%S.json")
        with open(os.path.join(self.data_args.log_path, log_file), "w") as f:
            json.dump(self.conversation_logs, f, indent=4)
    
    
    
    
class InstructTODS(AgentConfig):

    def __init__(self, 
                 config, 
                 model_args, 
                 data_args):
        super().__init__(config, 
                         model_args, 
                         data_args)
        
        self.conversation_logs = defaultdict(list)
        self.agent = self._load_agent()
        self.turn = 1
        
    
    def _print_config(self):
        print("\n\n")
        print("=================="*5)
        print(f"Current task: {self.task_objective}")
        print(f"Max dialogue history for belief state context: {self.data_args.dialog_history_limit_bs}")
        print(f"Max dialogue history for response generation context: {self.data_args.dialog_history_limit_rg}")
        print(f"Config file: {self.data_args.config_path}")
        print(f"Logging directory: {self.data_args.log_path}")
        print(f"Knowledge base path: {self.data_args.load_path}\n")
        print("To exit the interaction, type 'q' or 'quit' in the prompt")
        print("=================="*5)
        print("\n\n")
        


    def _load_agent(self):
        #Only support using OpenAI models currently (GPT3.5, GPT4)
        
        model = OpenAI(model_name=self.model_args.model_name_or_path, 
                       temperature=self.model_args.temperature)

        agent = create_pandas_dataframe_agent(llm=model, 
                                              df=self.kb_df, 
                                              max_iterations=self.data_args.agent_max_iterations, 
                                              verbose=self.data_args.verbose)
        
        return agent

    
    def reset_knowledge_base(self, df):
        
        self.agent = create_pandas_dataframe_agent(llm=self.model, 
                                                   df=df, 
                                                   max_iterations=self.data_args.agent_max_iterations, 
                                                   verbose=self.data_args.verbose)
    
    
    def reset_task_objective(self, objective:str):
        
        self.task_objective = objective

        
    
    def _parse_dialogue_history(self, mode):
        
        prompt_dh = ""       
        speakers = [v for turn, content in self.conversation_logs[self.session_id].items() for k, v in content.items() if k == "speaker"]
        dh = [v for turn, content in self.conversation_logs[self.session_id].items() for k, v in content.items() if k == "utterance"]
        
        if mode == "bs":
            dh_limit = self.data_args.dialog_history_limit_bs
        elif mode == "rg":
            dh_limit = self.data_args.dialog_history_limit_rg
        else:
            raise ValueError("Can only parse dialogue history in two modes: bs or rg.")
        
        #Assume here that we only use this method when the last turn was from the user
        if len(dh) < dh_limit:
            L = len(dh)
        else:
            L = dh_limit

        for idx in reversed(range(1, L+1)):
            prompt_dh += f"{speakers[-idx]}: {dh[-idx]}\n"

        return prompt_dh


    def _tod_or_chitchat(self, utterance):
        
        dialogue_context = self._parse_dialogue_history(mode="rg")
        prompt = self.prompt_classification_template.format(instruction=self.classification_instruction,
                                                            example=self.classification_example,
                                                            task=self.task_objective,
                                                            dialogue_context=dialogue_context,
                                                            utterance=utterance)
        output = self._completion(prompt) 
        return output

    
    def _tod_turn(self, utterance):
        
        # print(f"USER: {utterance}")
        dialogue_context_bs = self._parse_dialogue_history(mode="bs") + f"USER: {utterance}"
        prompt = self.prompt_bs_template.format(instruction=self.bs_instruction,
                                                example=self.bs_example,
                                                information=", ".join(self.attributes),
                                                dialogue_context=dialogue_context_bs)
        output = self._completion(prompt)
        print(f"\n----------------\nCurrent belief state: {output}")
        self._update_logs(utterance, "USER", bs=output)

        with get_openai_callback() as cb:
            try:
                query_df = self.agent.run(f"If there are many fitting this criteria, pick a few to propose: {output}") #Use fake intermediary belief state
            except ValueError as e:
                response = str(e)
                if not response.startswith("Could not parse LLM output: `"):
                    raise e
                query_df = response.removeprefix("Could not parse LLM output: `").removesuffix("`")
            if self.model_args.print_cost:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost (USD): ${cb.total_cost}")
                
        if query_df == "Agent stopped due to iteration limit or time limit.":
            query_df = "There is nothing that fits the criteria. Ask for more information."
        print(f"Query database results: {query_df}\n----------------\n")
        dialogue_context_rg = self._parse_dialogue_history(mode="rg") + f"USER: {utterance}\nSYSTEM:"
        prompt = self.prompt_rg_template.format(instruction=self.rg_instruction,
                                                example=self.rg_example,
                                                dialogue_context=dialogue_context_rg,
                                                dialogue_act=query_df)
        response = self._completion(prompt)
        print(f"SYSTEM: {response}")
        self._update_logs(response, "SYSTEM", mode=self.mode, kb=query_df)

        return response

    
    def _chitchat_turn(self, utterance):
        
        self._update_logs(utterance, "USER")
        # print(f"USER: {utterance}")
        dialogue_context = self._parse_dialogue_history(mode="rg") + f"USER: {utterance}\nSYSTEM:"
        prompt = self.prompt_chitchat_template.format(instruction=self.chitchat_instruction,
                                                      dialogue_context=dialogue_context)
        # print(dialogue_context)
        response = self._completion(prompt)
        print(f"SYSTEM: {response}")
        self._update_logs(response, "SYSTEM", self.mode)
        
        return response

    
    def interact(self):
        
        self.session_id = random.randint(100000000,999999999)
        self._create_session_logs()
        utterance = ""
        
        self._print_config()
        print(f"{self.welcome_sentence}\n=========================================\n")

        while True:
            utterance = input("USER: ")
            if utterance == "quit" or utterance == "q":
                self._save_logs()
                return "Finished" #TBD
            
            
            is_tod = self._tod_or_chitchat(utterance)
            
            if "yes" in is_tod.lower():
                self.mode = "Task-Oriented Dialogue"
                self._tod_turn(utterance)
            elif "no" in is_tod.lower():
                self.mode = "Chitchat"
                self._chitchat_turn(utterance)
            print("=========================================\n")
            
            
if __name__ == "__main__":
    parser = transformers.HfArgumentParser((ModelArguments, DataArguments, TrainingArguments))
    model_args, data_args, training_args = parser.parse_args_into_dataclasses()
    
    CONFIG = json.load(open(data_args.config_path, "r"))
    
    instructtods = InstructTODS(config=CONFIG,
                                model_args=model_args,
                                data_args=data_args)
    
    instructtods.interact()