import openai
import json
import os
import time


from openai.error import RateLimitError
from decouple import config


openai.api_key = config('OPENAI_API_KEY')

# the Q&As that are not in the format list and could not be handled by the exception handling
non_formatted_questions = []


with open('cleaned_paragraphs.json','r') as f:
    paragraphs = json.load(f)

# iterate over the paragraphs and extract the questions and answers
for idx,paragraph in enumerate(paragraphs):
    prompt = """
    Given the following paragraph, generate 5 to 10 questions and their answers using the information provided in the paragraph
    These questions/answers will be used to train an OpenAI GPT-based chatbot to answer questions about the "Toronto Metropolitan University" and it should not answer with information outside the information provided below.
    only generate questions that can be answered with the information provided in the paragraph
    return the questions and answers in a prompt,completion pairs list JSON format 
    start with '[' and end with ']'
    paragraph: 
    """
    prompt += paragraph 

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
                max_tokens=1160,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
            )
            try:
                # try to write the questions to a JSON file
                with open(f'./prompts_completion_maker/Q&As/questions_{idx}.json','w') as f:
                    list_of_questions = response['choices'][0]['text'].strip('\n')
                    list_of_questions = json.loads(list_of_questions)
                    json.dump(list_of_questions,f,indent=4)
            except:
                try:
                    # try to modify the questions to be in the format list and write them to a JSON file
                    with open(f'./prompts_completion_maker/Q&As/questions_{idx}.json','w') as f:
                        list_of_questions = response['choices'][0]['text'].strip('\n')
                        fidx = list_of_questions.find('[')
                        lidx = list_of_questions.find(']')
                        liist_of_questions = json.loads(list_of_questions[fidx:lidx+1])
                        json.dump(list_of_questions,f,indent=4)
                except:
                    # if the questions could not be handled by the exception handling, add the index of the question to the list of non_formatted_questions
                    non_formatted_questions.append(idx)
            
            # exit the loop if the request succeeds
            break  
        
        # in case of a RateLimitError, wait 60 seconds and try again
        except RateLimitError:
            print('RateLimitError')
            time.sleep(60)
            retries += 1
            if retries == max_retries:
                # write the list of non_formatted_questions to a JSON file before exiting the program
                with open ('./prompts_completion_maker/Q&As/not_formated_files.json','w') as f:
                    json.dump(non_formatted_questions,f,indent=4)
                
                print("Max retries exceeded. Aborting...")
                raise  # re-raise the exception to terminate the program

# save the list of non_formatted_questions to a JSON file
with open ('./prompts_completion_maker/Q&As/not_formated_files.json','w') as f:
    json.dump(non_formatted_questions,f,indent=4)
