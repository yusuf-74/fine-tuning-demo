import json

cleaned_paragraphs = []
temp = []
seen = set()

def check_alphanumeric(string):
    alpha = False
    num = False
    for char in string:
        if char.isdigit():
            num = True
        if char.isalpha():
            alpha = True
    return num & alpha

with open('paragraphs.json') as f:
    paragraphs = json.load(f)
    
for paragraph in paragraphs:
    for sentence in paragraph:
        if len(sentence) > 700:
            temp.append(sentence)

with open('cleaned_paragraphs.json','w') as f:
    for sentence in temp:
        x = sentence.split(' ')
        if check_alphanumeric(x[0]):
            x[0] = 'course of'
        paragraph = ' '.join(x)
        if paragraph not in seen:
            seen.add(paragraph)
            cleaned_paragraphs.append(paragraph)
            
    json.dump(cleaned_paragraphs[:18]+cleaned_paragraphs[19:38]+cleaned_paragraphs[39:],f,indent=4)