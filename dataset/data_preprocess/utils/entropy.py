from collections import Counter
import math
import os
import json

def compute_entropy(data):
    total = len(data)
    counts = Counter(data)
    return -sum((count / total) * math.log2(count / total) for count in counts.values())

def compute_entropy_by_file(file_path):
    with open(file_path, 'r') as file:
        data = file.read().splitlines()
    return compute_entropy(data)

def compute_entropy_by_folder(folder_path):
    entropies = {}
    for filename in os.listdir(folder_path):
        if filename.endswith('.txt'):
            file_path = os.path.join(folder_path, filename)
            entropies[filename] = compute_entropy_by_file(file_path)
    with open(os.path.join(folder_path, "entropy.json"), 'w') as outfile:
        json.dump(entropies, outfile, indent=2)
