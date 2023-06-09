import os
import json
import openai
import pandas as pd
from tqdm import tqdm
from pathlib import Path
from pprint import pprint
from langchain import PromptTemplate

from langchain.agents import create_pandas_dataframe_agent
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import get_openai_callback
from langchain.agents import AgentType

        
class E2E_InstrucTOD():
    def __init__(self, config, model_args, data_args, dataset):
        self.model_args = model_args
        self.data_args = data_args
        self.domains = ["attraction", "hotel", "restaurant", "train"]
        self.dataset = dataset
        self.config = config
        print(f"Loading agents for {self.domains}")
        self.agents = self._load_agents()
                        
        
    def _load_agents(self):
        agents = {}
        if "openai" in self.model_args.model_name_or_path_agent:
            model_name = self.model_args.model_name_or_path_agent.split("/")[1]
        else:
            if "gpt-3.5" not in self.model_args.model_name_or_path_agent:
                raise ValueError("Only gpt-3.5 is used for e2e")
            else:
                model_name = self.model_args.model_name_or_path_agent
        
        llm = OpenAI(model_name=model_name, temperature=0)
        # llm = ChatOpenAI(model_name=model_name, temperature=0)
        for domain in self.domains:
            file_path=os.path.join(self.data_args.mwoz_path, f"{domain}_db.json")
            data = json.loads(Path(file_path).read_text())
            df = pd.DataFrame(data)
            if domain == "attraction":
                df = df.drop(columns=["location"])
            elif domain == "hotel":
                df = df.drop(columns=["location", "price", "n"])
                df['stars'] = df['stars'].astype(int)
                df = df[['name'] + [col for col in df.columns if col != 'name']]
            elif domain == "restaurant":
                df = df.drop(columns=["location", "type", "introduction", "signature", "id"])
                # df = df.rename(columns={'food': 'cuisine'})
                df = df[['name'] + [col for col in df.columns if col != 'name']]
            elif domain == "train":
                pass

            agent = create_pandas_dataframe_agent(llm=llm, 
                                                  df=df,
                                                  max_iterations=self.data_args.agent_max_iterations, 
                                                  verbose=self.data_args.verbose)
            agents[domain] = agent  
        return agents

    
    def completion(self, prompt):
        if "gpt-3.5-turbo" in self.model_args.model_name_or_path or "gpt-4" in self.model_args.model_name_or_path:
                
            try:
                completion = openai.ChatCompletion.create(
                        model=self.model_args.model_name_or_path.replace("openai/", ""),
                        messages=[
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0
                    )
            except: #Try twice
                completion = openai.ChatCompletion.create(
                    model=self.model_args.model_name_or_path.replace("openai/", ""),
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0
                )
                
            response = completion.choices[0].message.content.strip()
        else:
            raise ValueError("model_name_or_path should be gpt-3.5-turbo for this setting")
        return response    

    
    def inference(self):
        prompt_query_db_template = PromptTemplate(
            input_variables=self.config["PROMPT_TEMPLATES"]["template_e2e_query_database"]["input_variables"],
            template=self.config["PROMPT_TEMPLATES"]["template_e2e_query_database"]["template"],
        )
        prompt_rg_template = PromptTemplate(
            input_variables=self.config["PROMPT_TEMPLATES"]["template_e2e_rg"]["input_variables"],
            template=self.config["PROMPT_TEMPLATES"]["template_e2e_rg"]["template"],
        )
        examples_e2e_query_db = self.config["EXAMPLES"]["e2e_query_database"]
        examples_e2e_rg = self.config["EXAMPLES"]["e2e_response_generation"]
        instructions_e2e_query_db = self.config["INSTRUCTIONS"]["instruction_e2e_query_database"]
        instructions_e2e_rg = self.config["INSTRUCTIONS"]["instruction_e2e_rg"]

        prompts_e2e_query_db = []
        preds_e2e_query_db = []
        preds_e2e_dialog_acts = []
        prompts_e2e_rg = []
        preds = []
        gold_responses = []
        idxs = []
        turn_domains = []
        for idx, row in tqdm(self.dataset.iterrows()):
            sample_id = row["id"]
            turn_domain = row["turn_domain"]
            dialogue_context = row["prompt_e2e"].split("\n\n")[-1]
            gold_response = row["gold_response"]
            
            prompt_query_db = prompt_query_db_template.format(instruction=instructions_e2e_query_db,
                                                              example=examples_e2e_query_db,
                                                              dialogue_context=dialogue_context[:-9])
            if turn_domain in self.domains:
                print(dialogue_context)
                pred_query_db = self.completion(prompt_query_db)
                print(pred_query_db)
                with get_openai_callback() as cb:
                    
                    try:
                        dialog_act = self.agents[turn_domain].run(f"If there are many fitting this criteria, pick a few to propose: {pred_query_db}")
                    except:
                        # response = str(e)
                        # if not response.startswith("Could not parse LLM output: `"):
                        #     raise e
                        dialog_act = "none"
                    print(f"Total Tokens: {cb.total_tokens}")
                    print(f"Prompt Tokens: {cb.prompt_tokens}")
                    print(f"Completion Tokens: {cb.completion_tokens}")
                    print(f"Total Cost (USD): ${cb.total_cost}")
                if dialog_act == "Agent stopped due to iteration limit or time limit.":
                    dialog_act = "none."
                print(dialog_act)

                prompt_rg = prompt_rg_template.format(instruction=instructions_e2e_rg,
                                                      example=examples_e2e_rg,
                                                      dialogue_context=dialogue_context[:-9],
                                                      dialogue_act=dialog_act)
            
                response = self.completion(prompt_rg)
                print(response)
            else:
                pred_query_db = "none"
                intermediate_step = "none"
                dialog_act = "none"
                prompt_rg = prompt_rg_template.format(instruction=instructions_e2e_rg,
                                                     example=examples_e2e_rg,
                                                     dialogue_context=dialogue_context[:-9],
                                                     dialogue_act=dialog_act)
                response = self.completion(prompt_rg)
            
        
            prompts_e2e_query_db.append(prompt_query_db)
            turn_domains.append(turn_domain)
            preds_e2e_query_db.append(pred_query_db)
            preds_e2e_dialog_acts.append(dialog_act)
            prompts_e2e_rg.append(prompt_rg)
            preds.append(response)
            gold_responses.append(gold_response)
            idxs.append(sample_id)
            
            if idx % self.data_args.save_every == 0:
                temp_save_path = self.data_args.save_path[:-4] + "_latestSave.csv"
                temp_df = pd.DataFrame({"id":idxs,
                                        "gold_response":gold_responses,
                                        "preds":preds,
                                        "prompts_e2e_query_db":prompts_e2e_query_db,
                                        "preds_e2e_query_db":preds_e2e_query_db,
                                        "preds_e2e_dialog_acts":preds_e2e_dialog_acts,
                                        "prompts_e2e_rg":prompts_e2e_rg,
                                        "turn_domain":turn_domains
                                        })
                temp_df.to_csv(temp_save_path)
        
        
        df = pd.DataFrame({"id":idxs,
                           "gold_response":gold_responses,
                           "preds":preds,
                           "prompts_e2e_query_db":prompts_e2e_query_db,
                           "preds_e2e_query_db":preds_e2e_query_db,
                           "preds_e2e_dialog_acts":preds_e2e_dialog_acts,
                           "prompts_e2e_rg":prompts_e2e_rg,
                           "turn_domain":turn_domains
                           })
        df.to_csv(self.data_args.save_path)
        return df
            
            
