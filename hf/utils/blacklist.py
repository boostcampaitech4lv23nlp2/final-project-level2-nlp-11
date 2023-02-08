import os

# Path to the folder containing the files
folder_path = 'datasets/noto_sans'

# Create a blacklist of words
blacklist = ['fitzpatrick']

# Create an empty set to store the unique file names
unique_files = set()
erased_files = set()

# Iterate over all the files in the folder
for file_name in os.listdir(folder_path):
    # Get the base name of the file (without the file extension)
    base_name, _ = os.path.splitext(file_name)
    split_name = base_name.split(" ")
    test_name = split_name[0] + split_name[-1]
    # Check if any part of the file name is in the blacklist
    if any(word in base_name for word in blacklist):
        # if it's in the blacklist, Check if the file name is already in the unique files set
        if test_name in unique_files:
            # If it is, remove the file
            erased_files.add(file_name)
            os.remove(os.path.join(folder_path, file_name))
        else:
            # If not, add it to the unique files set
            unique_files.add(test_name)
            
print(erased_files)
