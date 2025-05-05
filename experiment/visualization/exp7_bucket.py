import matplotlib.pyplot as plt
import numpy as np
import matplotlib.pyplot as plt
import json
import os
from utils import get_ground_truth, mean_error_std
import pandas as pd
import seaborn as sns

current_dir = os.path.dirname(__file__)

EXP_NAME = "exp7_bucket"

JSON_PATH_hash = os.path.join(current_dir, f"../result/{EXP_NAME}/result_hash.json")
JSON_PATH_mix = os.path.join(current_dir, f"../result/{EXP_NAME}/result_mix.json")
FIGURE_PATH_hash= os.path.join(current_dir, f"../result/{EXP_NAME}/{EXP_NAME}_hash.png")
FIGURE_PATH_mix1= os.path.join(current_dir, f"../result/{EXP_NAME}/{EXP_NAME}_mix1.png")
FIGURE_PATH_mix2= os.path.join(current_dir, f"../result/{EXP_NAME}/{EXP_NAME}_mix2.png")
DATA_PATH = os.path.join(current_dir, "../../dataset/cleaned/NCVoters_chunk/ncvoter_1_60.txt")

truth = get_ground_truth(DATA_PATH)

with open(JSON_PATH_hash , 'r') as file:
    results = json.load(file)

data = {}

for algorithm, value in results.items():
    data[algorithm] = {}
    for hash, sub_value in value.items():
        data[algorithm][hash] = sub_value["0"]["Bucket counts"]


fig, axs = plt.subplots(2, 2, figsize=(10, 4))

alg = "hyperloglog_bucket"
lists = [value for value in data[alg].values()]
print(lists)
titles = [hash for hash in data[alg].keys()]
x_labels = [x for x in range(len(lists[0]))]


for i, ax in enumerate(axs.flat):
    ax.bar(x_labels, lists[i])
    ax.set_xticklabels([]) 
    ax.set_title(titles[i])
    ax.set_ylabel('Occurence')
    ax.set_ylim(50000, 100000)

plt.tight_layout()
plt.savefig(FIGURE_PATH_hash, dpi=300, bbox_inches='tight')
plt.show()


with open(JSON_PATH_mix , 'r') as file:
    results = json.load(file)

data = {}

stat = {}

for algorithm, value in results.items():
    data[algorithm] = {}
    stat[algorithm] = {}
    for hash, trails in value.items():
        data[algorithm][hash] = []
        for trail_num, trial_data in trails.items():
            data[algorithm][hash].append(trial_data["Estimated cardinality"])
        mean, error, std =  mean_error_std(truth, data[algorithm][hash])
        stat[algorithm][hash] = error

print(stat)


def box_plot(data, figure_path, name, p):
    data_for_plot = []
    for hash, estimates in data.items():
        for value in estimates:
            data_for_plot.append({'hash': hash, 'Estimated Cardinality': value})

    df_plot = pd.DataFrame(data_for_plot)


    

    # Create boxplot

    plt.figure(figsize=(10, 3))
    sns.boxplot(data=df_plot, x='hash', y='Estimated Cardinality', palette=p)
    plt.axhline(truth, color='black', linestyle='--', label=f'Ground Truth: {truth}', alpha=1)
    plt.title("Estimated Cardinality by Hash (hash: select_string)")
    plt.xlabel("hash")
    plt.ylabel(f"Estimated Cardinality ({name})")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(figure_path, dpi=300, bbox_inches='tight')
    plt.show()

box_plot(data["hyperloglog_mixhash"], FIGURE_PATH_mix1, name="hyperloglog", p="Oranges")

box_plot(data["PCSA_mixhash"], FIGURE_PATH_mix2, name="hyperloglog",  p="BuPu")
