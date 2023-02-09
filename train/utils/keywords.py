import os
import re

# Path to the folder containing the files
DATA_DIR = 'datasets/noto_sans/train'

# List of keywords to remove from file names
keywords = ['fitzpatrick', 'type-1-2', 'type-3','type-4','type-5','type-6','emoji', 'modifier', 'zero width', 'joiner', 'component']
blacklist = ['fitzpatrick']

# Create an empty dictionary to store the used names
used_names = {}
# Create an empty set to store the unique file names
unique_files = set()
erased_files = set()

# Iterate over all the files in the folder
for file_name in os.listdir(DATA_DIR):
    base_name, file_ext = os.path.splitext(file_name)
    for keyword in keywords:
        # Compile a regular expression pattern for the keyword
        pattern = re.compile(r"\b" + keyword + r"\b")
        # Replace the keyword with an empty string
        base_name = pattern.sub("", base_name)
    new_file_name = base_name + file_ext
    new_file_name = new_file_name.replace("  ", " ")
    # Check if the new file name already exists in the dictionary
    if new_file_name in used_names:
        # if it does, add a suffix (1) to the file name
        suffix = used_names[new_file_name] + 1
        new_file_name = new_base_name + " (" + str(suffix) + ")" + file_ext
        used_names[new_file_name] = suffix
    else:
        # if it does not, add the file name to the dictionary with a value of 1
        used_names[new_file_name] = 1
    # Rename the file
    os.rename(os.path.join(DATA_DIR, file_name), os.path.join(DATA_DIR, new_file_name))
    
    
# # Iterate over all the files in the folder
# for file_name in os.listdir(DATA_DIR):
#     # Get the base name of the file (without the file extension)
#     base_name, _ = os.path.splitext(file_name)
#     split_name = base_name.split(" ")
#     test_name = split_name[0] + split_name[-1]
#     # Check if any part of the file name is in the blacklist
#     if any(word in base_name for word in blacklist):
#         # if it's in the blacklist, Check if the file name is already in the unique files set
#         if test_name in unique_files:
#             # If it is, remove the file
#             erased_files.add(file_name)
#             os.remove(os.path.join(DATA_DIR, file_name))
#         else:
#             # If not, add it to the unique files set
#             unique_files.add(test_name)
            
# print(f"Number of erased files: {len(erased_files)}")