import csv , json

data = []
with open('./bld-data-Q&A.csv','r') as file:
    reader = csv.reader(file)
    next(reader)
    for idx , row in enumerate(reader):
        row_data = dict()
        row_data["prompt"] = row[3]
        row_data["completion"] = row[4]
        data.append(row_data)

with open('bld-data-Q&A.json','w') as file:
    json.dump(data,file)