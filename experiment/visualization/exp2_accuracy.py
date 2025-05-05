import matplotlib.pyplot as plt
import json
import os
import pandas as pd
import seaborn as sns
import numpy as np
from utils import get_ground_truth, get_size, mean_error_std

current_dir = os.path.dirname(__file__)

JSON_PATH = os.path.join(current_dir, "../result/exp2_accuracy/result.json")
FIGURE_PATH1 = os.path.join(current_dir, "../result/exp2_accuracy/exp2_accuracy.png")
FIGURE_PATH2 = os.path.join(current_dir, "../result/exp2_accuracy/exp2_accuracy_wo_loglog.png")
DATA_PATH = os.path.abspath(os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt"))



with open(JSON_PATH , 'r') as file:
    results = json.load(file)

data = {}


for algorithm, data_paths in results.items():
    data[algorithm] = {}
    for m, trials in data_paths.items():
        cardinalities = []
        for trial_data in trials.values():
            cardinality = trial_data.get("Estimated cardinality")
            if cardinality is not None:
                cardinalities.append(cardinality)
        data[algorithm][m] = cardinalities

total = get_size(DATA_PATH)
ground_truth = get_ground_truth(DATA_PATH)
# print(f"Ground Truth: {ground_truth}")

stat = {}
for algorithm, values in data.items():
    if algorithm in ["hyperloglog", "PCSA_O1"]:
        continue
    stat[algorithm] = {}
    for hash, estimates in values.items():
        mean, error, std = mean_error_std(ground_truth, estimates)
        print(f"Algorithm: {algorithm}, Hash: {hash}, Mean: {mean}, Error: {error}, Std: {std}, std/truth: {std/ground_truth}, theory: ")
        stat[algorithm][hash] = {
            "Mean": mean,
            "Error": error,
            "Std": std,
            "std/truth": std/ground_truth
        }


  

# print(data)


data_for_plot = []
for algo, m_dict in data.items():
    for m, estimates in m_dict.items():
        print(f"Algorithm: {algo}, m: {m}, Estimated Cardinality: {estimates[0]}")
        for value in estimates:
            
            data_for_plot.append({'Algorithm': algo, 'm': int(m), 'Estimated Cardinality': value})

df_plot = pd.DataFrame(data_for_plot)


truth = get_ground_truth(DATA_PATH)
print(truth)

# Create boxplot

plt.figure(figsize=(12, 6))
sns.boxplot(data=df_plot, x='m', y='Estimated Cardinality', hue='Algorithm')
plt.axhline(truth, color='black', linestyle='--', label=f'Ground Truth: {truth}')
plt.title("Estimated Cardinality by m and Algorithm")
plt.xlabel("m")
plt.ylabel("Estimated Cardinality")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH1, dpi=300, bbox_inches='tight')
plt.show()


data_for_plot = []
for algo, m_dict in data.items():
    if algo != "loglog_O1":
        for m, estimates in m_dict.items():
            print(f"Algorithm: {algo}, m: {m}, Estimated Cardinality: {estimates[0]}")
            for value in estimates:
                
                data_for_plot.append({'Algorithm': algo, 'm': int(m), 'Estimated Cardinality': value})

df_plot = pd.DataFrame(data_for_plot)


# Create boxplot

plt.figure(figsize=(12, 6))
sns.boxplot(data=df_plot, x='m', y='Estimated Cardinality', hue='Algorithm')
plt.axhline(truth, color='black', linestyle='--', label=f'Ground Truth: {truth}')
plt.title("Estimated Cardinality by m and Algorithm")
plt.xlabel("m")
plt.ylabel("Estimated Cardinality")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH2, dpi=300, bbox_inches='tight')
plt.show()