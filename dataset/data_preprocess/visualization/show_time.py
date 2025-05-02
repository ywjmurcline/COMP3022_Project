import json
import matplotlib.pyplot as plt

# Simulate the JSON input as a Python dict
results = {
    "64-20": {
        "Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/fm": {
            "FM addBatch time": 7.961268,
            "Estimated cardinality": 1009664.0,
            "Memory usage": 4.077016
        },
        "Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/PCSA": {
            "FM addBatch time": 0.063105,
            "Estimated cardinality": 938019.345833,
            "Memory usage": 3.920766
        },
        "Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/AMS": {
            "FM addBatch time": 8.431079,
            "Estimated cardinality": 1059994.244011,
            "Memory usage": 4.108266
        },
        "Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/algorithms/executable/hyperloglog": {
            "FM addBatch time": 0.063971,
            "Estimated cardinality": 1006821.561535,
            "Memory usage": 3.827016
        }
    }
}

path = '/Users/lily/Documents/2024-2025_Spring/algorithm_lab/cadinality_estimation/COMP3022_Project/experiment/time.json'

with open(path, 'r') as file:
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
plt.show()
