import openai
import json
from decouple import config
from answers_formatter import format_it
openai.api_key = config('OPENAI_API_KEY')


with open ("prompts_completion_maker/bld-data-Q&A.json", "r") as file:
    data = file.read()
    data = json.loads(data)
    
    
    for idx,q_a in enumerate(data[69:]):
        prompt = """User: Hello
        Bot: Hi there! How can I assist you today?
        """
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "User:  I want the prompts to be with the meaning of"+q_a['prompt']+\
                "and completions with the meaning of"+q_a['completion']+\
                    "5 examples in json"},
                    ],
            )   
        answer = response["choices"][0]["message"]["content"]
        print(answer)
        with open (f"prompts_completion_maker/Q{idx+69}_bot.json", "w") as file:
            json.dump(answer,file,indent=4)

