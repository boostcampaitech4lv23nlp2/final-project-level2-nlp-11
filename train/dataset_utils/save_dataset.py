import datasets


dataset = datasets.load_dataset('soypablo/Emoji_Dataset-Openmoji')
dataset.save_to_disk('datasets/open-emoji')