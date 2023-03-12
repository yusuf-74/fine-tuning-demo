import json

cleaned_paragraphs = []


with open('paragraphs.json') as f:
    paragraphs = json.load(f)
    
for paragraph in paragraphs:
    for sentence in paragraph:
        if len(sentence) > 700:
            cleaned_paragraphs.append(sentence)

with open('cleaned_paragraphs.json','w') as f:
    json.dump(cleaned_paragraphs,f,indent=4)