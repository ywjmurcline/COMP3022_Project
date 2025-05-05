import matplotlib.pyplot as plt
import json
import os
from utils import get_ground_truth, get_size, mean_error_std
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd


EXP_NAME = "exp6_hash"

current_dir = os.path.dirname(__file__)


JSON_PATH = os.path.join(current_dir, f"../result/{EXP_NAME}/result.json")
FIGURE_PATH1 = os.path.join(current_dir, f"../result/{EXP_NAME}/{EXP_NAME}.png")
FIGURE_PATH2 = os.path.join(current_dir, f"../result/{EXP_NAME}/{EXP_NAME}_wo_loglog.png")
DATA_PATH = os.path.abspath(os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt"))


with open(JSON_PATH , 'r') as file:
    results = json.load(file)

data = {}

def to_markdown(headers, rows):
    header_line = "| " + " | ".join(headers) + " |"
    separator = "| " + " | ".join(["---"] * len(headers)) + " |"
    row_lines = ["| " + " | ".join(map(str, row)) + " |" for row in rows]
    return "\n".join([header_line, separator] + row_lines)

def box_plot(data, figure_path):
    data_for_plot = []
    for algo, m_dict in data.items():
        for hash, estimates in m_dict.items():
            print(f"Algorithm: {algo}, 'hash': {hash}, Estimated Cardinality: {estimates[0]}")
            for value in estimates:
                
                data_for_plot.append({'Algorithm': algo, 'hash': hash, 'Estimated Cardinality': value})

    df_plot = pd.DataFrame(data_for_plot)


    truth = get_ground_truth(DATA_PATH)

    # Create boxplot

    plt.figure(figsize=(12, 6))
    sns.boxplot(data=df_plot, x='hash', y='Estimated Cardinality', hue='Algorithm')
    plt.axhline(truth, color='black', linestyle='--', label=f'Ground Truth: {truth}')
    plt.title("Estimated Cardinality by Hash and Algorithm")
    plt.xlabel("hash")
    plt.ylabel("Estimated Cardinality")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.show()



for algorithm, data_paths in results.items():
    data[algorithm] = {}
    for hash, trials in data_paths.items():
        cardinalities = []
        for trial_data in trials.values():
            cardinality = trial_data.get("Estimated cardinality")
            if cardinality is not None:
                cardinalities.append(cardinality)
        data[algorithm][hash] = cardinalities


box_plot(data, FIGURE_PATH1)

del data["loglog_O1"]

box_plot(data, FIGURE_PATH2)

total = get_size(DATA_PATH)
ground_truth = get_ground_truth(DATA_PATH)
# print(f"Ground Truth: {ground_truth}")
for algorithm, values in data.items():
    for hash, estimates in values.items():
        mean, error, std = mean_error_std(ground_truth, estimates)
        print(f"Algorithm: {algorithm}, Hash: {hash}, Mean: {mean}, Error: {error}, Std: {std}, std/total: {std/total}")


# print(data)



