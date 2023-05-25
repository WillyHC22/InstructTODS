import os

# CONFIG = {
#     "openai_api_key": os.environ["OPENAI_API_KEY"], #Put your own there
#     "openai_organization": os.environ["OPENAI_API_ORG"], #Put your own there (needed afaik if using gpt4)
#     #NEED TO RENAME THESE TO SLOT FREE DST (no need to even know slot name)
#     "INSTRUCTION_PROMPTS":["""Using the following context, generate the belief states of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting in a json format:\n""",
#                            """You are a task-oriented dialogue system focusing on doing Dialogue State Tracking. Using the following knowledge base as grounding for acts, slots and values, generate the belief state of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. The results should be in json format with 'domain', 'act' and 'belief_state' as information:\n""",
#                            """You are a task-oriented dialogue system focusing on doing Dialogue State Tracking. Using the following knowledge base as grounding for acts, slots and values, generate the belief state of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. The results should be in json format with 'domain', 'act' and 'belief_state' as primary keys, for example {'domain':domain, 'act':act, 'belief_state':{first slot: first value, second slot: second value, etc...}:\n""",
#                            """You are a task-oriented dialogue system focusing on doing Dialogue State Tracking. Using the following SLOTS provided, generate the belief state of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. The results should be in json format with the slot name as the primary key, and the retrieved value associated to the slot, for example {'slot1':'value1', 'slot2':'value2', etc...}:\n"""],
#     "CORRECTION_INSTRUCTION_PROMPTS": ["""You are a task-oriented dialogue system focusing on doing Dialogue State Tracking. Using the following knowledge base as grounding for acts, slots and values, another faulty system already generated the belief state of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. If you think the belief states are inaccurate, you should generate new correct belief state. The dialogue states should only be related to the information the USER is looking for, and not what the SYSTEM should give. If you think the given belief states are accurate, then just say 'correct'. The newly generated results should follow the same json format with 'domain', 'act' and 'belief_state' as information:\n""",
#                                        """You are a task-oriented dialogue system focusing on doing Dialogue State Tracking. Using the following knowledge base as grounding for acts, slots and values, another faulty system already generated the belief state of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. You should generate the new and correct belief state. The belief state should only be related to the information the USER is looking for, and not what the SYSTEM needs to give. The newly generated results should follow the same json format with 'domain', 'act' and 'belief_state' as primary keys:\n"""],
#     "SLOTS_GENERATION_INSTRUCTION_PROMPTS": [""""""],
#     "PROMPT_TEMPLATE":{"template": """{instruction}\n\nKnowledge base:\n{ontology}\n\nContext:\n{dialogue}""",
#                        "input_variables": ["instruction", "ontology", "dialogue"]},
#     "PROMPT_TEMPLATE_WITHOUT_ONTOLOGY":{"template": """{instruction}\n\nContext:\n{dialogue}""",
#                                         "input_variables": ["instruction", "dialogue"]},
#     "CORRECTION_PROMPT_TEMPLATE":{"template": """{instruction}\n\nKnowledge base:\n{ontology}\n\nContext:\n{dialogue}\n\nPredicted Belief State:\n{belief_state}""",
#                                   "input_variables": ["instruction", "ontology", "dialogue", "belief_state"]},
#     "CORRECTION_PROMPT_TEMPLATE_WITHOUT_ONTOLOGY":{"template": """{instruction}\n\nContext:\n{dialogue}\n\nPredicted Belief State:\n{belief_state}""",
#                                                    "input_variables": ["instruction", "dialogue", "belief_state"]},
#     "PROMPT_TEMPLATE_SLOTS_GENERATION":{"template": """Complete the following python dictionnary named SLOTS of the most general slots that a USER can query in a task-oriented dialogue setting for belief state tracking in the following domain: {domains_string}. The dictionnary should hav for primary keys the possible domains, for example "SLOTS = {{"domain1":[slot1, slot2, etc...], "domain2":[slot1, slot2, etc...]}}\n\nSLOTS = {{""",
#                                         "input_variables": ["domains_string"]}, #Generates dictionnary SLOTS = {domain:[list of slots]}
# }


CONFIG = {
    "openai_api_key": os.environ["OPENAI_API_KEY"], #Put your own there
    "openai_organization": os.environ["OPENAI_API_ORG"], #Put your own there (needed afaik if using gpt4)
    "INSTRUCTIONS":{"instruction_with_extracted_ontology":"""You are a task-oriented dialogue system focusing on doing Dialogue State Tracking. Using the following knowledge base as grounding for acts, slots and values, generate the belief state of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. The results should be in json format with 'domain', 'act' and 'belief_state' as primary keys, for example {'domain':domain, 'act':act, 'belief_state':{first slot: first value, second slot: second value, etc...}:""",
                   "instruction_with_slots":"""Generate the belief state of the very last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. The results should be in json format following this format: {'slot1':'value1', 'slot2':'value2', etc...}. Use the slot from SLOTS to generate the belief state:""",
                   "instruction_with_slots_recorrect":"""You are a task-oriented dialogue system focusing on doing Dialogue State Tracking. Using the following SLOTS provided, another faulty system already generated the belief state of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. You should generate the new and correct belief state. The results should be in json format with the slot name as the primary key, and the retrieved value associated to the slot, for example {'slot1':'value1', 'slot2':'value2', etc...}:""",
                   "instruction_with_slots_recorrect_2":"""Using the following SLOTS provided with their description, another faulty system already generated the WRONG BELIEF STATES of the last dialogue turn in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. You should generate the new and CORRECTED BELIEF STATES. The results should be in json format following this format: {'slot1':'value1', 'slot2':'value2', etc...}.""",
                   "instruction_with_slots_recorrect_3":"""Using the following SLOTS provided, another system generated the WRONG BELIEF STATES of the last dialogue turn in the conversation between a USER and a SYSTEM given in the CONTEXT, in a task-oriented dialogue setting. You should generate the CORRECTED BELIEF STATES. The results should be in json format following this format: {'slot1':'value1', 'slot2':'value2', etc...}.""",
                   "instruction_with_slots_recorrect_4":"""A task-oriented dialogue system has generated the following belief state: {belief_state} for the following dialogue. The belief states are slightly wrong, so use the provided SLOTS to generate the corrected belief states. The results should be in json format following this format: {'slot1':'value1', 'slot2':'value2', etc...}.""",
                   "instruction_query_database":"""""", #TODO
                   "instruction_response_generation":"""""" #TODO
                   }, 
    "PROMPT_TEMPLATES":{"template_with_extracted_ontology":{"template": """{instruction}\n\nKNOWLEDGE BASE:\n{ontology}\n\nCONTEXT:\n{dialogue_context}""",
                                                           "input_variables": ["instruction", "ontology", "dialogue_context"]},
                       "template_with_slots":{"template": """{instruction}\n\nSLOTS:\n{slots}\n\nCONTEXT:\n{dialogue_context}""",
                                                           "input_variables": ["instruction", "slots", "dialogue_context"]},
                       "template_with_slots_recorrect":{"template": """{instruction}\n\nSLOTS:\n{slots}\n\nCONTEXT:\n{dialogue_context}\n\nWRONG BELIEF STATES:\n{belief_states}\n\nCORRECT BELIEF STATES:""",
                                                        "input_variables": ["instruction", "slots", "dialogue_context", "belief_states"]},
                       "template_with_slots_recorrect_4":{"template": """{instruction}\n\nSLOTS:\n{slots}\n\nCONTEXT:\n{dialogue_context}\n\n""",
                                                        "input_variables": ["instruction", "slots", "dialogue_context"]},
                       "template_query_database":{"template": """{instruction}\n\nBELIEF STATES:\n{belief_states}\n\nSELECT * FROM""",
                                                           "input_variables": ["instruction", "belief_states"]},
                       "template_response_generation":{"template": """{instruction}\n\nDIALOGUE ACTS:\n{dialogue_acts}\n\nCONTEXT:\n{dialogue_context}""",
                                                           "input_variables": ["instruction", "dialogue_acts", "dialogue_context"]},
                      },
    "multiwoz21":{
                "requestable_slots" : {"taxi": ["car", "phone"],
                                    "police": ["postcode", "address", "phone"],
                                    "hospital": ["address", "phone", "postcode"],
                                    "hotel": ["address", "postcode", "type", "internet", "phone", "parking", "pricerange", "stars", "area", "reference"],
                                    "attraction": ["price", "address", "type", "postcode", "phone", "area", "reference"],
                                    "train": ["time", "leaveat", "price", "arriveby", "id", "reference"],
                                    "restaurant": ["phone", "postcode", "address", "pricerange", "food", "area", "reference"]
                                    },
                "informable_slots" : {"taxi": ["leaveat", "destination", "departure", "arriveby"],
                                    "police": [],
                                    "hospital": ["department"],
                                    "hotel": ["parking", "pricerange", "type", "internet", "stay", "day", "people", "area", "stars", "name"],
                                    "attraction": ["area", "type", "name"],
                                    "train": ["destination", "day", "arriveby", "departure", "people", "leaveat"],
                                    "restaurant": ["food", "pricerange", "area", "name", "time", "day", "people"]
                                    },
                "all_requestable_slots":["car", "address", "postcode", "phone", "type", "internet",  "parking", "pricerange", "food",
                                "stars", "area", "reference", "time", "leaveat", "price", "arriveby", "id"],
                "all_informable_slots":["parking", "pricerange", "internet", "stay", "type", "day", "people", "area", "stars", "name",
                                "leaveat", "destination", "departure", "arriveby", "food", "time"],
                }
}