import json
import glob

all_data = []

# Loop through all the JSON files that match the pattern
for filename in glob.glob("/home/yaaa3ser/Desktop/fine-tuning-demo/25QAs/generated_QAs*.json"):
    print("Processing file: " + filename)
    # Open the file and load the JSON data into a list
    with open(filename, "r") as f:
        data = json.load(f)
        # Add the data from this file to the all_data list
        all_data.extend(data)

# Write the combined data to a new file
with open("merged_QAs.json", "w") as f:
    json.dump(all_data, f)
