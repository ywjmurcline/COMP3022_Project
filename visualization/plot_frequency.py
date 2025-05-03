import matplotlib.pyplot as plt
from matplotlib.colors import Normalize, LinearSegmentedColormap
import json
import os
import sys
import math
import shutil

# get argument
if len(sys.argv) < 4:
    print("Usage: python script_a.py <argument>")
    sys.exit(1)

directory_path = sys.argv[1] 
dataset_name = sys.argv[2]
save_path = sys.argv[3] 

print(f"Received argument: {directory_path} {dataset_name}")

figure_path = os.path.join(save_path, dataset_name) + ".png"

# check if directory_path exists
os.makedirs(save_path, exist_ok=True)

if os.path.isfile(figure_path ):
    if input("Exist previous result, do you want to replace it? (y/n): ").lower() != 'y':
        print("Exiting without changes.")
        sys.exit(0)
    else:
        os.remove(figure_path )
    print(f"deleted {figure_path}")





# get data
for filename in os.listdir(directory_path):
    if filename.endswith('_all.txt'):
        all_file = filename
        print(f"Found file: {filename}")

all_filename = os.path.join(directory_path, all_file)

# get profile info

profile_json = os.path.join(directory_path, "profile.json")

# Open and read the JSON file
with open(profile_json, 'r') as file:
    data = json.load(file)

total_lines = data[all_file]["total"]


# count frequency
freq_counter = {}
cnt = 0
with open(all_filename, 'r', encoding='utf-8') as f:
    for line in f:
        # input(line)
        line = line.strip()
        cnt += 1
        if (cnt % 100000 == 0): print(f"\rprogress: {(cnt/total_lines):.2%}", end='', flush=True)
        if line in freq_counter.keys():
            freq_counter[line] += 1
        else:
            freq_counter[line] = 1

# Sort the dictionary by frequency descending 
sorted_items = dict(sorted(freq_counter.items(), key=lambda item: item[1], reverse=True))

COUNT = 50000
# # sample dict otherwise, matplotlib might break
print("\nsampling data for visualization")
key_sample = list(sorted_items.keys())[::math.ceil(total_lines/COUNT)]

filtered_dict = {k: sorted_items[k] for k in key_sample if k in sorted_items}


# ready for plot
labels, counts = zip(*filtered_dict.items())


# show figure
plt.figure(figsize=(14, 6))
plt.bar(labels, counts, color="#97CCE8")
plt.xticks([], [])  # Hide x-axis tick labels
plt.xticks(rotation=90)
plt.xlabel('Value')
plt.ylabel('Occurrence')
# plt.xscale('log')  # Set y-axis to logarithmic scale
plt.title(f'Frequencies of {dataset_name} (sampled 1 in {math.ceil(total_lines/COUNT)})')
plt.tight_layout()
plt.savefig(figure_path, dpi=300, bbox_inches='tight')
plt.show()


