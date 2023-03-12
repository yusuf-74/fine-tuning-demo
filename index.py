import openai 
from decouple import config
openai.api_key = config('OPENAI_API_KEY')
print(openai.api_key)
while True:
    prompt = """
    in the context of bld.ai (the E-commerce for knowledge workers), answer the following question:
    """
    prompt += input('question: ')
    
    if prompt == 'q':
        break
    print ("processing...")
    response = openai.Completion.create(
        prompt=prompt,
        max_tokens=256,
        temperature=0.2,
        model="davinci:ft-personal-2023-03-10-04-59-57",
        n=1,
        stop=["END"]
    )
    print("ans: "+response['choices'][0]['text'])
    
    