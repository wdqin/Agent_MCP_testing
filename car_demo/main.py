import json
from utils import load_json_file, interpret_time_string, interpret_preference_time_string
from agent import QwenAgentWrapper
# from qwen_agent.agents import Assistant  # or your wrapper
# import os

# TEMPORARY FILE PATHS
STATUS_FILE = "./data/status.json"
HISTORY_FILE = "./data/history.json"
PREFERENCE_FILE = "./data/preference.json"

LLM_CONFIG_FILE = "./configs/llm_config.json"
TOOL_CONFIG_FILE = "./configs/agent_tool_config.json"

# JUST FOR TESTING
action = "auto-navigation"

def convert_status_to_prompt_text(status_dict):
    def add_text_header():
        return "the following is a description of the car status: \n"
    def add_text_car_id(status_id):
        return f"the car ID is {status_id}\n"
    def add_text_current_time(current_time):
        return f"the current local time is {current_time}\n"
    def add_text_current_location(current_location):
        return f"the current car location is {current_location}\n"

    
    status_text =  add_text_header() + "[\n" + add_text_car_id(status_dict['car_id']) + \
                                 add_text_current_time(interpret_time_string(status_dict['car_current_time'])) + \
                                 add_text_current_location(status_dict['car_current_location']) + "]\n"
                  
    return status_text

def convert_history_to_prompt_text(history_dict_list):
    # car_id"0"
    # time"25:08:06:13:47"
    # car_start_location"121.307751, 31.208762"
    # car_end_location"121.457775, 31.253214"
    # purpose"to_work"
    def add_text_header():
        return "the following is a history of car travel history: \n"
    def add_text_car_id(history_id):
        return f"the car ID is {history_id}\n"
    def add_text_start_time(history_start_time):
        return f"the travel start time is {interpret_time_string(history_start_time)}\n"
    def add_text_end_time(history_end_time):
        return f"the travel end time is {interpret_time_string(history_end_time)}\n"
    def add_text_start_location(history_start_location):
        return f"the start location is {history_start_location}\n"
    def add_text_end_location(history_end_location):
        return f"the end location is {history_end_location}\n"
    def add_text_purpose(history_purpose):
        
        if history_purpose == "to_home":
            purpose = "to go home"
        elif history_purpose == "to_work":
            purpose = "to go to work"
        elif history_purpose == "to_eat":
            purpose = "to go to eat"
        else:
            purpose = "not specified"
        return f"the purpose is {purpose}\n"
    text = "{\n" +add_text_header()
    for i,history_dict in enumerate(history_dict_list):
        text += "[\n"
        text += f"travel_id: {str(i+1)}\n"
        text += add_text_car_id(history_dict['car_id'])
        text += add_text_start_time(history_dict['car_start_time'])
        text += add_text_end_time(history_dict['car_end_time'])
        text += add_text_start_location(history_dict['car_start_location'])
        text += add_text_end_location(history_dict['car_end_location'])
        text += add_text_purpose(history_dict['purpose'])
        text += "],\n"
    text += "}\n"
    return text

def convert_preference_to_prompt_text(preference_dict):
    def add_text_header():
        return "the following is the preference of car driver: \n"
    def add_text_car_id(preference_id):
        return f"the car ID is {preference_id}\n"
        
    def add_text_home_location(preference_home_location):
        return f"the home location is {preference_home_location}\n"
    def add_text_home_time(preference_home_time):
        return f"the estimate go home time is {interpret_preference_time_string(preference_home_time)}\n"
    
    def add_text_work_location(preference_work_location):
        return f"the work location is {preference_work_location}\n"
    def add_text_work_time(preference_work_time):
        return f"the estimate go to work time is {interpret_preference_time_string(preference_work_time)}\n"
    
    def add_text_breakfast_location(preference_breakfast_location):
        return f"the breakfast locations are {preference_breakfast_location}\n"
    def add_text_breakfast_time(preference_breakfast_time):
        return f"the estimated breakfast time is {interpret_preference_time_string(preference_breakfast_time)}\n"

    def add_text_dinner_location(preference_dinner_location):
        return f"the dinner locations are {preference_dinner_location}\n"
    def add_text_dinner_time(preference_dinner_time):
        return f"the estimated dinner time is {interpret_preference_time_string(preference_dinner_time)}\n"

    text = "{\n" +add_text_header()
    
    text += add_text_car_id(preference_dict['car_id'])
    text += add_text_home_location(preference_dict['car_preference_home_location'])
    text += add_text_home_time(preference_dict['car_preference_estimate_home_time'])
    
    text += add_text_work_location(preference_dict['car_preference_working_location'])
    text += add_text_work_time(preference_dict['car_preference_estimate_work_time'])

    text += add_text_breakfast_location(preference_dict['car_preference_breakfast_restaurants'])
    text += add_text_breakfast_time(preference_dict['car_preference_estimate_breakfast_time'])

    text += add_text_dinner_location(preference_dict['car_preference_dinner_restaurants'])
    text += add_text_dinner_time(preference_dict['car_preference_estimate_dinner_time'])
    
    text += "}\n"

    return text

def add_text_action(action):
    if action == "auto-navigation":   
        # return "1. show what tools are available."
        # return "1. Extract the start, end address, and their purpose of each item in the car travel history, then predict which is the home address and work address. 2. Extract the current time and location of the car. 3. Should the next navigation to be set for going home or going to work? In this case, write a prompt with the current location address and destination address to ask amap_agent_mcp to generate a driving route?"
        # return "Say hello to gpt-oss by gpt_llm_mcp and show reply."
        return "1. Based on the preference, predict which navigation purpose to take next from 'go home', 'go to work', and 'go to eat'. 2. Predict preferred destination. 3. Calculate a viable driving route to the preferred destination with amap_agent_mcp." # 5. summarize the route, show it."
# Entry point
if __name__ == "__main__":

    # step 1: load data (into a prompt).
    status = load_json_file(STATUS_FILE)
    history = load_json_file(HISTORY_FILE)
    preference = load_json_file(PREFERENCE_FILE)

    car_info = {
                    "action_received": action,
                    "status": status,
                    "history": history,
                    "preference": preference
                }    
    prompt = convert_status_to_prompt_text(car_info['status'])
    prompt += convert_history_to_prompt_text(car_info['history'])
    prompt += convert_preference_to_prompt_text(car_info['preference'])
    prompt += add_text_action("auto-navigation")
    
    # step 2: load agent
    agent = QwenAgentWrapper.from_json(LLM_CONFIG_FILE, TOOL_CONFIG_FILE)
    agent.initialize_agent()
    
    # step 3: Send prompt to agent 
    msg = agent.chat(prompt)
    print("msg",msg[-1]['content'])
    response = msg[-1]['content'].split('</think>')[-1]
    with open("output.txt", "w", encoding="utf-8") as f:
        f.write(response)

    