import json
import re

def format_it_1(ans):
    json_list = []
    example_list = ans.split("\n{\n")

    for example in example_list[1:]:
        example = example.strip("},\n`")
        prompt, completion = example.split("\",\n  \"completion\": \"")
        prompt = prompt.strip("{\n  \"prompt\": \"")
        completion = completion.strip()
        json_dict = {"prompt": prompt, "completion": completion}
        json_list.append(json_dict)

    json_output = json.dumps(json_list, indent=4)
    return json_output


def format_it_2(ans):
   
    # Split the ans into prompts and completions using regex
    pattern = r'\d+\. {\n\s+"prompt": "(.*?)",\n\s+"completion": "(.*?)"\n}\n'

    matches = re.findall(pattern, ans, re.DOTALL)
    print(matches)
    
    # Combine prompts and completions
    result = []
    for prompt, completion in matches:
        prompt_dict = json.loads(prompt.strip().replace('\n', '').replace('\r', ''))
        completion_dict = json.loads(completion.strip().replace('\n', '').replace('\r', ''))
        result.append({'prompt': prompt_dict['prompt'], 'completion': completion_dict['text']})

    # Convert the result to JSON
    return result

def format_prompts_completions(data):
    # Split the data into prompts and completions using regex
    pattern = r'Prompt:(.*?)\nCompletion:(.*?)\n\n\d'
    matches = re.findall(pattern, data, re.DOTALL)
    # Combine prompts and completions
    result = []
    for prompt, completion in matches:
        prompt_dict = json.loads(prompt.strip().replace('\n', '').replace('\r', ''))
        completion_dict = json.loads(completion.strip().replace('\n', '').replace('\r', ''))
        result.append({'prompt': prompt_dict['prompt'], 'completion': completion_dict['text']})

    # Convert the result to JSON
    return result

for i in range(5,84):
    with open(f"prompts_completion_maker/Q{i}_bot.json", "r") as read_file:
        ans = json.load(read_file)
        ans = ans["content"]
        
        try:
            json_data = format_it_2(ans)
            if json_data == []:
                continue
            with open(f"prompts_completion_maker/Q{i}_bot_done.json", "w") as write_file:
                json.dump(json_data, write_file, indent=4)
        except:
            continue

# for i in range(6,84):
#     with open(f"prompts_completion_maker/Q{i}_bot.json", "r") as read_file:
#         ans = read_file.read()
#         with open(f"prompts_completion_maker/Q{i}_bot.json", "w") as write_file:
#             json_data = dict()
#             json_data["content"] = ans
#             json.dump(json_data,write_file,indent=4)
        
