import json

def format_it(ans):
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

for i in range(5,84):
    
    with open(f"prompts_completion_maker/Q{i}_bot.json", "r") as read_file:
        ans = read_file.read()
        try:
            json_data = format_it(ans)
            with open(f"prompts_completion_maker/Q{i}_bot_done.json", "w") as write_file:
                json.dump(json_data, write_file, indent=4)
        
        except:
            continue
        

