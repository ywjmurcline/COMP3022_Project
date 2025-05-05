import matplotlib.pyplot as plt
import json
import os

current_dir = os.path.dirname(__file__)

JSON_PATH = os.path.join(current_dir, "../result/exp8_complier/result_para.json")
FIGURE_PATH = os.path.join(current_dir, "../result/exp8_complier/exp8_complier_para.png")

with open(JSON_PATH , 'r') as file:
    results = json.load(file)

data = {}

for key, value in results.items():
    data[key] = {}
    for sub_key, sub_value in value.items():
        data[key][sub_key] = sub_value["FM addBatch time"]


print(data)

x_labels = ["O0", "O1"]

# plt.figure(figsize=(10, 6))
plt.figure(figsize=(4, 4)) 

for method, values in data.items():
    y = [values[o] for o in x_labels]
    plt.plot(x_labels, y, marker='o', label=method, alpha = 0.7)


plt.title("FM addBatch Time by Method and Optimization Level")
plt.xlabel("Optimization Level")
plt.ylabel("FM addBatch Time (s)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig(FIGURE_PATH, dpi=300, bbox_inches='tight')
plt.show()
