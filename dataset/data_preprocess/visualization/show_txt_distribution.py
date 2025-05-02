import collections
import matplotlib.pyplot as plt
import json
import os
import sys


if len(sys.argv) < 3:
    print("Usage: python script_a.py <argument>")
    sys.exit(1)

directory_path = sys.argv[1]
dataset_name = sys.argv[2]
print(f"Received argument: {directory_path} {dataset_name}")

profile_json = os.path.join(directory_path, "profile.json")

# Open and read the JSON file
with open(profile_json, 'r') as file:
    data = json.load(file)

total_lines = data["total"]["total"]


for filename in os.listdir(directory_path):
    if filename.endswith('_all.txt'):
        all_file = filename
        print(f"Found file: {filename}")


# filename = os.path.join(directory_path, )

# freq_counter = {}
# cnt = 0
# with open(filename, 'r', encoding='utf-8') as f:
#     for line in f:
#         # input(line)
#         line = line.strip()
#         cnt += 1
#         if (cnt % 100000 == 0): print(cnt)
#         if line in freq_counter.keys():
#             freq_counter[line] += 1
#         else:
#             freq_counter[line] = 1

# # freq_dict = dict(collections.Counter(lines))

# # === Step 2: Sort the dictionary by frequency descending ===
# sorted_items = dict(sorted(freq_counter.items(), key=lambda item: item[1], reverse=True))

# # sampled_dict = dict(list(sorted_items.keys())[::100])
# key_sample = list(sorted_items.keys())[::100]

# filtered_dict = {k: sorted_items[k] for k in key_sample if k in sorted_items}


# print(filtered_dict)
# # === Step 3: Plot ===
# labels, counts = zip(*filtered_dict.items())

# plt.figure(figsize=(14, 6))
# plt.bar(labels, counts, color='skyblue')
# plt.xticks([], [])  # hide x-axis labels
# plt.xticks(rotation=90)
# plt.xlabel('value')
# plt.ylabel('Occurance')
# plt.title('Frequencies of NCVoters')
# plt.tight_layout()
# plt.show()