from datasets import load_dataset
from pororo import Pororo
import chardet
# make virtual environment first: and pip install pororo
dataset = load_dataset('soypablo/Emoji_Dataset-Openmoji') # write dataset path what you want to get korean dataset
dataset_text = dataset['train']['text']

# print(dataset_text)
ko_txt = []
mt = Pororo(task="translation", lang="multi")
for idx, en_txt in enumerate(dataset_text) :
    print(en_txt.encode('utf-8', 'ignore').decode('utf-8') )
    ko_text = mt(en_txt, src='en', tgt='ko')
    ko_txt.append(ko_text)

with open('train_text.txt', 'w') as file:
    for kt in ko_txt:
        file.write(kt + '\n')
