import json

for i in range(10):
    try:
        with open(f'./prompts_completion_maker/Q&As/questions_{i}.json','r') as f:
            questions = json.load(f)
            questions = json.loads(questions)
        with open(f'./prompts_completion_maker/Q&As/questions_{i}.json','w') as f:
            json.dump(questions,f,indent=4)
    except:
        continue