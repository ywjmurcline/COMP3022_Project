import matplotlib.pyplot as plt
import json
import os

current_dir = os.path.dirname(__file__)

JSON_PATH = os.path.join(current_dir, "../result/exp3_memory/result.json")
FIGURE_PATH1 = os.path.join(current_dir, "../result/exp3_memory/exp3_memory.png")

with open(JSON_PATH , 'r') as file:
    results = json.load(file)

data = {}

for key, value in results.items():
    data[key] = {}
    for sub_key, sub_value in value.items():
        sum = 0
        last = None
        for sub_key2, sub_value2 in sub_value.items():
           sum += sub_value2["Memory usage"] if sub_value2["Memory usage"] < 10000000 else last
           last = sub_value2["Memory usage"]

        data[key][sub_key] = sum / len(sub_value.keys())
        


print(data)

x_labels = ["4", "8", "16", "32", "64", "128"]

plt.figure(figsize=(10, 6))

for method, values in data.items():
    y = [values[o] for o in x_labels]
    plt.plot(x_labels, y, marker='o', label=method)

plt.title("Memory Usage by m")
plt.xlabel("m")
plt.ylabel("Memory Usage (MB)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH1, dpi=300, bbox_inches='tight')
plt.show()