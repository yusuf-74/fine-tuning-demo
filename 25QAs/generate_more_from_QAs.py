import openai
import json
from decouple import config
openai.api_key = config("OPENAI_API_KEY")

questions = []
answers = []

with open("/home/yaaa3ser/Desktop/fine-tuning-demo/25QAs/questions.txt", "r") as file:
    data = file.read()
    data = data.split("\n")
    for i in range(0, len(data)):
        questions.append(data[i])
    

with open("/home/yaaa3ser/Desktop/fine-tuning-demo/25QAs/answers.txt", "r") as file:
    data = file.read()
    data = data.split("$$$")
    for i in range(0, len(data)):
        answers.append(data[i])
        
        
for i in range(len(questions)):
    prompt = f"""Generate the data in JSON array format, with the keys "prompt" and "completion". Include the original question/answer pairs in the array.

            Given the following question and answer, generate 10 similar questions and 10 similar answers.
            These questions/answers will be used to train an OpenAI GPT based chatbot to answer questions about the "Toronto Metropolitan University" and it should not answer with information outside the information provided below.
            Question: {questions[i]}
            
            Answer: {answers[i]}
    """
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.2,
        max_tokens=3000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    try:
        with open(f"/home/yaaa3ser/Desktop/fine-tuning-demo/25QAs/generated_QAs{i}.json", "w") as file:
            json.dump(json.loads(response["choices"][0]["text"]),file,indent=4)
    except:
        print("error")
        with open(f"/home/yaaa3ser/Desktop/fine-tuning-demo/25QAs/generated_A{i}.json", "w") as file:
            list_of_questions = response['choices'][0]['text'].strip('\n')
            fidx = list_of_questions.find('[')
            lidx = list_of_questions.find(']')
            list_of_questions = json.loads(list_of_questions[fidx:lidx+1])
            
            json.dump(list_of_questions,file,indent=4)