import matplotlib.pyplot as plt
import json
import os

current_dir = os.path.dirname(__file__)

JSON_PATH = os.path.join(current_dir, "../result/exp9_para/result.json")
FIGURE_PATH1 = os.path.join(current_dir, "../result/exp9_para/exp9_para.png")

with open(JSON_PATH , 'r') as file:
    results = json.load(file)

data = {}

for key, value in results.items():
    data[key] = {}
    for sub_key, sub_value in value.items():
        data[key][sub_key] = sub_value["FM addBatch time"]


print(data)

x_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]

plt.figure(figsize=(10, 6))

for method, values in data.items():
    y = [values[o] for o in x_labels]
    plt.plot(x_labels, y, marker='o', label=method)

plt.title("Running Time by Thread Number")
plt.xlabel("Thread Number")
plt.ylabel("Running Time (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH1, dpi=300, bbox_inches='tight')
plt.show()

FIGURE_PATH2 = os.path.join(current_dir, "../result/exp9_para/exp9_para_memory.png")


data_m = {}

for key, value in results.items():
    data_m[key] = {}
    for sub_key, sub_value in value.items():
        data_m[key][sub_key] = sub_value["Memory usage"]
print(data_m)



x_labels = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14"]

plt.figure(figsize=(10, 6))

# Get the two top-level keys
top_keys = list(data_m.keys())
colors = {'red': top_keys[0], 'darkred': top_keys[1]}

# Plot each group with its respective color
for color, top_key in colors.items():
    y = [data_m[top_key][o] for o in x_labels]
    plt.plot(x_labels, y, marker='o', label=f"{top_key}-{method}", color=color)


plt.title("Memory Usage by Thread Number")
plt.xlabel("Thread Number")
plt.ylabel("Memory Usage (MB)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH2, dpi=300, bbox_inches='tight')
plt.show()