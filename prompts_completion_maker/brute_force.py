import json

data = list()

for i in range(1,5):
    try:
        with open (f"prompts_completion_maker/Q{i}_me.json","r") as file:
            file_data = json.load(file)
            data += file_data
    except:
        print(f"file : {i}")
for i in range(5,84):
    try:
        with open (f"prompts_completion_maker/Q{i}_bot.json","r") as file:
            file_data = json.load(file)
            data += file_data
    except:
        print(f"file : {i}")

with open (f"prompts_completion_maker/all_done.json","w") as file:
    json.dump(data,file,indent=4)