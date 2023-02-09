import json
import os

# path to dataset folder
dataset_path = 'datasets/noto_sans/train'

# get list of all files in dataset folder
files = os.listdir(dataset_path)

# open jsonl file for writing
with open('dataset.jsonl', 'w', encoding='utf-8') as jsonl_file:
    # loop through files in dataset folder
    for file in files:
        # get file name and file path
        # create dictionary with file name and text
        data = {'file_name': f'{file}', 'text': f'{file[:-4]}'}
        
        # write dictionary to jsonl file
        jsonl_file.write(json.dumps(data) + '\n')
