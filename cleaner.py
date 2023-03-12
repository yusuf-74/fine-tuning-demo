import json

cleaned_paragraphs = []
cleaned_paragraphs2 = []
temp = []
temp2 = []
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

with open('paragraphs.json' ,'r') as f:
    paragraphs = json.load(f)

with open('paragraphs2.json', 'r') as f:
    paragraphs2 = json.load(f)
    
for paragraph in paragraphs:
    for sentence in paragraph:
        if len(sentence) > 700:
            temp.append(sentence)
            
for paragraph in paragraphs2:
    for sentence in paragraph:
        if len(sentence) > 700:
            temp2.append(sentence)

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
    

with open('cleaned_paragraphs2.json','w') as f:
    for sentence in temp2:
        x = sentence.split(' ')
        if check_alphanumeric(x[0]):
            x[0] = 'course of'
        paragraph = ' '.join(x)
        if paragraph not in seen:
            seen.add(paragraph)
            cleaned_paragraphs2.append(paragraph)
            
    json.dump(cleaned_paragraphs2,f,indent=4)