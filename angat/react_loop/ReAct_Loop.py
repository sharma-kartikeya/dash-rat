from ..llm_model import openAiChat
import re
from ..actions.actions import available_actions

def extract_action(log_string):
    # Adjusted pattern to handle multiline and quoted values
    pattern = r"ACTION:\s*{\s*function_name:\s*([^\s,]+)\s+function_params:\s*{([\s\S]*?)\s*}\s*}"
    
    # Search for pattern in log_string
    match = re.search(pattern, log_string)
    
    if match:
        function_name = match.group(1)
        params_str = match.group(2).strip()

        # Extract key-value pairs from function_params
        function_params = {}
        
        # Matches key-value pairs, where values can be quoted strings or numbers
        param_pattern = r'(\w+):\s*("[^"]*"|\S+)'
        for param in re.findall(param_pattern, params_str):
            key, value = param
            # Remove quotes from quoted values
            function_params[key] = value.strip('"').strip(',')
        
        # Construct the final dictionary
        action_dict = {
                "function_name": function_name,
                "function_params": function_params
        }
        
        return action_dict
    
    return None

# Example usage
# log_string = """
# Some log data...
# ACTION: {
#     function_name: myFunction,
#     function_params: {
#         param1: value1,
#         param2: value2
#     }
# }
# More log data...
# """

# extracted_action = extract_action(log_string)
# print(extracted_action)

def agentic_loop(user_message: str):
    turn_count = 1
    max_turns = 2

    openAiChat.user_message(f'OBSERVATION: {user_message}')
    response = openAiChat.messages[-1]

    while turn_count < max_turns:
        print (f"Loop: {turn_count}")
        print("----------------------")
        turn_count += 1

        action_dict = extract_action(response['content'])

        if action_dict:
                function_name = action_dict['function_name']
                if function_name == "chat_with_user":
                     break
                function_parms = action_dict['function_params']
                if function_name not in available_actions:
                    raise Exception(f"Unknown action: {function_name}: {function_parms}")
                print(f" -- running {function_name} {function_parms}")
                action_function = available_actions[function_name]
                #call the function
                result = action_function(**function_parms)
                function_result_message = f"OBSERVATION: {result}"
                openAiChat.user_message(function_result_message)
                print(function_result_message)
        else:
             break