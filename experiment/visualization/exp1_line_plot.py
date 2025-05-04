import json
import matplotlib.pyplot as plt
import os

current_dir = os.path.dirname(__file__)

JSON_PATH1 = os.path.join(current_dir, "../result/exp1_time_data_size/result.json")
FIGURE_PATH1 = os.path.join(current_dir, "../result/exp1_time_data_size/time_data_size.png")

with open(JSON_PATH1 , 'r') as file:
    results = json.load(file)

# Prepare plot data
x_values = []
labels = []
data_by_label = {}

for x_key, alg_results in results.items():
    x = int(x_key.split("-")[1])  # extract the right part of the key (e.g., 20)
    x_values.append(x)

    for full_path, metrics in alg_results.items():
        label = full_path.split("/")[-1]
        if label not in data_by_label:
            data_by_label[label] = {"x": [], "y": []}
        data_by_label[label]["x"].append(x)
        data_by_label[label]["y"].append(metrics["FM addBatch time"])

# Plot
plt.figure(figsize=(10, 6))
for label, values in data_by_label.items():
    plt.plot(values["x"], values["y"], marker='o', linestyle='-', alpha=0.5, label=label)

plt.xlabel("number of entries")
plt.ylabel("Run Time (s)")
plt.title("Run Time vs Data Size")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH1, dpi=300, bbox_inches='tight')
plt.show()



JSON_PATH2 = os.path.join(current_dir, "../result/exp1_time_data_size/result2.json")
FIGURE_PATH2 = os.path.join(current_dir, "../result/exp1_time_data_size/time_data_size2.png")

with open(JSON_PATH2 , 'r') as file:
    results = json.load(file)

# Prepare plot data
x_values = []
labels = []
data_by_label = {}

for x_key, alg_results in results.items():
    x = int(x_key.split("-")[1])  # extract the right part of the key (e.g., 20)
    x_values.append(x)

    for full_path, metrics in alg_results.items():
        label = full_path.split("/")[-1]
        if label not in data_by_label:
            data_by_label[label] = {"x": [], "y": []}
        data_by_label[label]["x"].append(x)
        data_by_label[label]["y"].append(metrics["FM addBatch time"])

# Plot
plt.figure(figsize=(10, 6))
for label, values in data_by_label.items():
    plt.plot(values["x"], values["y"], marker='o', linestyle='-', alpha=0.5, label=label)

plt.xlabel("number of entries")
plt.ylabel("Run Time (s)")
plt.title("Run Time vs Data Size")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH2, dpi=300, bbox_inches='tight')
plt.show()
