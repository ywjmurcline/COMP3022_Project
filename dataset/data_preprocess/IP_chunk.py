import os
import shutil
from utils.profile_dataset import profile_folder_by_file
import glob
import json
import math
import random

# Set your target folder
FOLDER_FOLDER = '../cleaned/IPs'
DISTINATION = '../cleaned/IPs_chunk'


if os.path.isdir(DISTINATION):
    shutil.rmtree(DISTINATION)
    print(f"emptied {DISTINATION}")

os.makedirs(DISTINATION, exist_ok=True)


# Loop through all .zip files in the folder

input_files = glob.glob(os.path.join(FOLDER_FOLDER, '*.txt'))
profile_json = os.path.join(FOLDER_FOLDER, "profile.json")

all_file = os.path.join(DISTINATION, f"IPs_all.txt")  
print("creating IPs_all.txt")
with open(all_file, 'w', encoding='utf-8') as outfile:
    for fname in input_files:
        with open(fname, 'r', encoding='utf-8') as infile:
            outfile.write(infile.read())
            outfile.write('\n')  # Optional: separate files by newline
    

# Open and read the JSON file
with open(profile_json, 'r') as file:
    data = json.load(file)

total_lines = data["total"]["total"]

PARTITION = 10

chunk_size = math.ceil(total_lines // PARTITION)

with open(all_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

random.shuffle(lines)

for i in range(10):
    chunk = lines[0:(i + 1) * chunk_size]
    print(f"creating IPs_chunk_{i + 1}.txt")
    with open(os.path.join(DISTINATION, f'IPs_chunk_{i + 1}.txt'), 'w', encoding='utf-8') as out:
        out.writelines(chunk)



# Profile the folder
profile_folder_by_file(DISTINATION)
print("Done profiling.")


with open(os.path.join(DISTINATION, "flag"), 'a') as flagfile:
    flagfile.write("1")

print("DONE!")
        