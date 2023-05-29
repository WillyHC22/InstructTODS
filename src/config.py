import os

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
                   "instruction_response_generation":"""In a task oriented dialogue setting, generate a SYSTEM response to the USER query in the conversation provided in CONTEXT. You should follow the information provided in ACT to generate this answer. Do not answer with anything other than what is provided in the dialogue act:""",
                   "instruction_e2e":"""Generate the answer of the SYSTEM in the following conversation between a USER and a SYSTEM in a task-oriented dialogue setting. You can either request more details to the user that is available in the knowledge base to complete the goal, or simply answer the user's request. Do not provide multiple choice for the user to choose, just recommend one, and generate nothing other that the SYSTEM reply. Use the following knowledge base to interact with the user:"""
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
                       "template_response_generation":{"template": """{instruction}\n\nYou can follow this example:\n{example}\n\nCONTEXT:\n{dialogue_context}""",
                                                           "input_variables": ["instruction", "example", "dialogue_context"]},
                        "template_e2e":{"template": """{instruction}\n\n{database}\n\n{dialogue_context}""",
                                        "input_variables":["instruction", "database", "dialogue_context"]}
                      },
    "EXAMPLES":{"response_generation":"""USER: How much does the banana cost?\nACT: Inform the user that the price is 10$, the promotion is 80%, and the choice is 5, and request the amount that user wants.\nSYSTEM: There are 5 to choose from. Banana currently cost 10$, with a 80% off. How many would you like?"""},
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