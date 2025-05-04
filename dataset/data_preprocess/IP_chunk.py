import os
import shutil
from utils.profile_dataset import profile_folder_by_file
import glob
import json
import math
import random
from utils.entropy import compute_entropy_by_folder

# Set your target folder
FOLDER_FOLDER = '../cleaned/IPs'
DISTINATION = '../cleaned/IPs_chunk'
DISTINATION2 = '../cleaned/IPs_imbalanced_chunk'


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

PARTITION = 10000000

chunk_size = math.ceil(total_lines // PARTITION)

with open(all_file, 'r', encoding='utf-8') as f:
    lines = f.readlines()

random.shuffle(lines)

for i in range(10):
    chunk = lines[0:int((i + 1) * PARTITION / 10 * chunk_size)]
    print(f"creating IPs_chunk_{i + 1}.txt")
    with open(os.path.join(DISTINATION, f'IPs_chunk_{i + 1}.txt'), 'w', encoding='utf-8') as out:
        out.writelines(chunk)


# Profile the folder
profile_folder_by_file(DISTINATION)
print("Done profiling.")

with open(os.path.join(DISTINATION, "flag"), 'a') as flagfile:
    flagfile.write("1")

print("DONE 50%")

if os.path.isdir(DISTINATION2):
    shutil.rmtree(DISTINATION2)
    print(f"emptied {DISTINATION2}")

os.makedirs(DISTINATION2, exist_ok=True)

for i in [1, 10, 1000, 100000, 1000000, 3000000, 6000000, 10000000]:  # start from 1 to avoid division by zero
    chunk = lines[0: i * chunk_size]  #  chunk = 1/10,000,000 all
    multiplier = PARTITION / (i)
    target_size = math.ceil(len(chunk) * multiplier)

    # Upsample with randomness
    if chunk:
        upsampled_chunk = [random.choice(chunk) for _ in range(target_size)]
    else:
        upsampled_chunk = []

    upsampled_chunk += lines[:]
    print(f"creating IPs_chunk_{i}.txt with {len(upsampled_chunk)} lines")
    with open(os.path.join(DISTINATION2, f'IPs_chunk_unbalanced_{i}.txt'), 'w', encoding='utf-8') as out:
        out.writelines(upsampled_chunk)


# Profile the folder
profile_folder_by_file(DISTINATION2)
print("Done profiling.")

compute_entropy_by_folder(DISTINATION2)
print("Done computing entropy.")


with open(os.path.join(DISTINATION2, "flag"), 'a') as flagfile:
    flagfile.write("1")

print("DONE 100%")

        