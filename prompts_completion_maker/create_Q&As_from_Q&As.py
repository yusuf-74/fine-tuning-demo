import json
import openai
import time

from openai.error import RateLimitError
from decouple import config


openai.api_key = config('OPENAI_API_KEY')

non_formatted_questions = []
organization = 'Toronto Metropolitan University'

with open('training_data_tmu.json','r') as f:
    training_QAs = json.load(f)

for idx,pc in enumerate(training_QAs[7:]):
    prompt = f"""
    Given the following question and answer, generate 10 similar questions and 10 similar answers.
    These questions/answers will be used to train an OpenAI GPT based chatbot to answer questions about the "{organization}" and it should not answer with information outside the information provided below.
    Question: {pc['prompt']}
    Answer: {pc['completion']}
    Generate the data in JSON array format, with the keys "prompt" and "completion". Include the original question/answer pairs in the array.
    the response should start with '[' and end with ']'
    """

    max_retries = 5
    retries = 0
    # retry the request if we get a RateLimitError    
    while retries < max_retries:
        # try to make the request
        try:
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
                # try to write the questions to a JSON file
                with open(f'./prompts_completion_maker/Q&As/from_Q&A/questions_{idx+7}.json','w') as f:
                    
                    list_of_questions = response['choices'][0]['text'].strip('\n')
                    list_of_questions = json.loads(list_of_questions)
                    json.dump(list_of_questions,f,indent=4)
            except:
                try:
                    # try to modify the questions to be in the format list and write them to a JSON file
                    with open(f'./prompts_completion_maker/Q&As/from_Q&A/questions_{idx+7}.json','w') as f:
                        list_of_questions = response['choices'][0]['text'].strip('\n')
                        fidx = list_of_questions.find('[')
                        lidx = list_of_questions.rfind(']')
                        list_of_questions = json.loads(list_of_questions[fidx:lidx+1])
                        json.dump(list_of_questions,f,indent=4)
                except Exception as e:
                    # if the questions could not be handled by the exception handling, add the index of the question to the list of non_formatted_questions
                    non_formatted_questions.append(idx)
            break
        except RateLimitError:
            # if we get a RateLimitError, wait 1 min and try again
            time.sleep(60)
            retries += 1
            if retries == max_retries:
                with open('./prompts_completion_maker/Q&As/from_Q&A/non_formatted_questions.json','w') as f:
                    json.dump(non_formatted_questions,f,indent=4)
                # if we've tried 5 times, raise the error
                raise
            
# save the list of non_formatted_questions to a JSON file
with open ('./prompts_completion_maker/Q&As/not_formated_files.json','w') as f:
    json.dump(non_formatted_questions,f,indent=4)