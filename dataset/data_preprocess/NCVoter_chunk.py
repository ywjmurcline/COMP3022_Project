import os
import shutil
from utils.profile_dataset import profile_folder_by_file

# Set your target folder
FOLDER_FOLDER = '../cleaned/NCVoters'
DISTINATION = '../cleaned/NCVoters_chunk'

if os.path.isdir(DISTINATION):
    shutil.rmtree(DISTINATION)
    print(f"emptied {DISTINATION}")

os.makedirs(DISTINATION, exist_ok=True)


chunk_by = [
    [0, 20], 
    [0, 40], 
    [0, 60], 
    [0, 80], 
    [0, 100], 
    ]


# Loop through all .zip files in the folder
for a, b in chunk_by:
    input_files = []
    print(f"Processing file {a} to {b}.")
    for i in range(a, b):
        file = os.path.join(FOLDER_FOLDER, f'ncvoter{i+1}.txt')
        if os.path.isfile(file):
            input_files.append(file)
    output_file = os.path.join(DISTINATION, f"ncvoter_{a+1}_{b}.txt")  
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for fname in input_files:
            with open(fname, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
                outfile.write('\n')  # Optional: separate files by newline

    if b == 100:
        shutil.copy(output_file, os.path.join(DISTINATION, f"ncvoter_all.txt") )
        

# Profile the folder
profile_folder_by_file(DISTINATION)
print("Done profiling.")


with open(os.path.join(DISTINATION, "flag"), 'a') as flagfile:
    flagfile.write("1")

print("DONE!")
        
