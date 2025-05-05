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
FIGURE_PATH3 = os.path.join(current_dir, "../result/exp2_accuracy/exp2_accuracy_PCSA.png")
FIGURE_PATH4 = os.path.join(current_dir, "../result/exp2_accuracy/exp2_accuracy_hyperloglog.png")
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
        stat[algorithm] = {}
        for m, estimates in values.items():
            mean, error, std = mean_error_std(ground_truth, estimates)
            if algorithm == "hyperloglog":
                c = 1
            elif algorithm == "PCSA_O1":
                c = 0.78
            print(f"Algorithm: {algorithm}, m, Mean: {mean}, Error: {error}, Std: {std}, std/truth: {std/ground_truth} ")
            stat[algorithm][int(m)] = {
                "Mean": mean,
                "Error": error,
                "Std": std,
                "std/truth": std/ground_truth,
                "theory": c / int(m)
            }


algorithm = 'hyperloglog'  # Change to the algorithm you want to plot
stat_data = stat[algorithm]

# Extract m values and sort
m_values = sorted(stat_data.keys())

# Extract y values
std_over_total = [stat_data[m]['std/truth'] for m in m_values]
theory = [stat_data[m]['theory'] for m in m_values]

# Plot
plt.figure(figsize=(6, 5))
plt.plot(m_values, std_over_total, label='std/truth', color='tab:blue', marker='o')
plt.plot(m_values, theory, label='theory', color='gray', linestyle='--', marker='x')

plt.xlabel('m')
plt.ylabel('Value')
plt.title(f"std/truth vs theory for {algorithm}")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH4, dpi=300, bbox_inches='tight')
plt.show()

algorithm = 'PCSA_O1'  # Change to the algorithm you want to plot
stat_data = stat[algorithm]

# Extract m values and sort
m_values = sorted(stat_data.keys())

# Extract y values
std_over_total = [stat_data[m]['std/truth'] for m in m_values]
theory = [stat_data[m]['theory'] for m in m_values]

# Plot
plt.figure(figsize=(6, 5))
plt.plot(m_values, std_over_total, label='std/truth', color='tab:blue', marker='o')
plt.plot(m_values, theory, label='theory', color='gray', linestyle='--', marker='x')

plt.xlabel('m')
plt.ylabel('Value')
plt.title(f"std/truth vs theory for {algorithm}")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH3, dpi=300, bbox_inches='tight')
plt.show()


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